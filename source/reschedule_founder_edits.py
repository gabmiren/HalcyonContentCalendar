"""16 Nov: reschedule the founder edits to start today (Mon 16) and run two weeks. Clip 03 is no longer in the Drive folder, so its posts come off.
Mon 16's founder clip (R10) is replaced by the first edit and moves to Mon 30."""
import re,json,datetime
f='index.html'; s=open(f).read()
m=re.search(r'^const D = (\{.*\});\s*$',s,re.M)
D=json.loads(m.group(1)); P=D['posts']; by={p['id']:p for p in P}
D['posts']=P=[p for p in P if p['id'] not in ('T21','R19')]
def myt(d,t):
    h,mi=map(int,t.split(':')); x=datetime.datetime.fromisoformat(d)+datetime.timedelta(hours=h+13,minutes=mi)
    return f"{x.strftime('%-I:%M %p')} {x.strftime('%a')} {x.day} {x.strftime('%b')} MYT"
def tl(t): h,mi=map(int,t.split(':')); return datetime.time(h,mi).strftime('%-I:%M %p')+' ET'
def mv(pid,d,t,ctx,why):
    p=by[pid]; p.update(date=d,time=t,timeLabel=tl(t),myt=myt(d,t),ctx=ctx,why=why)
W={ # clip -> base why
 '06':"A contrarian opinion with a practical answer inside it (the 9 EMA). It opens the set because it needs no sign-off and gets people arguing in the comments.",
 '61':"Part 2 of the indicators clip, so it follows Part 1 while it's fresh and answers the obvious question: how do you use the 9 EMA?",
 '09':"A risk habit almost every trader has an opinion on, told as Steve's own rule.",
 '05':"Tier lists invite disagreement, and Fibonacci at F is the kind of call people comment on. It follows the two indicator clips, so it lands with viewers who already know Steve's view.",
 '11':"The brand story in Steve's words, and the clip that explains why Halcyon exists, once his trading clips have introduced him.",
 '10':"Practical advice for someone about to buy their first evaluation, after the founder story and the \"check this before you buy\" explainer from Mon 23.",
 '08':"The question every trader asks a new prop firm, answered in 24 seconds. It's a trust post, so it goes out once Halcyon has signed off the claim.",
 '01':"The strongest hook in the set: the founder's own worst trade.",
 '12':"Greed is the most common trading psychology topic, and it closes the set on a lesson. It's last so there's time for the recut.",
}
# TikTok: all nine inside 16 to 29 Nov, as a second TikTok on the day
TT=[('T22','06','2026-11-16','16:00','Monday · start of Nvidia week',"Second TikTok of the day, after Trading terms Part 2."),
    ('T23','61','2026-11-18','07:00','Fed minutes day, morning',"Second TikTok of the day, ahead of the 4:44 meme."),
    ('T24','09','2026-11-20','07:00','Friday · end of Nvidia week',"Second TikTok of the day, ahead of the 9:00 PM meme."),
    ('T25','05','2026-11-22','18:00','Sunday evening',"Second TikTok of the day, after the morning carousel."),
    ('T26','11','2026-11-24','16:00','Tuesday · two days before Thanksgiving',"Second TikTok of the day, after the dinner meme."),
    ('T27','10','2026-11-26','16:00','Thanksgiving · futures halted from 1:00 PM ET',"A quiet market day suits a longer advice clip. Second TikTok of the day, after the halt card."),
    ('T28','08','2026-11-27','07:00','Black Friday · futures close at 1:15 PM ET',"Second TikTok of the day, ahead of the 9:00 PM meme."),
    ('T29','01','2026-11-28','16:00','Saturday afternoon',"Second TikTok of the day, after the two-accounts explainer in the 7:00 AM slot."),
    ('T30','12','2026-11-29','18:00','Sunday evening',"Second TikTok of the day, after the morning chart quiz.")]
# Instagram: only days with room (max 2 a day); the rest stay in the first week of December
IG=[('R20','06','2026-11-16','18:00','Monday · start of Nvidia week',"It takes Monday's 6:00 PM ET Reel slot from the \"pick after you pass\" clip, which moves to Mon 30."),
    ('R21','61','2026-11-20','11:00','Friday · feed slot before the evening meme Reel',"Friday had one Instagram post, so Part 2 takes the late-morning slot."),
    ('R22','09','2026-11-22','18:00','Sunday evening',"Sunday had only the This week carousel."),
    ('R23','05','2026-11-29','18:00','Sunday evening',"Sunday 29 is the last free Instagram slot in the fortnight."),
    ('R24','11','2026-12-01','18:00','Tuesday · first week of December',"Instagram is full (two a day) from Mon 23 to Sat 28, so the last five founder Reels run in the first week of December."),
    ('R25','10','2026-12-02','18:00','Wednesday',"Instagram is full until Sun 29, so this Reel runs in the first week of December."),
    ('R26','08','2026-12-03','18:00','Thursday · the day before the jobs report',"Instagram is full until Sun 29, so this Reel runs in the first week of December."),
    ('R27','01','2026-12-05','18:00','Saturday evening',"Instagram is full until Sun 29, so this Reel runs in the first week of December."),
    ('R28','12','2026-12-06','18:00','Sunday evening',"Instagram is full until Sun 29, so this Reel runs in the first week of December.")]
for pid,k,d,t,ctx,ex in TT+IG: mv(pid,d,t,ctx,W[k]+' '+ex)
# R10 replaced on Mon 16, moved to Mon 30
r=by['R10']; mv('R10','2026-11-30','18:00','Monday · first week of December',"Accounts clip 3 of 3, the Dynamic deep dive for traders ready to level up. Moved off Mon 16 (16 Nov) so the founder edits could start that day; it opens December on Instagram.")
r['todo']=["Moved from Mon 16 to Mon 30 (16 Nov). It's a draft in Metricool for Tue 17, 7:00 AM MYT: reschedule it to Tue 1 Dec, 7:00 AM MYT when you okay it"]+[t for t in r['todo'] if 'Moved from Sat 21' not in t and 'Re-schedule' not in t]
# deadlines: two working days before the first post (Thu 26 is a holiday)
DL={'11':('Fri 20','Tue 24 Nov'),'10':('Tue 24','Thu 26 Nov'),'08':('Wed 25','Fri 27 Nov'),'01':('Wed 25','Sat 28 Nov'),'12':('Wed 25','Sun 29 Nov')}
keymap={'T26':'11','R24':'11','T27':'10','R25':'10','T28':'08','R26':'08','T29':'01','R27':'01','T30':'12','R28':'12'}
for pid,k in keymap.items():
    p=by[pid]; p['dep']=re.sub(r', by [^,]*$',', by '+DL[k][0],p['dep'])
labels={'11':'Why I started my own prop firm','10':'Buying your first eval?','08':'Has a payout ever been denied?','01':'Even founders take bad trades','12':"You're a bad trader because of this"}
for n in D['needs']:
    for k,lab in labels.items():
        if f'"{lab}"' in n[3]:
            n[0]=DL[k][0]; n[3]=f"Founder clip \"{lab}\", first post {DL[k][1]} (TikTok). If it isn't cleared, it moves to the next fortnight."
for x in D['prod']:
    if x[0]=='Mon 30' and 'greed clip' in x[1]: x[0]='Tue 24'; x[1]=x[1].replace('Ask the editor','Ask the editor by today'); x[2]='Chase sign-off on the four founder clips due Wed 25.'
D['prod'].sort(key=lambda x:datetime.datetime.strptime(x[0]+' 2026','%a %d %Y') if x[0][:3] in ('Mon','Tue','Wed','Thu','Fri','Sat','Sun') else datetime.datetime(2099,1,1))
D['prod'].append(['Fri 20','Chase the "Why I started Halcyon" sign-off (path to live, allocation): first post Tue 24.',''])
D['prod'].sort(key=lambda x:datetime.datetime.strptime(x[0]+' Nov 2026','%a %d %b %Y'))
open(f,'w').write(s[:m.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+s[m.end(1):])
print([ (x[0]) for x in D['prod']])
