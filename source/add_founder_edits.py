"""One-off: add the 10 founder edits from the Drive "Edits" folder (15 Nov 2026) to the calendar, 20 Nov to 6 Dec.
Nothing existing is removed or moved."""
import re,json,datetime
f='index.html'; s=open(f).read()
m=re.search(r'^const D = (\{.*\});\s*$',s,re.M)
D=json.loads(m.group(1)); P=D['posts']
assert not any(p['id'] in ('T21','R19') for p in P), 'already added'
DISC="Halcyon offers simulated educational accounts. Results not guaranteed. T&C apply."
DR="https://drive.google.com/file/d/%s/view"
CLIP={
 '03':dict(fid='1cCkjRIaAi2fidUg0bF0SxdYYDcpoQNkO',file='Halcyon 03 - I Want To Quit Every Day.mp4',len='46 s',title='I want to walk away from trading every day',pillar='Entertainment',
   card='I want to walk away from trading every day',status='Ready',
   todo=["Founder edit from the Drive Edits folder, 1440 x 2560, Halcyon logo under the footage","The cash B-roll at about 16 to 24 s is stock $100-bill footage, which the brand avoids. Ask the editor to swap it for a brand card if there's time; fine to post as is"],
   why="The most relatable of the ten edits, and a feeling every trader knows. It's psychology with no rules or prices in it, so nothing needs sign-off, which makes it the right one to open the set."),
 '06':dict(fid='1QKFRITHi7tucmkfVWAFkTt8kuql0ZLQN',file='Halcyon 06 - I Laugh At No Indicator Traders.mp4',len='50 s',title='I laugh when traders say they use no indicators',pillar='Education',status='Ready',
   todo=["Founder edit from the Drive Edits folder","Part 1 of 2 with the 9 EMA clip, which reuses about 25 s of this footage. Reply to comments asking about the 9 EMA with a pointer to Part 2"],
   why="A contrarian opinion with a practical answer inside it (the 9 EMA), the kind of take that gets people arguing in the comments, which we need on both apps."),
 '61':dict(fid='1_bC9Pr86Yzzd09j1QBw9LnB0UTVzrNtL',file='Halcyon 6.1 - Why the 9 EMA.mp4',len='43 s',title='9 EMA is all you need',pillar='Education',status='Ready',
   todo=["Founder edit from the Drive Edits folder","Part 2 of the indicators clip: about the first 25 s repeat Part 1, then Steve adds the slope (incline, decline, flat). Post it after Part 1 on each app"],
   why="Part 2 of Sunday's indicators clip, so it follows Part 1 while it's fresh and answers the obvious question: how do you use the 9 EMA?"),
 '09':dict(fid='1G7awMmb7vcdij55PZvJN_JnSjZhAMimg',file='Halcyon 09 - Never Move To Break Even.mp4',len='44 s',title='Stop moving to break even',pillar='Education',status='Ready',
   todo=["Founder edit from the Drive Edits folder, with chart B-roll"],
   why="A risk habit almost every trader has an opinion on, told as Steve's own rule. It sits after the drawdown posts and before Saturday's two-accounts explainer, so the risk thread runs through the week."),
 '05':dict(fid='1_I5O1E38jijgO-bSm1z7SRdc8OgcRjeM',file='Halcyon 05 - Indicator Tier List.mp4',len='87 s',title="Our founder's indicator tier list",pillar='Entertainment',status='Ready',
   todo=["Founder edit from the Drive Edits folder. Tier list: S EMAs, support and resistance; A MACD, volume profile; B fair value gaps; D order flow; F Fibonacci","87 s is the longest of the set and twice our usual length. Ask the editor for a 45 to 60 s cut if there's time","The S to F badges use green, yellow, orange and red, outside the one-accent palette. Fine for a tier list, but note it for the next edit"],
   why="Tier lists invite disagreement, and Fibonacci at F is the kind of call people comment on. It follows the two indicator clips, so it lands with viewers who already know Steve's view."),
 '11':dict(fid='1JtZ1v98Bdw3KfDkwnfpBL7ouy7W_RYsS',file='Halcyon 11 - Why I Started Halcyon.mp4',len='58 s',title='Why I started my own prop firm',pillar='Promo',status='Needs Halcyon',
   dep="Halcyon confirms Steve's lines about a path to live trading and allocation (\"take you live and give you allocation\", \"go live sooner than later\") are accurate for current accounts, by {d}",
   todo=["Founder edit from the Drive Edits folder","Steve says traders get \"payout after payout\" elsewhere and that Halcyon gives \"a path to live\". The caption leaves the live path out until Halcyon confirms it"],
   why="The brand story in Steve's words, and the clip that explains why Halcyon exists. It opens the last week once the earlier clips have introduced him."),
 '10':dict(fid='1lIFrFeBESpLX0ZbdDxc_S0wRTmR5SYn0',file='Halcyon 10 - First Eval Controversial.mp4',len='49 s',title='Buying your first eval? Listen up',pillar='Education',status='Needs Halcyon',
   dep="Halcyon confirms the activation-fee model Steve recommends is still sold, and that \"way cheaper\" is fine to say, by {d}",
   todo=["Founder edit from the Drive Edits folder","Steve recommends the activation-fee model and a trailing drawdown for new traders, and says end of day accounts exist. Ties to the Lite question still open with Halcyon"],
   why="Practical advice for someone about to buy, which follows the founder story and the \"check this before you buy\" explainer from Mon 23."),
 '08':dict(fid='1SA3EZAtLi9SohDkMTn9hvlX9jv9xJ__O',file='Halcyon 08 - Never denied a payout.mp4',len='24 s',title='Has a payout ever been denied?',pillar='Promo',status='Needs Halcyon',
   dep="Halcyon (and counsel) approve Steve's line \"we've never denied a single payout\", which opens and closes the clip, by {d}",
   todo=["Founder edit from the Drive Edits folder","\"Never denied a single payout\" is an absolute claim. It needs written sign-off before it goes out. The caption only describes the automatic and manual review process"],
   why="The question every trader asks a new prop firm, answered in 24 seconds. It's a trust post, so it goes out once Halcyon has signed off the claim."),
 '01':dict(fid='1wDSPHNwYnP_I3QgcMTWAK7v43A9aeWYf',file='Halcyon 01 - Worst Trade Ever.mp4',len='56 s',title='Even founders take bad trades',pillar='Entertainment',status='Needs Halcyon',
   dep="Halcyon OKs the burned-in \"$180,000\" loss (said twice, and the biggest number on screen) and the penny-stock story, by {d}",
   todo=["Founder edit from the Drive Edits folder","\"$180,000\" is a dollar loss shown as the largest text on screen, which our rules keep off frames. Ask Halcyon whether to keep it, or ask the editor to cut the figure from the captions","The trade was a stock, not futures. The caption keeps that clear"],
   why="The strongest hook in the set: the founder's own worst trade. It takes Saturday's best slot."),
 '12':dict(fid='11QK21Go2zUk4zPVq0dvx6HTJnMD20FWI',file='Halcyon 12 - Greed Kills Traders.mp4',len='38 s',title="You're a bad trader because of this",pillar='Education',status='Needs Halcyon',
   dep="Halcyon approves, or the editor cuts, the dollar maths in the clip (\"$300 in a day\", then \"over 10 days that's $2,000, $3,000\"), by {d}",
   todo=["Founder edit from the Drive Edits folder","The clip frames income in dollars ($300 a day, $2,000 to $3,000 over 10 days), which breaks the no-dollar-earnings rule. Best fix: the editor cuts 30.4 to 35 s and keeps the \"take the profit\" message"],
   why="Greed is the most common trading psychology topic, and this closes the set on a lesson. It's last so there's time for the recut."),
}
def myt(d,t):
    h,mi=map(int,t.split(':')); x=datetime.datetime.fromisoformat(d)+datetime.timedelta(hours=h+13,minutes=mi)
    return f"{x.strftime('%-I:%M %p')} {x.strftime('%a')} {x.day} {x.strftime('%b')} MYT"
def tl(t): h,mi=map(int,t.split(':')); return datetime.time(h,mi).strftime('%-I:%M %p')+' ET'
def wd(d): x=datetime.date.fromisoformat(d); return f"{x.strftime('%a')} {x.day}"
def post(pid,plat,key,date,time,caption,ctx,why_extra,fb=None):
    c=CLIP[key]; dep=c.get('dep'); 
    return {"id":pid,"platform":plat,"date":date,"time":time,"timeLabel":tl(time),"myt":myt(date,time),"day":"Post" if plat=='TikTok' else "Reel",
      "title":c['title'],"pillar":c['pillar'],"format":("Founder clip · talking head with captions · " if plat=='TikTok' else "Reel · founder clip · ")+c['len'],
      "src":"Founder edit · "+c['file']+" (Drive, Edits folder)","status":c['status'],"scls":"dep" if dep else "new","ctx":ctx,
      "why":c['why']+(" "+why_extra if why_extra else ""),"todo":list(c['todo']),"dep":dep,"fb":fb,"fbcap":None,"fbimg":None,
      "caption":caption,"videos":[{"src":DR%c['fid'],"label":"Watch in Drive · "+c['file'],"drive":True}],"slides":[],"reel":None,"story":None,"extra":None,"pub":"none"}
skip=["Skip it","Week 3 has no other posts yet, so if it isn't cleared, the next fortnight's plan fills the day."]
# deadlines: two working days before the earliest post of each clip
DL={'11':'Wed 25','10':'Mon 30','08':'Tue 1 Dec','01':'Wed 2 Dec','12':'Wed 2 Dec'}
for k,v in DL.items(): CLIP[k]['dep']=CLIP[k]['dep'].format(d=v)
TT={ # TikTok: one line + 1-3 hashtags
 '03':"Founder Steve on the days he wants to walk away from trading, and why patience is what keeps him in it 🫂 #tradingpsychology #daytrading",
 '06':"Founder Steve says skipping indicators is a mistake, and the one he trades with is a 9 EMA on charts from 30 minutes down to 1 minute 📈 #daytrading #EMA #futurestrading",
 '61':"Part 2 of Founder Steve's 9 EMA: how steep it slopes tells you if there's a trend, and a flat line means consolidation 🧭 #EMA #daytrading",
 '09':"Founder Steve on why he won't move his stop to break even until he's scaled out and secured some profit 🛑 #riskmanagement #daytrading",
 '05':"Founder Steve ranks indicators: EMAs and support and resistance at S tier, Fibonacci at F 📋 #daytrading #indicators #futurestrading",
 '11':"Why Founder Steve started Halcyon after eight or nine years of trading with prop firms himself 🛤️ #propfirm #futurestrading",
 '10':"Founder Steve's advice for your first evaluation: the activation fee model and a trailing drawdown, so you learn to take profit 🔰 #propfirm #futurestrading",
 '08':"Has Halcyon ever denied a payout? Founder Steve explains automatic rewards and when a manual review happens 🔎 #propfirm #futurestrading",
 '01':"Founder Steve's worst trade: trapped short on a penny stock after hours with no way to get out 😵 #tradingpsychology #riskmanagement",
 '12':"Founder Steve on greed, and why taking the profit you planned beats chasing more 🎣 #tradingpsychology #daytrading",
}
IG={
 '03':"Even our founder wants to walk away some days 🫂\n\nFounder Steve says the urge to quit comes weekly, sometimes daily, and his advice to his younger self is to be patient. Money on a screen doesn't feel real, so he pictures it leaving the table with every loss.\n\nWhen did you last want to quit?\n\n👉 Talk it through with other traders in our Discord: link in bio",
 '06':"Founder Steve laughs at the no-indicators crowd 📈\n\nHis minimum is trend lines plus one EMA. He runs a 9 EMA on any chart from 30 minutes down to 1 minute and watches how price reacts around it, and a flat 9 EMA tells him the market is consolidating.\n\nDo you trade with indicators or a clean chart?\n\n👉 Share your setup in our Discord: link in bio",
 '61':"9 EMA is all you need, says Founder Steve 🧭\n\nIn part 2 he adds the slope: a sharp incline or decline points to a trend, and a flat 9 EMA means consolidation. He uses it as his entry guide and his stop loss guide.\n\nWhich moving average do you keep on your chart?\n\n👉 Share your setup in our Discord: link in bio",
 '09':"Stop moving your stop to break even 🛑\n\nFounder Steve knows his risk before he enters, so he scales out to de-risk as the trade goes his way. Moving to break even before anything is secured usually just gets the stop hit, right before price goes where he expected.\n\nWhen do you move your stop?\n\n👉 Talk risk with us in our Discord: link in bio",
 '05':"Our founder's indicator tier list 📋\n\nFounder Steve puts EMAs and support and resistance at the top, MACD and volume profile in A, and fair value gaps in B. Order flow lands in D and Fibonacci at the bottom.\n\nWhere would you put Fibonacci?\n\n👉 Argue your tier list in our Discord: link in bio",
 '11':"Why our founder started his own prop firm 🛤️\n\nFounder Steve traded with prop firms for eight or nine years and kept hitting the same wall: consistent traders had nowhere to go next. He built Halcyon so traders could keep growing with someone behind them.\n\nWhat would you want from a firm after you pass?\n\n👉 Ask Steve in our Discord: link in bio\n\n"+DISC,
 '10':"Buying your first evaluation? Listen up 🔰\n\nFounder Steve's pick for brand new traders is the activation fee model with a trailing drawdown. It costs less up front while you're learning, and the trailing drawdown pushes you to take profit and step away for the day.\n\nWhich drawdown did you start with?\n\n👉 Ask us which evaluation fits you in our Discord: link in bio\n\n"+DISC,
 '08':"Has a payout ever been denied? 🔎\n\nFounder Steve says rewards are processed automatically when the rules are followed. If something looks off, the account goes to a manual review, which takes longer.\n\nWhat else would you ask about payouts?\n\n👉 Ask us in our Discord: link in bio\n\n"+DISC,
 '01':"Even founders take bad trades 😵\n\nFounder Steve shorted a biopharma penny stock after hours, the company announced more shares, and price jumped every time he tried to buy back. He was holding too many shares to get out. Never again.\n\nWhat's the trade you still think about?\n\n👉 Share it in our Discord: link in bio",
 '12':"Greed is why most traders struggle 🎣\n\nFounder Steve says it's a cliché for a reason: traders see a win on the screen and want more. Taking the profit you planned, day after day, is what builds a track record.\n\nWhat's your take-profit rule?\n\n👉 Talk it through in our Discord: link in bio",
}
TS=[('T21','03','2026-11-20','07:00',"Friday · end of Nvidia week","It takes Friday's 7:00 AM ET slot as a second TikTok, ahead of the 9:00 PM meme."),
    ('T22','06','2026-11-22','18:00',"Sunday evening","Second TikTok of the day, after the morning carousel."),
    ('T23','61','2026-11-24','16:00',"Tuesday · two days after Part 1","Second TikTok of the day, after the dinner meme."),
    ('T24','09','2026-11-27','07:00',"Black Friday · futures close at 1:15 PM ET","Second TikTok of the day, ahead of the 9:00 PM meme."),
    ('T25','05','2026-11-29','18:00',"Sunday evening","Second TikTok of the day, after the morning chart quiz."),
    ('T26','11','2026-11-30','01:00',"Monday · first week of December",""),
    ('T27','10','2026-12-02','16:00',"Wednesday",""),
    ('T28','08','2026-12-03','07:00',"Thursday · the day before the jobs report",""),
    ('T29','01','2026-12-05','07:00',"Saturday · best TikTok slot",""),
    ('T30','12','2026-12-06','07:00',"Sunday","")]
IS=[('R19','03','2026-11-20','11:00',"Friday · feed slot before the evening meme Reel","Friday had one Instagram post, so this takes the late-morning slot."),
    ('R20','06','2026-11-22','18:00',"Sunday evening","Sunday had only the This week carousel."),
    ('R21','61','2026-11-29','18:00',"Sunday evening · a week after Part 1","Sunday 29 is the first free Instagram slot after Part 1."),
    ('R22','09','2026-11-30','18:00',"Monday · first week of December",""),
    ('R23','05','2026-12-01','18:00',"Tuesday",""),
    ('R24','11','2026-12-02','18:00',"Wednesday",""),
    ('R25','10','2026-12-03','18:00',"Thursday",""),
    ('R26','08','2026-12-04','18:00',"Friday · jobs report day, evening",""),
    ('R27','01','2026-12-05','18:00',"Saturday evening",""),
    ('R28','12','2026-12-06','18:00',"Sunday evening","")]
for pid,k,d,t,ctx,ex in TS: P.append(post(pid,'TikTok',k,d,t,TT[k],ctx,ex,skip if CLIP[k].get('dep') else None))
for pid,k,d,t,ctx,ex in IS: P.append(post(pid,'Instagram',k,d,t,IG[k],ctx,ex,skip if CLIP[k].get('dep') else None))
# Waiting on Halcyon
for k,label in [('11','Why I started my own prop firm'),('10','Buying your first eval?'),('08','Has a payout ever been denied?'),('01','Even founders take bad trades'),('12',"You're a bad trader because of this")]:
    c=CLIP[k]; first=min(x[2] for x in TS+IS if x[1]==k)
    D['needs'].append([DL[k], c['dep'].rsplit(', by ',1)[0], 'Both', f"Founder clip \"{label}\", first post {wd(first)} {datetime.date.fromisoformat(first).strftime('%b')}. If it isn't cleared, it moves to the next fortnight."])
D['prod'].append(['Mon 30','Ask the editor for the recut of the greed clip (cut the $300 a day and $2,000 to $3,000 maths) and, if Halcyon wants it, the $180,000 caption on the worst trade clip.','Chase sign-off on the founder clips due this week (Mon 30, Tue 1, Wed 2).'])
s2=s[:m.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+s[m.end(1):]
# page: Drive-hosted videos show a link instead of an inline player
old_m='if(p.videos.length) return `<div class="vids">${p.videos.map(v=>`<figure><video src="${v.src}" controls playsinline preload="metadata"></video>${v.label?`<figcaption>${esc(v.label)}</figcaption>`:""}</figure>`).join("")}</div>`;'
new_m='if(p.videos.length) return `<div class="vids">${p.videos.map(v=>v.drive?`<figure class="drv"><a class="dlb pri" href="${esc(v.src)}" target="_blank" rel="noopener">Watch in Google Drive</a>${v.label?`<figcaption>${esc(v.label.replace("Watch in Drive · ",""))}</figcaption>`:""}</figure>`:`<figure><video src="${v.src}" controls playsinline preload="metadata"></video>${v.label?`<figcaption>${esc(v.label)}</figcaption>`:""}</figure>`).join("")}</div>`;'
assert s2.count(old_m)==1; s2=s2.replace(old_m,new_m)
old_d='if(p.videos.length) return `<div class="dlr">${p.videos.map((v,i)=>dlb("Download video",v.src,b+(p.videos.length>1?"-"+(i+1):"")+".mp4","pri")).join("")}</div>`;'
new_d='if(p.videos.length) return `<div class="dlr">${p.videos.map((v,i)=>v.drive?`<a class="dlb" href="${esc(v.src)}" target="_blank" rel="noopener">Download from Drive</a>`:dlb("Download video",v.src,b+(p.videos.length>1?"-"+(i+1):"")+".mp4","pri")).join("")}</div>`;'
assert s2.count(old_d)==1; s2=s2.replace(old_d,new_d)
if '.drv{' not in s2: s2=s2.replace('</style>','.drv{display:flex;flex-direction:column;align-items:flex-start;gap:8px;padding:18px;border:1px solid rgba(0,251,244,.25);border-radius:14px}.drv a{text-decoration:none}\n</style>',1)
open(f,'w').write(s2)
print('added',len(TS)+len(IS))
