/* Halcyon content calendar · edit mode (v2, 11 Nov 2026)
   Loads after index.html's own script and hooks grid(), open(), pubState() and fmt() from outside,
   so the template and the post data in index.html stay untouched.
   Edits live in this browser's localStorage only, until they're copied out and baked into the data. */
(function(){
"use strict";
const KEY="hal_cal_edits_v1", MODEK="hal_cal_editmode_v1";
const MON=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const DOW7=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
const DOT={r:"#ff5a6e",y:"#ffc94a",g:"#3ddc84"}, DOTNAME={r:"Not scheduled",y:"Scheduled",g:"Posted"};
const COPYF=[["caption","Caption"],["fbcap","Backup caption"]];

// ---------- stable ids from each post's ORIGINAL fields ----------
function hash(s){let h=5381;for(let i=0;i<s.length;i++)h=((h<<5)+h+s.charCodeAt(i))>>>0;return h.toString(36);}
const ORIG={}, BYKEY={};
P.forEach(p=>{
  const k=(p.platform==="TikTok"?"tt":"ig")+"-"+p.date.replace(/-/g,"")+"-"+p.time.replace(":","")+"-"+hash(p.platform+"|"+p.title+"|"+p.date+"|"+p.time);
  p._k=k; BYKEY[k]=p;
  ORIG[k]={date:p.date,time:p.time,timeLabel:p.timeLabel,myt:p.myt,day:p.day,caption:p.caption||"",fbcap:p.fbcap||""};
});

// ---------- storage ----------
let E={};
try{E=JSON.parse(localStorage.getItem(KEY)||"{}")||{};}catch(e){E={};}
for(const k in E) if(!BYKEY[k]) delete E[k];          // drop edits for posts that no longer exist
function persist(){try{localStorage.setItem(KEY,JSON.stringify(E));}catch(e){toast("Couldn't save in this browser");}}
const count=()=>Object.keys(E).length;

// set one field; drop it if it matches the original again, drop the post's edit when empty
function setF(k,f,v){
  const o=ORIG[k]; E[k]=E[k]||{};
  if(f==="pub"){ if(v==null) delete E[k].pub; else E[k].pub=v; }
  else if(v===o[f]) delete E[k][f]; else E[k][f]=v;
  if(!Object.keys(E[k]).length) delete E[k];
}

// ---------- time helpers ----------
const pad=n=>String(n).padStart(2,"0");
function etLabel(t){const [h,m]=t.split(":").map(Number);return ((h%12)||12)+":"+pad(m)+" "+(h<12?"AM":"PM")+" ET";}
function mytLabel(d,t){ // ET is UTC-5 until 8 Mar, MYT is UTC+8, so MYT = ET + 13h
  const [y,mo,dd]=d.split("-").map(Number),[h,m]=t.split(":").map(Number);
  const x=new Date(Date.UTC(y,mo-1,dd,h+13,m));
  return ((x.getUTCHours()%12)||12)+":"+pad(x.getUTCMinutes())+" "+(x.getUTCHours()<12?"AM":"PM")+" "+DOW7[x.getUTCDay()]+" "+x.getUTCDate()+" "+MON[x.getUTCMonth()]+" MYT";
}

// ---------- apply edits onto the live post objects ----------
function applyAll(){
  P.forEach(p=>{
    const o=ORIG[p._k], e=E[p._k]||{};
    p.date=e.date||o.date; p.time=e.time||o.time;
    p.caption=("caption" in e)?e.caption:o.caption;
    if(o.fbcap||("fbcap" in e)) p.fbcap=("fbcap" in e)?e.fbcap:o.fbcap;
    if(e.time||e.date){ p.timeLabel=etLabel(p.time); p.myt=mytLabel(p.date,p.time); }
    else { p.timeLabel=o.timeLabel; p.myt=o.myt; }
    p.day=o.day;
  });
  // keep TikTok "Post N" in date order once a TikTok has moved
  if(P.some(p=>p.platform==="TikTok"&&E[p._k]&&(E[p._k].date||E[p._k].time))){
    P.filter(p=>p.platform==="TikTok").sort((a,b)=>(a.date+a.time).localeCompare(b.date+b.time)).forEach((p,i)=>p.day="Post "+(i+1));
  }
}

// ---------- hooks into the page ----------
const _grid=grid, _open=open, _pub=pubState;
fmt=function(iso){const x=dt(iso);return DOW[(x.getUTCDay()+6)%7]+" "+x.getUTCDate()+" "+MON[x.getUTCMonth()];};
pubState=function(p){const e=E[p._k];if(e&&e.pub)return [e.pub,DOTNAME[e.pub]];return _pub(p);};
grid=function(){
  _grid();
  // tag each in-month day with its date: in-month days are the non-pad cells, in order, Nov then Dec
  let mi=-1, prev=99;
  document.querySelectorAll("#grid .day:not(.pad)").forEach(d=>{
    const n=+d.querySelector(".dn b").textContent; if(n<prev) mi++; prev=n;
    const [y,m]=MONTHS[mi]; d.dataset.date=y+"-"+pad(m+1)+"-"+pad(n);
  });
  document.querySelectorAll("#grid .card").forEach(c=>{
    const p=P.find(x=>x.id===c.dataset.id); if(!p) return;
    c.dataset.k=p._k;
    const e=E[p._k];
    if(e){ c.classList.add("ed"); const t=c.querySelector(".t"); if(t&&!c.querySelector(".edt")) t.insertAdjacentHTML("beforebegin",`<span class="edt">Edited</span>`); }
    if(e&&e.pub){ const d=c.querySelector(".pub"); if(d) d.classList.add("man"); }
  });
};
open=function(id){
  _open(id);
  const p=P.find(x=>x.id===id); if(!p||!EDIT) return;
  const e=E[p._k]||{}, o=ORIG[p._k];
  const st=e.pub?DOTNAME[e.pub]:"Automatic ("+_pub(p)[1].toLowerCase()+")";
  const tx=COPYF.filter(([f])=>f==="caption"||o[f]).map(([f,lab])=>`<label class="efl">${lab}${(f in e)?' <span class="edt">Edited</span>':""}<textarea data-f="${f}" rows="${f==="caption"?9:5}">${esc(p[f]||"")}</textarea></label>`).join("");
  const html=`<div class="eform" data-k="${p._k}">
    <div class="lab" style="color:var(--c)">Edit this post</div>
    <div class="erow"><label class="efl">Date<input type="date" data-f="date" value="${p.date}" min="2026-11-01" max="2026-12-31"></label>
    <label class="efl">Time (ET)<input type="time" data-f="time" value="${p.time}" step="300"></label>
    <label class="efl">Status dot<select data-f="pub"><option value="">Automatic</option><option value="r">Not scheduled</option><option value="y">Scheduled</option><option value="g">Posted</option></select></label></div>
    ${tx}
    <div class="ebtns"><button class="btn" data-act="save">Save</button><button class="ebtn" data-act="orig"${E[p._k]?"":" disabled"}>Back to original</button><span class="enote">Now: ${esc(st)}${E[p._k]?" · original "+fmt(o.date)+", "+esc(o.timeLabel):""}</span></div>
  </div>`;
  const h2=document.querySelector("#dr h2"); h2.insertAdjacentHTML("afterend",html);
  document.querySelector('.eform select[data-f="pub"]').value=e.pub||"";
};

// ---------- styles ----------
document.head.insertAdjacentHTML("beforeend",`<style>
.hdr-r{display:flex;align-items:center;gap:10px}
#editBtn{background:transparent;border:1px solid var(--c);color:var(--c);font:600 13px Poppins,sans-serif;padding:8px 18px;border-radius:999px;cursor:pointer}
#editBtn.on{background:var(--c);color:#001514;box-shadow:0 0 18px rgba(0,251,244,.35)}
.ebar{position:sticky;top:0;z-index:9;display:none;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 14px;padding:10px 14px;background:rgba(14,20,24,.96);border:1px solid rgba(0,251,244,.45);border-radius:12px;box-shadow:0 0 24px rgba(0,251,244,.08);backdrop-filter:blur(6px)}
body.editing .ebar{display:flex}
.ebar .n{font-weight:600;font-size:14px;margin-right:auto}.ebar .n i{font-style:normal;color:var(--c)}
.ebar .hint{font-size:12px;color:var(--ink3);flex-basis:100%;order:9}
.ebtn{background:transparent;border:1px solid #2b3a41;color:var(--ink);font:500 13px Poppins,sans-serif;padding:7px 14px;border-radius:999px;cursor:pointer}
.ebtn:hover{border-color:var(--c);color:var(--c)}.ebtn[disabled]{opacity:.4;cursor:default;border-color:#2b3a41;color:var(--ink)}
.ebtn.warn{border-color:#ff5a6e;color:#ff8fa3}
body.editing .card{touch-action:none;user-select:none;-webkit-user-select:none;cursor:grab}
body.editing .card img{pointer-events:none}
body.editing .card .pub{width:13px;height:13px;top:6px;right:6px;cursor:pointer}
body.editing .card .pub::after{content:"";position:absolute;inset:-8px}
.card .pub.man{box-shadow:0 0 0 2px var(--s2),0 0 0 3.5px #fff}
.card.ed{box-shadow:inset 0 0 0 1px rgba(0,251,244,.35)}
.edt{display:inline-block;font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;font-weight:600;color:var(--c);border:1px solid rgba(0,251,244,.4);border-radius:5px;padding:0 5px;margin-top:4px}
.card.dragsrc{opacity:.35}
.dghost{position:fixed;z-index:60;pointer-events:none;width:var(--w);opacity:.92;transform:rotate(-2deg);box-shadow:0 18px 40px rgba(0,0,0,.6),0 0 0 1px var(--c)!important;background:var(--s3)!important}
.day.dropok{background:rgba(0,251,244,.07);box-shadow:inset 0 0 0 2px rgba(0,251,244,.7)}
.card.dropok{box-shadow:0 0 0 2px var(--c),0 0 18px rgba(0,251,244,.35)}
body.dragging,body.dragging *{cursor:grabbing!important}
.eform{border:1px solid rgba(0,251,244,.4);border-radius:12px;padding:14px;margin:14px 0 16px;background:var(--s1)}
.erow{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.efl{display:flex;flex-direction:column;gap:5px;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink3);font-weight:500;margin-top:10px}
.efl input,.efl select,.efl textarea{background:var(--bg);border:1px solid var(--line);border-radius:8px;color:var(--ink);font:13px/1.5 Poppins,sans-serif;padding:8px 10px;letter-spacing:0;text-transform:none;color-scheme:dark}
.efl textarea{resize:vertical}.efl input:focus,.efl select:focus,.efl textarea:focus{outline:none;border-color:var(--c)}
.ebtns{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:12px}.enote{font-size:12px;color:var(--ink3)}
@media (max-width:600px){.erow{grid-template-columns:1fr}}
</style>`);

// ---------- header button and edit bar ----------
const hdr=document.querySelector("header");
hdr.insertAdjacentHTML("beforeend",`<div class="hdr-r"><button id="editBtn" type="button">Edit</button></div>`);
document.querySelector("#v-cal").insertAdjacentHTML("afterbegin",`<div class="ebar" id="ebar">
  <span class="n" id="ecount"></span>
  <button class="ebtn" id="eCopy" type="button">Copy my edits</button>
  <button class="ebtn" id="eUndo" type="button">Undo all edits</button>
  <button class="btn" id="eDone" type="button">Done</button>
  <span class="hint">Drag a post to another day to move it, or onto another post to swap. Click a dot to change its status. Click a post to edit its date, time and copy.</span>
</div>`);

let EDIT=false;
function setEdit(on){EDIT=on;document.body.classList.toggle("editing",on);document.getElementById("editBtn").classList.toggle("on",on);document.getElementById("editBtn").textContent=on?"Editing":"Edit";try{sessionStorage.setItem(MODEK,on?"1":"")}catch(e){}if(!on)disarm();}
function bar(){const n=count();document.getElementById("ecount").innerHTML=n?`<i>${n}</i> post${n===1?"":"s"} edited`:"No edits yet";
  document.getElementById("eCopy").disabled=!n;document.getElementById("eUndo").disabled=!n;
  const b=document.getElementById("editBtn");b.textContent=(EDIT?"Editing":"Edit")+(n&&!EDIT?" · "+n:"");}
function refresh(){applyAll();render();bar();}

let armT=null;
function disarm(){const u=document.getElementById("eUndo");clearTimeout(armT);armT=null;u.classList.remove("warn");u.textContent="Undo all edits";}

// capture-phase click router: runs before any card, nav or tab handler and stops them for our controls
document.addEventListener("click",ev=>{
  const t=ev.target;
  if(SUPPRESS){ev.stopImmediatePropagation();ev.preventDefault();SUPPRESS=false;return;}
  if(t.closest("#editBtn")){ev.stopImmediatePropagation();ev.preventDefault();setEdit(!EDIT);bar();return;}
  if(t.closest("#eDone")){ev.stopImmediatePropagation();setEdit(false);bar();toast(count()?"Edits saved in this browser":"Edit mode off");return;}
  if(t.closest("#eCopy")){ev.stopImmediatePropagation();copy(exportJSON(),"Edits copied, paste them to Claude");return;}
  if(t.closest("#eUndo")){ev.stopImmediatePropagation();
    if(!armT){const u=t.closest("#eUndo");u.classList.add("warn");u.textContent="Click again to undo all";armT=setTimeout(disarm,3500);return;}
    disarm();E={};persist();closeD();refresh();toast("All edits undone");return;}
  if(EDIT&&t.closest("#grid .card .pub")){ev.stopImmediatePropagation();ev.preventDefault();
    const k=t.closest(".card").dataset.k, cur=(E[k]&&E[k].pub)||null, order=[null,"r","y","g"];
    const nx=order[(order.indexOf(cur)+1)%4]; setF(k,"pub",nx); persist(); refresh();
    toast(nx?"Status: "+DOTNAME[nx]:"Status: automatic"); return;}
  const fb=t.closest(".eform button"); if(fb){ev.stopImmediatePropagation();formAct(fb);return;}
},true);

function formAct(b){
  const f=b.closest(".eform"), k=f.dataset.k, p=BYKEY[k];
  if(b.dataset.act==="orig"){delete E[k];persist();refresh();open(p.id);toast("Back to original");return;}
  const v=n=>{const el=f.querySelector(`[data-f="${n}"]`);return el?el.value:null;};
  const d=v("date"), tm=v("time");
  if(!/^2026-1[12]-\d\d$/.test(d||"")){toast("Pick a date in Nov or Dec 2026");return;}
  if(!/^\d\d:\d\d$/.test(tm||"")){toast("Pick a time");return;}
  setF(k,"date",d); setF(k,"time",tm);
  COPYF.forEach(([n])=>{const x=v(n); if(x!==null) setF(k,n,x.replace(/\r\n/g,"\n"));});
  setF(k,"pub",v("pub")||null);
  persist(); refresh(); open(p.id); toast(E[k]?"Saved":"Matches the original, edit cleared");
}

function exportJSON(){
  const out=Object.keys(E).map(k=>{const p=BYKEY[k],o=ORIG[k],e=E[k],ch={};
    for(const f in e) ch[f]=f==="pub"?DOTNAME[e[f]]:e[f];
    return {key:k,id:p.id,platform:p.platform,title:p.title,original:{date:o.date,time:o.time},changes:ch};});
  return JSON.stringify({calendar:"Halcyon content calendar",exported:new Date().toISOString(),edits:out},null,2);
}

// ---------- drag with pointer events ----------
let DRG=null, SUPPRESS=false, RAF=0;
document.addEventListener("pointerdown",ev=>{
  SUPPRESS=false;                         // a new press always starts clean
  if(!EDIT||ev.button!==0) return;
  const c=ev.target.closest("#grid .card"); if(!c||ev.target.closest(".pub")) return;
  DRG={c,x:ev.clientX,y:ev.clientY,on:false,ghost:null,tgt:null,id:ev.pointerId};
});
document.addEventListener("pointermove",ev=>{
  if(!DRG||ev.pointerId!==DRG.id) return;
  if(!DRG.on){
    if(Math.hypot(ev.clientX-DRG.x,ev.clientY-DRG.y)<6) return;
    const r=DRG.c.getBoundingClientRect(), g=DRG.c.cloneNode(true);
    g.classList.add("dghost"); g.style.setProperty("--w",r.width+"px");
    DRG.ox=DRG.x-r.left; DRG.oy=DRG.y-r.top; document.body.appendChild(g);
    DRG.ghost=g; DRG.on=true; DRG.c.classList.add("dragsrc"); document.body.classList.add("dragging");
    loop();
  }
  ev.preventDefault();
  DRG.cx=ev.clientX; DRG.cy=ev.clientY;
  DRG.ghost.style.left=(ev.clientX-DRG.ox)+"px"; DRG.ghost.style.top=(ev.clientY-DRG.oy)+"px";
  target(ev.clientX,ev.clientY);
},{passive:false});
function target(x,y){
  const el=document.elementFromPoint(x,y); let t=null;
  if(el){
    const card=el.closest("#grid .card");
    if(card&&card!==DRG.c) t=card;
    else if(!card){const d=el.closest("#grid .day[data-date]"); if(d&&!d.classList.contains("out")) t=d;}
    else { const d=card.closest(".day"); if(d&&d.dataset.date) t=d; }  // over itself: its own day
  }
  if(t!==DRG.tgt){ if(DRG.tgt) DRG.tgt.classList.remove("dropok"); DRG.tgt=t; if(t) t.classList.add("dropok"); }
}
function loop(){ // auto-scroll near the top and bottom edges
  cancelAnimationFrame(RAF);
  const step=()=>{ if(!DRG||!DRG.on) return;
    const y=DRG.cy, h=window.innerHeight, edge=70; let dy=0;
    if(y<edge) dy=-Math.ceil((edge-y)/4); else if(y>h-edge) dy=Math.ceil((y-(h-edge))/4);
    if(dy){ window.scrollBy(0,dy); target(DRG.cx,DRG.cy); }
    RAF=requestAnimationFrame(step); };
  RAF=requestAnimationFrame(step);
}
function endDrag(ev,cancel){
  if(!DRG||(ev&&ev.pointerId!==DRG.id)) return;
  const d=DRG; DRG=null; cancelAnimationFrame(RAF);
  if(!d.on) return;                       // a plain click: let it open the panel
  SUPPRESS=true; setTimeout(()=>SUPPRESS=false,350);
  d.ghost.remove(); d.c.classList.remove("dragsrc"); document.body.classList.remove("dragging");
  if(d.tgt) d.tgt.classList.remove("dropok");
  if(cancel||!d.tgt) return;
  const src=BYKEY[d.c.dataset.k];
  if(d.tgt.classList.contains("card")){
    const dst=BYKEY[d.tgt.dataset.k];
    if(!dst||dst.platform!==src.platform) return;
    const a={date:src.date,time:src.time}, b={date:dst.date,time:dst.time};
    setF(src._k,"date",b.date); setF(src._k,"time",b.time); setF(dst._k,"date",a.date); setF(dst._k,"time",a.time);
    persist(); refresh(); toast(`Swapped with ${dst.title}`);
  }else{
    const nd=d.tgt.dataset.date; if(nd===src.date) return;
    setF(src._k,"date",nd); persist(); refresh(); toast(`Moved to ${fmt(nd)}`);
  }
}
document.addEventListener("pointerup",ev=>endDrag(ev,false));
document.addEventListener("pointercancel",ev=>endDrag(ev,true));
document.addEventListener("keydown",ev=>{ if(ev.key==="Escape"&&DRG&&DRG.on){ const id=DRG.id; endDrag({pointerId:id},true); } });

// ---------- start ----------
let wasEdit=false; try{wasEdit=sessionStorage.getItem(MODEK)==="1";}catch(e){}
applyAll(); render(); setEdit(wasEdit); bar();
window.HAL_EDIT={export:exportJSON,count,edits:()=>JSON.parse(JSON.stringify(E))};
})();
