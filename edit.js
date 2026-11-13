/* Halcyon content calendar · editor (v4, 13 Nov 2026), always on
   Loads after index.html's own script and hooks grid(), open(), pubState() and fmt() from outside.
   Edit mode: move, swap, retime and recaption posts, add new posts and delete posts.
   With a GitHub token connected, every change auto-saves (2 s after the last one) by committing
   index.html, the calendar's source of truth. GitHub Pages rebuilds in about a minute. */
(function(){
"use strict";
const KEY="hal_cal_edits_v1", ADDK="hal_cal_added_v1", DELK="hal_cal_deleted_v1",
      TOKK="hal_cal_gh_token_v1", PENDK="hal_cal_pending_v1";
const REPO="gabmiren/HalcyonContentCalendar", BRANCH="main", FILE="index.html";
const MON=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const DOW7=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
const DOTNAME={r:"Not scheduled",y:"Scheduled",g:"Posted"}, PUBVAL={r:"none",y:"scheduled",g:"posted"};
const COPYF=[["caption","Caption"],["fbcap","Backup caption"]];
const STATUS=[["Ready","ok"],["To build","new"],["Needs Halcyon","dep"],["Posted","ok"]];
const ld=(k,d)=>{try{const v=JSON.parse(localStorage.getItem(k));return v==null?d:v;}catch(e){return d;}};
const sv=(k,v)=>{try{if(v==null)localStorage.removeItem(k);else localStorage.setItem(k,JSON.stringify(v));return true;}catch(e){toast("Couldn't save in this browser");return false;}};
const norm=o=>JSON.stringify(typeof o==="string"?JSON.parse(o):o);

// ---------- a save that GitHub Pages hasn't published yet ----------
let ORIGD=norm(D), PENDING=false;
const pend=ld(PENDK,null);
if(pend){
  if(norm(pend.data)===ORIGD||Date.now()-pend.t>20*60*1000) sv(PENDK,null);
  else { const nd=JSON.parse(pend.data); P.splice(0,P.length,...nd.posts); ORIGD=norm(pend.data); PENDING=true; }
}

// ---------- stable keys from each post's ORIGINAL fields ----------
function hash(s){let h=5381;for(let i=0;i<s.length;i++)h=((h<<5)+h+s.charCodeAt(i))>>>0;return h.toString(36);}
const ORIG={}, BYKEY={};
function keyOf(p){return (p.platform==="TikTok"?"tt":"ig")+"-"+p.date.replace(/-/g,"")+"-"+p.time.replace(":","")+"-"+hash(p.platform+"|"+p.title+"|"+p.date+"|"+p.time);}
P.forEach(p=>{
  const k=keyOf(p); p._k=k; BYKEY[k]=p;
  ORIG[k]={date:p.date,time:p.time,timeLabel:p.timeLabel,myt:p.myt,day:p.day,caption:p.caption||"",fbcap:p.fbcap||""};
});

// ---------- storage: edits (E), added posts (A), deleted keys (X) ----------
let E=ld(KEY,{})||{}, A=ld(ADDK,[])||[], X=new Set(ld(DELK,[])||[]);
for(const k in E) if(!BYKEY[k]) delete E[k];
X.forEach(k=>{if(!BYKEY[k])X.delete(k);});
A.forEach(p=>{p._new=true; BYKEY[p._k]=p; P.push(p);});
X.forEach(k=>{const i=P.indexOf(BYKEY[k]); if(i>-1)P.splice(i,1);});
function persist(quiet){sv(KEY,E);sv(ADDK,A.map(strip));sv(DELK,[...X]);if(!quiet)schedule();}
function strip(p){const o={};for(const f in p)if(f[0]!=="_"||f==="_k")o[f]=p[f];return o;}
const nEd=()=>Object.keys(E).length, total=()=>nEd()+A.length+X.size;
const dirty=()=>norm(bakeData())!==ORIGD;

function setF(k,f,v){
  const p=BYKEY[k];
  if(p._new){ if(f==="pub") p._pub=v; else p[f]=v; return; }
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
    if(p._new){ p.timeLabel=etLabel(p.time); p.myt=mytLabel(p.date,p.time); return; }
    const o=ORIG[p._k], e=E[p._k]||{};
    p.date=e.date||o.date; p.time=e.time||o.time;
    p.caption=("caption" in e)?e.caption:o.caption;
    if(o.fbcap||("fbcap" in e)) p.fbcap=("fbcap" in e)?e.fbcap:o.fbcap;
    if(e.time||e.date){ p.timeLabel=etLabel(p.time); p.myt=mytLabel(p.date,p.time); }
    else { p.timeLabel=o.timeLabel; p.myt=o.myt; }
    p.day=o.day;
  });
  // keep TikTok "Post N" in date order once a TikTok has moved, been added or deleted
  const tt=p=>p.platform==="TikTok";
  if(P.some(p=>tt(p)&&(p._new||(E[p._k]&&(E[p._k].date||E[p._k].time))))||[...X].some(k=>tt(BYKEY[k]))){
    P.filter(tt).sort((a,b)=>(a.date+a.time).localeCompare(b.date+b.time)).forEach((p,i)=>p.day="Post "+(i+1));
  }
  P.filter(p=>p._new&&!tt(p)).forEach(p=>p.day=p.day||"Post");
}

// ---------- hooks into the page ----------
const _grid=grid, _open=open, _pub=pubState;
fmt=function(iso){const x=dt(iso);return DOW[(x.getUTCDay()+6)%7]+" "+x.getUTCDate()+" "+MON[x.getUTCMonth()];};
pubState=function(p){
  if(p._new&&p._pub) return [p._pub,DOTNAME[p._pub]];
  const e=E[p._k]; if(e&&e.pub) return [e.pub,DOTNAME[e.pub]];
  if(p.pub==="none") return ["r","Not scheduled"];
  return _pub(p);
};
grid=function(){
  _grid();
  let mi=-1, prev=99;
  document.querySelectorAll("#grid .day:not(.pad)").forEach(d=>{
    const n=+d.querySelector(".dn b").textContent; if(n<prev) mi++; prev=n;
    const [y,m]=MONTHS[mi]; d.dataset.date=y+"-"+pad(m+1)+"-"+pad(n);
    if(!d.classList.contains("out")) d.querySelector(".dn").insertAdjacentHTML("beforeend",`<button class="addp" type="button" data-date="${d.dataset.date}" title="Add a post on this day" aria-label="Add a post">+</button>`);
  });
  document.querySelectorAll("#grid .card").forEach(c=>{
    const p=P.find(x=>x.id===c.dataset.id); if(!p) return;
    c.dataset.k=p._k;
    const tag=p._new?"New":(E[p._k]?"Edited":"");
    if(tag){ c.classList.add("ed"); const t=c.querySelector(".t"); if(t&&!c.querySelector(".edt")) t.insertAdjacentHTML("beforebegin",`<span class="edt">${tag}</span>`); }
    if((E[p._k]&&E[p._k].pub)||(p._new&&p._pub)){ const d=c.querySelector(".pub"); if(d) d.classList.add("man"); }
  });
};
open=function(id){
  const p=P.find(x=>x.id===id); if(!p) return;
  if((p._new||/^N/.test(p.id))&&EDIT){ postForm(p); return; }
  _open(id);
  if(!EDIT) return;
  const e=E[p._k]||{}, o=ORIG[p._k];
  const st=e.pub?DOTNAME[e.pub]:"Automatic ("+_pub(p)[1].toLowerCase()+")";
  const tx=COPYF.filter(([f])=>f==="caption"||o[f]).map(([f,lab])=>`<label class="efl">${lab}${(f in e)?' <span class="edt">Edited</span>':""}<textarea data-f="${f}" rows="${f==="caption"?9:5}">${esc(p[f]||"")}</textarea></label>`).join("");
  const html=`<div class="eform" data-k="${p._k}">
    <div class="lab" style="color:var(--c)">Edit this post</div>
    <div class="erow"><label class="efl">Date<input type="date" data-f="date" value="${p.date}" min="2026-11-01" max="2026-12-31"></label>
    <label class="efl">Time (ET)<input type="time" data-f="time" value="${p.time}" step="300"></label>
    <label class="efl">Status dot<select data-f="pub"><option value="">Automatic</option><option value="r">Not scheduled</option><option value="y">Scheduled</option><option value="g">Posted</option></select></label></div>
    ${tx}
    <div class="ebtns"><button class="btn" data-act="save">Save</button><button class="ebtn" data-act="orig"${E[p._k]?"":" disabled"}>Back to original</button><button class="ebtn del" data-act="del">Delete post</button><span class="enote">Now: ${esc(st)}${E[p._k]?" · original "+fmt(o.date)+", "+esc(o.timeLabel):""}</span></div>
  </div>`;
  document.querySelector("#dr h2").insertAdjacentHTML("afterend",html);
  document.querySelector('.eform select[data-f="pub"]').value=e.pub||"";
};

// ---------- add / edit form for new posts ----------
function postForm(p,date){
  const isNew=!p, q=p||{platform:plat,date:date||defDate(),time:"07:00",title:"",pillar:"Entertainment",format:"",status:"To build",caption:"",why:"",todo:[]};
  const base=q.status.split(" · ")[0], extra=q.status.includes(" · ")?q.status.split(" · ").slice(1).join(" · "):"";
  const opt=(arr,v)=>arr.map(x=>`<option${x===v?" selected":""}>${esc(x)}</option>`).join("");
  $("#dr").innerHTML=`<button class="x" onclick="closeD()">Close</button>
  <div class="lab">${isNew?"New post":"New post · added on this page"}</div>
  <h2>${isNew?"Add a post":esc(q.title)}</h2>
  <div class="eform nform" data-k="${isNew?"":q._k}">
    <div class="erow"><label class="efl">App<select data-f="platform">${opt(["TikTok","Instagram"],q.platform)}</select></label>
    <label class="efl">Date<input type="date" data-f="date" value="${q.date}" min="2026-11-01" max="2026-12-31"></label>
    <label class="efl">Time (ET)<input type="time" data-f="time" value="${q.time}" step="300"></label></div>
    <label class="efl">Title<input type="text" data-f="title" value="${esc(q.title)}" placeholder="What the post is"></label>
    <div class="erow"><label class="efl">Pillar<select data-f="pillar">${opt(Object.keys(D.pil),q.pillar)}</select></label>
    <label class="efl">Status<select data-f="status">${opt(STATUS.map(s=>s[0]),base)}</select></label>
    <label class="efl">Status note<input type="text" data-f="snote" value="${esc(extra)}" placeholder="e.g. Mon 16"></label></div>
    <label class="efl">Format<input type="text" data-f="format" value="${esc(q.format)}" placeholder="e.g. Meme · 12 s"></label>
    <label class="efl">Caption<textarea data-f="caption" rows="8">${esc(q.caption)}</textarea></label>
    <label class="efl">Why here<textarea data-f="why" rows="3">${esc(q.why)}</textarea></label>
    <label class="efl">To do (one per line)<textarea data-f="todo" rows="3">${esc((q.todo||[]).join("\n"))}</textarea></label>
    <div class="ebtns"><button class="btn" data-act="nsave">${isNew?"Add post":"Save"}</button>${isNew?"":`<button class="ebtn del" data-act="del">Delete post</button>`}<span class="enote">Video or slides get attached when Claude bakes it in.</span></div>
  </div>`;
  $("#dr").classList.add("on");$("#ov").classList.add("on");$("#dr").scrollTop=0;
}
function defDate(){const t=new Date(),d=t.getFullYear()+"-"+pad(t.getMonth()+1)+"-"+pad(t.getDate());return d<"2026-11-01"?"2026-11-01":d>"2026-12-31"?"2026-12-31":d;}
function saveNew(f){
  const v=n=>{const el=f.querySelector(`[data-f="${n}"]`);return el?el.value.replace(/\r\n/g,"\n"):"";};
  const d=v("date"), tm=v("time"), title=v("title").trim();
  if(!title){toast("Give the post a title");return;}
  if(!/^2026-1[12]-\d\d$/.test(d)){toast("Pick a date in Nov or Dec 2026");return;}
  if(!/^\d\d:\d\d$/.test(tm)){toast("Pick a time");return;}
  const st=v("status"), sc=STATUS.find(s=>s[0]===st)[1], note=v("snote").trim();
  let p=f.dataset.k?BYKEY[f.dataset.k]:null;
  if(!p){ const id="N"+Date.now().toString(36); p={id,_k:"new-"+id,_new:true,dep:null,fb:null,fbcap:null,fbimg:null,videos:[],slides:[],reel:null,story:null,extra:null,ctx:"",src:"Added on the page",day:""}; A.push(p); BYKEY[p._k]=p; P.push(p); }
  Object.assign(p,{platform:v("platform"),date:d,time:tm,title,pillar:v("pillar"),format:v("format").trim()||"New post",
    status:st+(note?" · "+note:""),scls:sc,caption:v("caption"),why:v("why").trim(),todo:v("todo").split("\n").map(s=>s.trim()).filter(Boolean)});
  if(st==="Posted") p.pub="posted"; else delete p.pub;
  persist(); if(p.platform!==plat){plat=p.platform;try{localStorage.setItem("hal_cal2_plat",plat)}catch(e){}}
  refresh(); closeD(); toast(f.dataset.k?"Saved":"Post added to "+fmt(d));
}
function delPost(k){
  const p=BYKEY[k]; if(!p) return;
  if(p._new){ A=A.filter(x=>x!==p); delete BYKEY[k]; }
  else { delete E[k]; X.add(k); }
  const i=P.indexOf(p); if(i>-1)P.splice(i,1);
  persist(); closeD(); refresh(); toast("Deleted "+p.title);
}

// ---------- save to GitHub ----------
function bakeData(){
  const d=JSON.parse(ORIGD);
  d.posts=P.map(p=>{const o={};for(const f in p)if(f[0]!=="_")o[f]=p[f];
    const e=E[p._k]; if(e&&e.pub) o.pub=PUBVAL[e.pub]; if(p._new&&p._pub) o.pub=PUBVAL[p._pub];
    return o;});
  return d;
}
const b64dec=s=>new TextDecoder().decode(Uint8Array.from(atob(s.replace(/\n/g,"")),c=>c.charCodeAt(0)));
function b64enc(str){const b=new TextEncoder().encode(str);let s="";for(let i=0;i<b.length;i+=0x8000)s+=String.fromCharCode.apply(null,b.subarray(i,i+0x8000));return btoa(s);}
async function gh(path,opt,tok){
  const r=await fetch("https://api.github.com/repos/"+REPO+path,Object.assign({},opt,{headers:{"Accept":"application/vnd.github+json","Authorization":"Bearer "+tok,"Content-Type":"application/json"}}));
  const j=await r.json().catch(()=>({})); if(!r.ok){const e=new Error(j.message||("HTTP "+r.status));e.status=r.status;throw e;} return j;
}
function tokenForm(msg){
  $("#dr").innerHTML=`<button class="x" onclick="closeD()">Close</button>
  <div class="lab">Save to GitHub</div><h2>Turn on auto-save</h2>
  ${msg?`<div class="box">${esc(msg)}</div>`:""}
  <p style="color:var(--ink2);font-size:14px;line-height:1.6">Once this is on, every change saves itself to the calendar repo a couple of seconds after you make it, so every device sees it. It needs a GitHub token, made once:</p>
  <ol style="color:var(--ink2);font-size:14px;line-height:1.7;padding-left:20px">
   <li>Open <a href="https://github.com/settings/personal-access-tokens/new" target="_blank" rel="noopener" style="color:var(--c)">GitHub, new fine-grained token</a>.</li>
   <li>Repository access: only <b>HalcyonContentCalendar</b>.</li>
   <li>Permissions: <b>Contents</b> set to Read and write. Nothing else.</li>
   <li>Generate it, then paste it below.</li></ol>
  <div class="eform"><label class="efl">Token<input type="password" id="ghTok" placeholder="github_pat_..." autocomplete="off"></label>
  <div class="ebtns"><button class="btn" data-act="tok">Turn on auto-save</button><span class="enote">Kept in this browser only.</span></div></div>`;
  $("#dr").classList.add("on");$("#ov").classList.add("on");$("#dr").scrollTop=0;
}
let SAVING=false, AGAIN=false, TMR=null, BLOCKED=false, STATE="";
function schedule(){ if(BLOCKED) return; clearTimeout(TMR); if(!ld(TOKK,null)){bar();return;} STATE="waiting"; bar(); TMR=setTimeout(saveGH,2000); }
function rebase(snap){
  ORIGD=norm(snap);
  P.forEach(p=>{const e=E[p._k]; if(e&&e.pub) p.pub=PUBVAL[e.pub]; if(p._new&&p._pub) p.pub=PUBVAL[p._pub]; delete p._new; delete p._pub;});
  E={}; A=[]; X=new Set();
  for(const k in BYKEY) delete BYKEY[k]; for(const k in ORIG) delete ORIG[k];
  P.forEach(p=>{const k=keyOf(p); p._k=k; BYKEY[k]=p; ORIG[k]={date:p.date,time:p.time,timeLabel:p.timeLabel,myt:p.myt,day:p.day,caption:p.caption||"",fbcap:p.fbcap||""};});
  persist(true);
}
async function saveGH(manual){
  clearTimeout(TMR);
  if(SAVING){AGAIN=true;return;}
  if(BLOCKED&&!manual) return;
  if(!dirty()){ if(manual) toast("Everything is already saved"); STATE=""; bar(); return; }
  const tok=ld(TOKK,null); if(!tok){tokenForm();return;}
  SAVING=true; AGAIN=false; STATE="saving"; bar();
  const snap=bakeData();
  try{
    let cur=null, html, lines, i;
    for(let n=0;n<4;n++){ // GitHub's API can lag a moment right after our own commit
      cur=await gh("/contents/"+FILE+"?ref="+BRANCH+"&t="+Date.now(),{method:"GET",cache:"no-store"},tok);
      html=b64dec(cur.content); lines=html.split("\n"); i=lines.findIndex(l=>l.startsWith("const D = "));
      if(i<0) throw new Error("Couldn't find the calendar data in index.html");
      if(norm(lines[i].slice(10).replace(/;\s*$/,""))===ORIGD) break;
      if(n===3){ BLOCKED=true; STATE="conflict"; bar();
        finishMsg("The calendar on GitHub changed after this page loaded, so auto-save has paused. Reload the page; your changes stay in this browser and save again after the reload.",true); return; }
      await new Promise(r=>setTimeout(r,1500));
    }
    lines[i]="const D = "+JSON.stringify(snap)+";";
    const parts=[];if(nEd())parts.push(nEd()+" edited");if(A.length)parts.push(A.length+" added");if(X.size)parts.push(X.size+" deleted");
    await gh("/contents/"+FILE,{method:"PUT",body:JSON.stringify({message:"Calendar auto-save from the page"+(parts.length?": "+parts.join(", "):""),content:b64enc(lines.join("\n")),sha:cur.sha,branch:BRANCH})},tok);
    sv(PENDK,{data:JSON.stringify(snap),t:Date.now()});
    rebase(snap); STATE="saved"; finishMsg("",false);
    document.getElementById("emsg").className="emsg";
    applyAll(); render();
  }catch(err){
    if(err.status===401||err.status===403||err.status===404){sv(TOKK,null);STATE="";tokenForm("GitHub didn't accept that token ("+err.message+"). Make a new one with Contents read and write on HalcyonContentCalendar.");}
    else if(err.status===409){AGAIN=true;}
    else {STATE="error"; finishMsg("Couldn't save: "+err.message+". Your changes are kept in this browser; tap Save now to retry.",true);}
  }finally{SAVING=false; bar(); if(AGAIN||(!BLOCKED&&STATE==="saved"&&dirty())) schedule();}
}
function finishMsg(t,bad){const n=document.getElementById("emsg");n.textContent=t;n.className="emsg on"+(bad?" bad":"");}

// ---------- styles ----------
document.head.insertAdjacentHTML("beforeend",`<style>
.hdr-r{display:flex;align-items:center;gap:10px}
.ebar{position:sticky;top:0;z-index:9;display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 14px;padding:10px 14px;background:rgba(14,20,24,.96);border:1px solid rgba(0,251,244,.45);border-radius:12px;box-shadow:0 0 24px rgba(0,251,244,.08);backdrop-filter:blur(6px)}
body.editing .ebar{display:flex}
.ebar .n{font-weight:600;font-size:14px;margin-right:auto}.ebar .n i{font-style:normal;color:var(--c)}
.ebar .hint{font-size:12px;color:var(--ink3);flex-basis:100%;order:9}
.sstat{font-size:12.5px;color:var(--ink3)}.sstat.saving,.sstat.waiting{color:var(--ink2)}.sstat.error,.sstat.conflict{color:#ff8fa3}
.emsg{display:none;flex-basis:100%;order:8;font-size:13px;color:var(--c);padding:6px 0 0}.emsg.on{display:block}.emsg.bad{color:#ff8fa3}
.pendb{margin:0 0 14px;padding:10px 14px;border:1px dashed rgba(0,251,244,.45);border-radius:12px;font-size:13px;color:var(--ink2)}
.ebtn{background:transparent;border:1px solid #2b3a41;color:var(--ink);font:500 13px Poppins,sans-serif;padding:7px 14px;border-radius:999px;cursor:pointer}
.ebtn:hover{border-color:var(--c);color:var(--c)}.ebtn[disabled]{opacity:.4;cursor:default;border-color:#2b3a41;color:var(--ink)}
.ebtn.warn,.ebtn.del{border-color:#ff5a6e;color:#ff8fa3}.ebtn.del.warn{background:#ff5a6e;color:#1a0005}
.day .dn{position:relative}
.addp{position:absolute;right:0;top:-2px;width:26px;height:26px;border-radius:50%;background:transparent;border:1px solid rgba(0,251,244,.3);color:var(--ink3);font:500 17px/1 Poppins,sans-serif;cursor:pointer;padding:0;opacity:.55;transition:opacity .15s}
.day:hover .addp,.addp:focus{opacity:1}.addp:hover{border-color:var(--c);color:var(--c)}
@media (hover:none){.addp{opacity:.8}}
body.editing .card{user-select:none;-webkit-user-select:none;-webkit-touch-callout:none}
@media (pointer:fine){body.editing .card{cursor:grab}}
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
@media (max-width:600px){.erow{grid-template-columns:1fr}.ebar{position:static;padding:8px 12px;gap:8px}.ebar .hint{display:none}}
</style>`);

// ---------- header button and edit bar ----------
document.querySelector("#v-cal").insertAdjacentHTML("afterbegin",`${PENDING?`<div class="pendb">Showing your last save while GitHub Pages updates. This note goes away once the live page has it.</div>`:""}<div class="ebar" id="ebar">
  <span class="n" id="ecount"></span>
  <button class="ebtn" id="eAdd" type="button">+ Add post</button>
  <button class="ebtn" id="eCopy" type="button">Copy my edits</button>
  <button class="ebtn" id="eUndo" type="button">Undo all</button>
  <span class="sstat" id="sstat"></span><button class="btn" id="eSave" type="button">Save now</button>
  <span class="emsg" id="emsg"></span>
  <span class="hint">Drag a post to another day to move it, or onto another post to swap (on a phone, press and hold first). Tap a dot to change its status. Tap a post to edit or delete it. Tap + on any day to add one.</span>
</div>`);

const EDIT=true; document.body.classList.add("editing");
function disarm(){const u=document.getElementById("eUndo");clearTimeout(armT);armT=null;u.classList.remove("warn");u.textContent="Undo all";}
let armT=null, armDel=null;
function bar(){
  const tok=!!ld(TOKK,null), d=dirty(), st=document.getElementById("sstat"), sb=document.getElementById("eSave");
  const parts=[];if(nEd())parts.push(`<i>${nEd()}</i> edited`);if(A.length)parts.push(`<i>${A.length}</i> added`);if(X.size)parts.push(`<i>${X.size}</i> deleted`);
  document.getElementById("ecount").innerHTML=tok?"Auto-save on":(parts.length?parts.join(" · ")+" · not saved yet":"Auto-save off");
  st.className="sstat "+(STATE||"");
  st.textContent=!tok?"":STATE==="saving"?"Saving…":STATE==="waiting"?"Saving in a moment…":STATE==="conflict"?"Paused, reload the page":STATE==="error"?"Not saved":d?"Unsaved changes":"All changes saved";
  sb.textContent=tok?"Save now":"Turn on auto-save"; sb.disabled=SAVING||(tok&&!d&&STATE!=="error");
  sb.style.display=(tok&&!d&&STATE!=="error")?"none":"";
  document.getElementById("eCopy").disabled=!total(); document.getElementById("eUndo").disabled=!total();
  const lc=!tok&&total(); document.getElementById("eCopy").style.display=document.getElementById("eUndo").style.display=lc?"":"none";
}
function refresh(){applyAll();render();bar();}


document.addEventListener("click",ev=>{
  const t=ev.target;
  if(SUPPRESS){ev.stopImmediatePropagation();ev.preventDefault();SUPPRESS=false;return;}
  if(t.closest("#eSave")){ev.stopImmediatePropagation();if(!ld(TOKK,null))tokenForm();else saveGH(true);return;}
  if(t.closest("#eAdd")){ev.stopImmediatePropagation();postForm(null);return;}
  if(EDIT&&t.closest(".addp")){ev.stopImmediatePropagation();ev.preventDefault();postForm(null,t.closest(".addp").dataset.date);return;}
  if(t.closest("#eCopy")){ev.stopImmediatePropagation();copy(exportJSON(),"Edits copied, paste them to Claude");return;}
  if(t.closest("#eUndo")){ev.stopImmediatePropagation();
    if(!armT){const u=t.closest("#eUndo");u.classList.add("warn");u.textContent="Click again to undo all";armT=setTimeout(disarm,3500);return;}
    disarm();sv(KEY,null);sv(ADDK,null);sv(DELK,null);toast("All changes undone");setTimeout(()=>location.reload(),400);return;}
  if(EDIT&&t.closest("#grid .card .pub")){ev.stopImmediatePropagation();ev.preventDefault();
    const k=t.closest(".card").dataset.k, p=BYKEY[k], cur=p._new?(p._pub||null):((E[k]&&E[k].pub)||null), order=[null,"r","y","g"];
    const nx=order[(order.indexOf(cur)+1)%4]; setF(k,"pub",nx); persist(); refresh();
    toast(nx?"Status: "+DOTNAME[nx]:"Status: automatic"); return;}
  if(t.closest('[data-act="tok"]')){ev.stopImmediatePropagation();const v=(document.getElementById("ghTok").value||"").trim();
    if(!v){toast("Paste the token first");return;} sv(TOKK,v); closeD(); toast("Auto-save is on"); saveGH(true); return;}
  const fb=t.closest(".eform button"); if(fb){ev.stopImmediatePropagation();formAct(fb);return;}
},true);

function formAct(b){
  const f=b.closest(".eform"), k=f.dataset.k, act=b.dataset.act;
  if(act==="nsave"){saveNew(f);return;}
  if(act==="del"){
    if(armDel!==b){armDel=b;b.classList.add("warn");b.textContent="Click again to delete";setTimeout(()=>{if(armDel===b){armDel=null;b.classList.remove("warn");b.textContent="Delete post";}},3500);return;}
    armDel=null; delPost(k); return;}
  const p=BYKEY[k];
  if(act==="orig"){delete E[k];persist();refresh();open(p.id);toast("Back to original");return;}
  const v=n=>{const el=f.querySelector(`[data-f="${n}"]`);return el?el.value:null;};
  const d=v("date"), tm=v("time");
  if(!/^2026-1[12]-\d\d$/.test(d||"")){toast("Pick a date in Nov or Dec 2026");return;}
  if(!/^\d\d:\d\d$/.test(tm||"")){toast("Pick a time");return;}
  setF(k,"date",d); setF(k,"time",tm);
  COPYF.forEach(([n])=>{const x=v(n); if(x!==null) setF(k,n,x.replace(/\r\n/g,"\n"));});
  setF(k,"pub",v("pub")||null);
  persist(); refresh(); open(p.id); toast(E[k]?"Saved in this browser":"Matches the original, edit cleared");
}

function exportJSON(){
  const ed=Object.keys(E).map(k=>{const p=BYKEY[k],o=ORIG[k],e=E[k],ch={};
    for(const f in e) ch[f]=f==="pub"?DOTNAME[e[f]]:e[f];
    return {key:k,id:p.id,platform:p.platform,title:p.title,original:{date:o.date,time:o.time},changes:ch};});
  const ad=A.map(p=>{const o=strip(p);delete o._k;return o;});
  const de=[...X].map(k=>({key:k,id:BYKEY[k].id,platform:BYKEY[k].platform,title:BYKEY[k].title,date:ORIG[k].date}));
  return JSON.stringify({calendar:"Halcyon content calendar",exported:new Date().toISOString(),edits:ed,added:ad,deleted:de},null,2);
}

// ---------- drag with pointer events ----------
let DRG=null, SUPPRESS=false, RAF=0;
function startGhost(){
  const r=DRG.c.getBoundingClientRect(), g=DRG.c.cloneNode(true);
  g.classList.add("dghost"); g.style.setProperty("--w",r.width+"px");
  DRG.ox=DRG.x-r.left; DRG.oy=DRG.y-r.top; document.body.appendChild(g);
  g.style.left=(DRG.x-DRG.ox)+"px"; g.style.top=(DRG.y-DRG.oy)+"px";
  DRG.ghost=g; DRG.on=true; DRG.c.classList.add("dragsrc"); document.body.classList.add("dragging");
  DRG.cx=DRG.x; DRG.cy=DRG.y; target(DRG.x,DRG.y); loop();
}
document.addEventListener("pointerdown",ev=>{
  SUPPRESS=false;
  if(ev.button!==0) return;
  const c=ev.target.closest("#grid .card"); if(!c||ev.target.closest(".pub")) return;
  DRG={c,x:ev.clientX,y:ev.clientY,on:false,ghost:null,tgt:null,id:ev.pointerId,touch:ev.pointerType!=="mouse"};
  if(DRG.touch){ const d=DRG; d.lt=setTimeout(()=>{ if(DRG!==d) return; if(navigator.vibrate)navigator.vibrate(12); startGhost(); },380); }
});
document.addEventListener("pointermove",ev=>{
  if(!DRG||ev.pointerId!==DRG.id) return;
  if(!DRG.on){
    const far=Math.hypot(ev.clientX-DRG.x,ev.clientY-DRG.y);
    if(DRG.touch){ if(far>8){clearTimeout(DRG.lt);DRG=null;} return; }  // a swipe: let the page scroll
    if(far<6) return;
    startGhost();
  }
  ev.preventDefault();
  DRG.cx=ev.clientX; DRG.cy=ev.clientY;
  DRG.ghost.style.left=(ev.clientX-DRG.ox)+"px"; DRG.ghost.style.top=(ev.clientY-DRG.oy)+"px";
  target(ev.clientX,ev.clientY);
},{passive:false});
document.addEventListener("touchmove",ev=>{ if(DRG&&DRG.on) ev.preventDefault(); },{passive:false});
document.addEventListener("contextmenu",ev=>{ if(ev.target.closest&&ev.target.closest("#grid .card")) ev.preventDefault(); });
function target(x,y){
  const el=document.elementFromPoint(x,y); let t=null;
  if(el){
    const card=el.closest("#grid .card");
    if(card&&card!==DRG.c) t=card;
    else if(!card){const d=el.closest("#grid .day[data-date]"); if(d&&!d.classList.contains("out")) t=d;}
    else { const d=card.closest(".day"); if(d&&d.dataset.date) t=d; }
  }
  if(t!==DRG.tgt){ if(DRG.tgt) DRG.tgt.classList.remove("dropok"); DRG.tgt=t; if(t) t.classList.add("dropok"); }
}
function loop(){
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
  const d=DRG; DRG=null; cancelAnimationFrame(RAF); clearTimeout(d.lt);
  if(!d.on) return;
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
applyAll(); render(); bar();
window.HAL_EDIT={export:exportJSON,count:total,bake:bakeData};
})();
