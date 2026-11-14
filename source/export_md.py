"""Export the calendar in index.html to markdown for the project's 03 calendar file.
Usage: python3 source/export_md.py 2026-11-16 2026-11-29 out.md"""
import re,json,sys,datetime
a,b,out=sys.argv[1:4]
s=open('index.html').read()
D=json.loads(re.search(r'^const D = (\{.*\});\s*$',s,re.M).group(1))
dt=lambda x:datetime.date.fromisoformat(x)
fmt=lambda d:f"{d.strftime('%a')} {d.day} {d.strftime('%b')}"
L=[f"# Halcyon content calendar, {dt(a).day} to {dt(b).day} {dt(b).strftime('%b %Y')}","",
 f"Exported {fmt(datetime.date.today())} {datetime.date.today().year} from the GitHub calendar (gabmiren/HalcyonContentCalendar), which is the source of truth. Times are ET, with Malaysia time beside them. TikTok and Instagram both post at least once a day. Reels marked To build have a script and storyboard on the calendar page.",""]
for plat in('TikTok','Instagram'):
    L+=[f"## {plat}",""]
    for p in sorted([p for p in D['posts'] if p['platform']==plat and a<=p['date']<=b],key=lambda p:(p['date'],p['time'])):
        L.append(f"### {fmt(dt(p['date']))} · {p['timeLabel']} · {p['title']}")
        L.append(f"- Pillar: {p['pillar']} · Format: {p['format']} · Status: {p['status']} · {p['myt']}")
        L.append(f"- Why here: {p['why']}")
        if p.get('dep'): L.append(f"- Depends on: {p['dep']}")
        sc=p.get('script')
        if sc: L.append(f"- Hook: {sc['hook']} ({sc['len']})")
        if p.get('slides'): L.append(f"- Slides: {', '.join(p['slides'])}")
        L+=["- Caption:","```",p['caption'],"```",""]
L+=["## Waiting on Halcyon",""]+[f"- By {n[0]}: {n[1]} ({n[3]})" for n in D['needs']]
open(out,'w').write("\n".join(L)+"\n")
