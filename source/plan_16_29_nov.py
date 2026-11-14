"""Applies the 16 to 29 Nov 2026 plan to index.html (run once from the repo root)."""
import re, json, datetime

s = open('index.html').read()
m = re.search(r'const D = (\{.*?\});\n', s)
D = json.loads(m.group(1))
P = {p['id']: p for p in D['posts']}
DISC = "Halcyon offers simulated educational accounts. Results not guaranteed. T&C apply."
DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def times(date, t):
    y, mo, d = map(int, date.split('-')); h, mi = map(int, t.split(':'))
    et = datetime.datetime(y, mo, d, h, mi)
    my = et + datetime.timedelta(hours=13)
    f = lambda x: x.strftime('%I:%M %p').lstrip('0')
    return f(et) + " ET", f"{f(my)} {DOW[my.weekday()]} {my.day} {my.strftime('%b')} MYT"


def post(id, platform, date, t, title, pillar, fmt, status, ctx, why, todo, caption, day="Post", src="Planned 15 Nov",
         dep=None, fb=None, slides=None, extra=None, script=None, videos=None):
    tl, myt = times(date, t)
    scls = "ok" if status == "Ready" else "dep" if status.startswith("Needs") else "new"
    p = dict(id=id, platform=platform, date=date, time=t, timeLabel=tl, myt=myt, day=day, title=title, pillar=pillar,
             format=fmt, src=src, status=status, scls=scls, ctx=ctx, why=why, todo=todo, dep=dep, fb=fb, fbcap=None,
             fbimg=None, caption=caption, videos=videos or [], slides=slides or [], reel=None, story=None,
             extra=extra or [], pub="none")
    if script: p['script'] = script
    D['posts'] = [x for x in D['posts'] if x['id'] != id] + [p]
    return p


VO = "Narration: the Alexey voice on Higgsfield costs credits, so check the cost first. Switch on the AI label for an AI voice"

# ---------- Week 1 additions and notes ----------
post("I14", "Instagram", "2026-11-20", "11:00", "Your $2,000 drawdown in points", "Education",
     "Explainer · carousel · 5 slides · kit v2", "Ready",
     "Friday · a quiet data day after Nvidia and the Fed minutes",
     "The drawdown reframe is the strongest prop firm topic in our research, and Reels carried it on Monday. This is the version people save: every contract's points on one card, with bars drawn to scale. It gives Friday a second post and becomes the file we DM when someone comments SIZE on Sat 28.",
     ["Built 15 Nov on kit v2. Contract values: ES $50, NQ $20, MES $5, MNQ $2 a point (CME)",
      "Search words in the caption: drawdown, ES points, NQ points, micros",
      "Alt text: Points in a $2,000 max drawdown: 40 on 1 ES, 100 on 1 NQ, 400 on 1 MES, 1,000 on 1 MNQ"],
     "Your $2,000 drawdown is only 40 ES points 📏\n\n- 1 ES is $50 a point, so $2,000 is 40 points\n- 1 NQ is $20 a point, so it's 100 points\n- On micros it's 400 MES points or 1,000 MNQ points\n- At the 5-mini limit it shrinks to 8 ES points or 20 NQ points\n\nKnow the number for your size before the open.\n\nHow many points is your usual stop?\n\n👉 Save this, and ask us about sizing in our Discord: link in bio\n\nBased on the $50K Halcyon Dynamic evaluation. " + DISC,
     slides=[f"ptA_{i}" for i in range(1, 6)])

P['R13']['todo'].append("15 Nov: Metricool rejected the Friday the 13th Trial Reel (\"account does not meet the trial reel follower requirement\"), and this one is scheduled the same way. Change it to a normal Reel in Metricool, or post it as a Trial Reel from the Instagram app")
P['R5']['fb'] = ["What an evaluation checks · Four numbers", "The faster cut of the evaluation explainer. Already made, nothing to approve. Friday's points carousel also covers the feed if this slips."]

# ---------- Week 2 moves ----------
r9 = P['R9']; r9['date'] = "2026-11-27"; r9['time'] = "18:00"; r9['timeLabel'], r9['myt'] = times("2026-11-27", "18:00")
r9['ctx'] = "Black Friday · futures closed early at 1:15 PM ET"
r9['why'] = "Moved from Mon 23 to Black Friday evening. It's the day people compare offers, and this clip walks through Lite, Prime and Dynamic without a discount or a countdown. It also gives Halcyon until Tue 24 to confirm the prices. The early close single covers the morning."
r9['dep'] = "Halcyon confirms the spoken prices and that Lite and Prime are still sold, by Tue 24"
r9['fb'] = ["Skip the Reel", "The early close single already covers Fri 27. Move the clip to the first week of December once the prices are confirmed."]
r9['todo'] = r9['todo'] + ["Founder clip 1 lost 82% of viewers in 3 seconds: check that this cut opens on Steve's strongest line with the question card at frame 0"]

i11 = P['I11']
i11['ctx'] = "Tuesday of Thanksgiving week · the day before PCE"
i11['why'] = "The one promo of the week, five days after Thursday's promo Reel and with the same $3,000 target and $2,000 drawdown. It becomes the third pinned post. Monday's Reel asks the questions and this answers them with Halcyon's numbers, so the two are a day apart on purpose."

# ---------- Week 2 new posts ----------
post("I15", "Instagram", "2026-11-23", "11:00", "Up or down? The first candle after news", "Education",
     "Chart quiz · carousel · 5 slides · kit v2", "Ready",
     "Monday · the week of PCE and Thanksgiving",
     "We have had almost no comments on either app, and the chart guessing game was the best comment driver in our research (1.37M views, viewers posting their call). It builds on our top post, the first candle after CPI, and sets up Wednesday's PCE.",
     ["Built 15 Nov on kit v2. The chart is an example with made-up prices and says so on slides 1, 2, 4 and 5",
      "Reply to every call in the comments within the first hour",
      "Story idea for the same morning: the cover with a native poll sticker, Up or Down",
      "Search words in the caption: NQ, chart, 8:30 AM ET release, drawdown",
      "Alt text: Example NQ 5-minute chart after an 8:30 release. The first candle jumps 38 points, then price falls 61 points"],
     "Up or down from here? Comment your call before you swipe 📊\n\n- An example NQ chart, right after an 8:30 AM ET release\n- The first 5-minute candle jumps 38 points\n- Slide 2 shows what came next, and slide 3 explains why\n\nOn 1 NQ, a 38-point candle is 38% of a $2,000 drawdown.\n\nDid you call it right?\n\n👉 Talk news days with us in our Discord: link in bio\n\nExample chart for illustration, not real market data. " + DISC,
     slides=[f"udA_{i}" for i in range(1, 6)])

CHECK = dict(
    len="About 32 s narrated (TikTok). The Instagram cut can run the same file",
    hook="Check this before you buy any evaluation",
    device="One checklist ticket. Each question ticks, then flips to Halcyon's one-line answer. The ticket stays on screen from the hook to the end card",
    beats=[
        ["0.0 to 2.5 s", "The whole hook on screen from frame 0, with the four-question ticket below it (the cover frame)", "Check this before you buy any prop firm evaluation."],
        ["2.5 to 9 s", "Row 1 lights up: \"What ends the account?\" It flips to \"$2,000 max drawdown\" and a bar drains to show it", "First, what ends the account? Here it's the $2,000 max drawdown."],
        ["9 to 15 s", "Row 2: \"When must you be flat?\" flips to a clock stopping at 4:45 PM ET", "Second, when do you have to be flat? At Halcyon, 4:45 PM Eastern, every trading day."],
        ["15 to 21 s", "Row 3: \"How big can you trade?\" flips to 5 blocks, then 25 small ones", "Third, how big can you trade? Five minis or twenty-five micros at one time."],
        ["21 to 26 s", "Row 4: \"What happens after you pass?\" flips to \"You pick your reward account\"", "And what happens after you pass? You pick your reward account."],
        ["26 to 29 s", "All four rows ticked. The payoff line appears word by word", "Any firm should answer those in one line. If it can't, keep asking."],
        ["29 to 32 s", "End card: logo, \"Ask in our Discord\" pill, LINK IN BIO, disclaimer held 2.5 s", "(music only)"],
    ],
    notes=["Pinned comment: \"The $2,000 drawdown can be trailing or end of day. You pick at checkout.\"",
           "Protective angle from our research: the top prop firm videos tell people what to check before they buy. We name no other firm",
           VO, "Every number is a published rule value. No fees on screen, so nothing new needs sign-off"])

CAP_CHECK = "Check this before you buy any prop firm evaluation ✅\n\n- What ends the account? Here it's the $2,000 max drawdown\n- When must you be flat? 4:45 PM ET, every trading day\n- How big can you trade? 5 minis or 25 micros at one time\n- What happens after you pass? You pick your reward account\n\nAny firm should be able to answer those in one line.\n\nWhich question do you wish you'd asked sooner?\n\n👉 Ask us anything in our Discord: link in bio\n\n" + DISC
post("T13", "TikTok", "2026-11-23", "01:00", "Check this before you buy any evaluation", "Education",
     "Narrated motion explainer · checklist ticket · about 32 s · script and storyboard", "To build · Sat 21",
     "Monday 1:00 AM ET, one of the five best TikTok slots",
     "The protective angle is the strongest prop firm format on YouTube and nobody in our scan runs it honestly from the firm's side. It's narrated, because 8 of 10 silent explainers we tracked flopped, and it sets up Tuesday's four cards.",
     ["Build from the script below. The cover frame is made", VO, "Disclaimer on the end card"],
     "4 questions to ask before you buy any prop firm evaluation, with Halcyon's answers: $2,000 drawdown, flat by 4:45 PM ET, 5 minis or 25 micros ✅ #propfirm #futurestrading",
     extra=[["Cover and first frame", "rc_check"]], script=CHECK)
post("R14", "Instagram", "2026-11-23", "18:00", "Check this before you buy any evaluation", "Education",
     "Reel · narrated explainer · about 32 s · script and storyboard", "To build · Sat 21",
     "Same day as the TikTok",
     "Reels drove 91% of our Instagram views, so the day's TikTok goes out as the evening Reel. The morning carousel carries the feed if the build slips.",
     ["Same file as the TikTok. Use the cover frame as the Reel cover", "Search words in the caption: prop firm evaluation, max drawdown, minis, micros"],
     CAP_CHECK, day="Reel", extra=[["Cover and first frame", "rc_check"]], script=CHECK)

DINNER = dict(
    len="8 s, no voice. Add a trending sound in the app",
    hook="Relatives: so what do you do now?",
    device="One chat thread. Two answers get typed and struck out, and the third one sends",
    beats=[
        ["0.0 to 1.5 s", "Hook on screen from frame 0 with the first answer already typed: \"I day trade NQ futures\"", "(sound only)"],
        ["1.5 to 3.5 s", "A strike runs through it. The second answer types in: \"I'm in a simulated evaluation\"", ""],
        ["3.5 to 5.5 s", "Strike through the second. Three typing dots hold for a beat", ""],
        ["5.5 to 8 s", "The last bubble pops in with a glow: \"I work in finance.\" Hold, then loop", ""],
    ],
    notes=["Silent export is fine here because a platform sound is added in the app",
           "Logo under the bubbles, everything inside the safe zone", "No disclaimer needed: no rules or offer on screen"])
post("R15", "Instagram", "2026-11-24", "18:00", "Thanksgiving dinner: so what do you do now?", "Entertainment",
     "Reel · faceless meme · 8 s · script and storyboard", "To build · Mon 23",
     "Two days before Thanksgiving",
     "A silent meme, the format that can win without a voiceover, on the one question every trader gets at the table. It follows the morning promo so the day isn't all product.",
     ["Build from the script below. The cover frame is made", "Add a trending sound in the Instagram app"],
     "Practising my answer before Thursday 🦃", day="Reel",
     extra=[["Cover and first frame", "rc_dinner"]], script=DINNER)
post("T15", "TikTok", "2026-11-26", "07:00", "Thanksgiving dinner: so what do you do now?", "Entertainment",
     "Faceless meme · 8 s · same file as the Instagram Reel", "To build · Mon 23",
     "Thanksgiving morning · futures halt at 1:00 PM ET",
     "Thursday 7:00 AM ET is the second best TikTok slot, and on Thanksgiving morning this is the joke of the day.",
     ["Same file as Tuesday's Reel", "Add a trending sound in the app"],
     "Thanksgiving dinner and someone asks what you do now 🦃 #tradinghumor #daytrading",
     extra=[["Cover and first frame", "rc_dinner"]], script=DINNER)

PCE = dict(
    len="About 24 s. Narrated for TikTok, and the same cut works on Instagram",
    hook="The last big number before Thanksgiving",
    device="One week strip (Wed, Thu, Fri) with a dot that travels along it. It stays on screen the whole time",
    beats=[
        ["0.0 to 3 s", "Hook from frame 0 over the week strip, with the dot on Wed and \"8:30 AM ET\" large (the cover frame)", "The last big number before Thanksgiving lands at 8:30 this morning."],
        ["3 to 8 s", "\"PCE\" and \"GDP\" pills grow under the time", "It's PCE, the Fed's preferred inflation gauge, with the second read on third-quarter GDP."],
        ["8 to 14 s", "Two paths fork from the dot: a grey one down labelled \"Hotter\", a cyan one up labelled \"Softer\"", "A hotter print tends to push rate expectations up and NQ down. A softer one tends to do the reverse."],
        ["14 to 19 s", "A drawdown bar: 100 points on 1 NQ, 1,000 on 1 MNQ", "On one NQ, your $2,000 drawdown is 100 points. On one micro, it's a thousand."],
        ["19 to 22 s", "The dot travels on: Thu \"halt 1:00 PM\", Fri \"close 1:15 PM\"", "Then futures halt early Thursday and close early Friday."],
        ["22 to 24 s", "End card with the question, the Discord pill and the disclaimer", "Hot or soft? Tell us below."],
    ],
    notes=["No forecast and no numbers for the print itself. Moves in points only",
           "News previews posted before the release were our top post on both apps, so this goes out 90 minutes before 8:30",
           VO, "Re-check on Tue 24 that BEA still lists both releases for 8:30 AM ET"])
CAP_PCE = "PCE and GDP land at 8:30 AM ET, the last big numbers before Thanksgiving ⏰\n\n- PCE is the Fed's preferred inflation gauge, out with the second estimate of Q3 GDP\n- ES and NQ futures halt at 1:00 PM ET on Thursday and close at 1:15 PM ET on Friday\n- On one NQ, a $2,000 drawdown is 100 points. On one MNQ, it's 1,000\n\nA hotter print tends to push rate expectations up and NQ down, and a softer one the other way.\n\nHot or soft? Tell us below.\n\n👉 Talk it through in our Discord: link in bio\n\nExample only, not a prediction. " + DISC
post("T14", "TikTok", "2026-11-25", "07:00", "PCE at 8:30: the last big number before Thanksgiving", "News",
     "Narrated news preview · week strip · about 24 s · script and storyboard", "To build · Tue 24",
     "PCE and GDP at 8:30 AM ET · the day before Thanksgiving",
     "The CPI preview was our top post on both apps, and news previews work when they go out before the number. This one lands 90 minutes ahead and ties the print to the holiday hours.",
     ["Build from the script below. The cover frame is made", VO, "No forecast, moves in points only"],
     "PCE and GDP at 8:30 AM ET, then a holiday week: what an NQ move in points means for a $2,000 drawdown ⏰ #PCE #NQ #futurestrading",
     extra=[["Cover and first frame", "rc_pce"]], script=PCE)
post("R16", "Instagram", "2026-11-25", "07:00", "PCE at 8:30: the last big number before Thanksgiving", "News",
     "Reel · news preview · about 24 s · script and storyboard", "To build · Tue 24",
     "PCE and GDP at 8:30 AM ET · the day before Thanksgiving",
     "Same timing as the Nvidia preview, which went out at 7:00 AM ET. The market mood single follows at noon with the result.",
     ["Same file as the TikTok. Use the cover frame as the Reel cover", "Search words in the caption: PCE, GDP, NQ, Thanksgiving trading hours"],
     CAP_PCE, day="Reel", extra=[["Cover and first frame", "rc_pce"]], script=PCE)

post("I16", "Instagram", "2026-11-25", "12:00", "After PCE: every market's mood", "News",
     "Market mood · single · built on the day", "To build · Wed 25",
     "After PCE and GDP · the last full session before Thanksgiving",
     "The morning preview asked hot or soft, and this answers it. The market mood single is the news format we can turn around in 30 minutes.",
     ["Build after the 9:30 AM ET open from source/kit/sets/md.html (edit the MOOD block only)", "Moves in percent, with sources on the card", "Fill the [brackets] in the caption from the same sources"],
     "How every market took PCE this morning 📊\n\n- PCE came in at [x.x%] against [x.x%] expected\n- Nasdaq [x.xx%], S&P 500 [x.xx%], Dow [x.xx%]\n- Gold [x.xx%], oil [x.xx%], the 10-year yield [x bps]\n\nFutures halt at 1:00 PM ET tomorrow for Thanksgiving.\n\nDid you trade it or watch it?\n\n👉 Share your morning in our Discord: link in bio",
     src="IG template")

post("I17", "Instagram", "2026-11-26", "10:00", "Futures halt at 1:00 PM ET today", "News",
     "Holiday hours · single · kit v2", "Ready",
     "Thanksgiving · stocks closed, futures halt at 1:00 PM ET",
     "One clear fact on the day it matters. Holiday hours change when a trade has to be closed, which is the rule our audience trips on most.",
     ["Built 15 Nov on kit v2. Hours from the CME Group holiday calendar, re-check on Fri 20",
      "Ask Halcyon for the holiday session close so the card can say it. Until then it tells people to check",
      "Alt text: Thanksgiving, Thu 26 Nov. ES and NQ futures halt at 1:00 PM ET and reopen at 6:00 PM ET"],
     "Futures halt at 1:00 PM ET today for Thanksgiving 🕐\n\n- The stock market is closed all day\n- ES and NQ halt at 1:00 PM ET and reopen at 6:00 PM ET\n- Friday's session closes early, at 1:15 PM ET\n\nNormal days are flat by 4:45 PM ET, so check Halcyon's holiday close before you trade today.\n\nTrading the morning or taking the day off?\n\n👉 Happy Thanksgiving from all of us. Say hi in our Discord: link in bio\n\n" + DISC,
     slides=["thB_thu"])
post("I18", "Instagram", "2026-11-27", "10:00", "Futures close early at 1:15 PM ET", "News",
     "Holiday hours · single · kit v2", "Ready",
     "Black Friday · early close",
     "The second half of the holiday hours, posted the morning it applies. It keeps Friday covered whether or not the founder clip is cleared.",
     ["Built 15 Nov on kit v2. Hours from the CME Group holiday calendar, re-check on Fri 20",
      "Alt text: Fri 27 Nov. ES and NQ futures close early at 1:15 PM ET and reopen Sunday at 6:00 PM ET"],
     "Futures close early today, at 1:15 PM ET 🔔\n\n- Stocks close at 1:00 PM ET\n- ES and NQ close at 1:15 PM ET\n- Futures reopen Sunday at 6:00 PM ET\n\nNormal days are flat by 4:45 PM ET, so check Halcyon's holiday close before you trade.\n\nTrading the half day or sitting it out?\n\n👉 Plan next week with us in our Discord: link in bio\n\n" + DISC,
     slides=["thB_fri"])

post("I19", "Instagram", "2026-11-28", "11:00", "Trailing or end of day?", "Education",
     "Explainer · carousel · 5 slides · kit v2", "Needs Halcyon",
     "Saturday · markets closed",
     "Trailing against end of day was the second most liked comment on the biggest drawdown video in our research, so people want this answered. It's the same day drawn twice, with the room left shown in points.",
     ["Built 15 Nov on kit v2. The example day is made up and tagged EXAMPLE",
      "Search words in the caption: trailing drawdown, end of day drawdown, prop firm evaluation",
      "Alt text: The same day on 1 NQ with a trailing and an end of day drawdown. After a 30-point pullback, trailing leaves 70 points of room and end of day leaves 110"],
     "Trailing or end of day? The same day with each drawdown 📐\n\n- Trailing: the floor follows your high and never moves back down\n- End of day: the floor stays put and updates once, after the close\n- In this example, a 30-point pullback leaves 70 points of room on trailing and 110 on end of day\n\nYou pick one at checkout: Trailing ($51) or End of day ($53).\n\nWhich one fits how you trade?\n\n👉 Ask us about both in our Discord: link in bio\n\nExample only, with made-up prices. " + DISC,
     dep="Halcyon confirms how the trailing drawdown moves (does it follow open profit during the day, as drawn?) and the $51 and $53 fees, by Tue 24",
     fb=["Skip it", "The evening Reel covers Saturday. Run this the week after once the wording is confirmed."],
     slides=[f"teA_{i}" for i in range(1, 6)])

SAME_TT = dict(
    len="About 34 s narrated",
    hook="Same 20-point loss, two accounts",
    device="Two drawdown bars side by side, Trader A and Trader B. They stay on screen from the first frame to the end card",
    beats=[
        ["0.0 to 3 s", "Hook from frame 0 over both bars, full (the cover frame, bars at 0% used)", "Two traders start the same $50K evaluation."],
        ["3 to 8 s", "A small NQ chart appears between the bars. Both enter long at the same candle", "Both go long NQ. Both get stopped out twenty points lower."],
        ["8 to 15 s", "Trader A's label shows \"5 minis\". The bar drains to empty: \"100% of the drawdown used\". A grey cross", "Trader A was on five minis. That one loss used the whole $2,000 drawdown, and the evaluation is over."],
        ["15 to 22 s", "Trader B's label shows \"5 micros\". The bar drops a sliver: \"10% used\"", "Trader B was on five micros. The same twenty points used ten percent."],
        ["22 to 27 s", "Nine more slivers ghost in on B's bar, one by one", "Trader B gets to be wrong nine more times."],
        ["27 to 31 s", "Both bars hold. The payoff line reveals word by word", "The trade was the same. The size decided who's still here."],
        ["31 to 34 s", "End card: logo, Discord pill, LINK IN BIO, disclaimer held 2.5 s", "(music only)"],
    ],
    notes=["Two characters on different paths was the strongest story shape in our research. The traders have no names or faces, so nobody poses as a customer",
           "EXAMPLE tag on screen from 3 s. Losses are shown in points and as a share of the drawdown, never as a dollar result",
           "Maths: 20 points x $20 x 5 minis = $2,000. 20 points x $2 x 5 micros = $200, which is 10%",
           "Pinned comment: \"5 minis is the most Halcyon Dynamic allows at one time. You don't have to use it.\"", VO])
SAME_IG = dict(
    len="8 to 10 s loop, text and music only",
    hook="Same 20-point loss, two accounts",
    device="The same two bars. The value sits in the caption, as in the reference Reel you shared",
    beats=[
        ["0.0 to 2 s", "Hook from frame 0, both bars full, \"Trader A · 5 minis\" and \"Trader B · 5 micros\"", "(music only)"],
        ["2 to 5 s", "Line 1 appears: \"20 points on 5 minis\". Bar A drains to empty, \"100% used\"", ""],
        ["5 to 8 s", "Line 2 appears: \"20 points on 5 micros\". Bar B drops a sliver, \"10% used\"", ""],
        ["8 to 10 s", "Hold on both results, then cut back to frame 0 so it loops", ""],
    ],
    notes=["Modelled on the reference Reel: a short loop that gets watched twice, with the lesson in a caption worth saving",
           "Comment keyword test: someone has to DM the points carousel (Fri 20) to everyone who comments SIZE. With our volume that can be done by hand; ManyChat's free plan can automate it later",
           "EXAMPLE tag on screen. Disclaimer in the caption"])
post("T16", "TikTok", "2026-11-28", "07:00", "Same 20-point loss, two accounts", "Education",
     "Narrated story explainer · two drawdown bars · about 34 s · script and storyboard", "To build · Fri 27",
     "Saturday 7:00 AM ET, the best TikTok slot of the week",
     "The best slot gets the strongest idea: the drawdown reframe told as two traders on different paths, the two patterns that broke out most in our research. It's a week after the first drawdown explainer and uses a different device.",
     ["Build from the script below. The cover frame is made", VO, "EXAMPLE tag on screen, disclaimer on the end card"],
     "Same 20-point NQ loss on a $50K evaluation: on 5 minis it uses the whole $2,000 drawdown, on 5 micros it uses 10% 📏 #propfirm #NQ #riskmanagement",
     extra=[["Cover and first frame", "rc_same"]], script=SAME_TT)
post("R17", "Instagram", "2026-11-28", "18:00", "Same 20-point loss, two accounts", "Education",
     "Reel · 8 to 10 s loop · text and music · script and storyboard", "To build · Fri 27",
     "Saturday evening",
     "On Instagram the breakout finance Reels were short, text-led loops, so this is the 10-second cut of the morning's TikTok with the lesson in the caption. It's also our first comment keyword test, aimed at the zero-comment problem.",
     ["Build from the script below. The cover frame is made", "After posting, DM the Fri 20 points carousel to everyone who comments SIZE",
      "Search words in the caption: NQ, minis, micros, drawdown, $50K evaluation"],
     "Same 20-point loss, two different accounts 📏\n\n- Both traders are long NQ in a $50K evaluation\n- Trader A is on 5 minis, so 20 points uses the whole $2,000 drawdown\n- Trader B is on 5 micros, so the same 20 points uses 10% of it\n\nYour size decides how many times you can be wrong.\n\nHow many losses could your size take?\n\n👉 Comment SIZE and we'll DM you the full points table\n\nExample only, using the $50K Dynamic evaluation's figures. " + DISC,
     day="Reel", extra=[["Cover and first frame", "rc_same"]], script=SAME_IG)

post("I20", "Instagram", "2026-11-29", "10:00", "This week: the jobs report is back Friday", "News",
     "This week · carousel · 5 slides · kit v2", "Ready",
     "Sunday · week ahead · futures reopen at 6:00 PM ET",
     "The Sunday habit, week four. The jobs report on Fri 4 Dec opens the year's last run of big dates, with the Fed on Wed 9 Dec and CPI on Thu 10 Dec.",
     ["Built 15 Nov on kit v2. Dates from BLS (jobs 4 Dec, CPI 10 Dec) and the Federal Reserve (FOMC 8 to 9 Dec)", "Sat 28: re-check all three dates before it goes out",
      "Alt text: This week, 30 Nov to 4 Dec. Jobs report Fri 4 Dec 8:30 AM ET, Fed decision Wed 9 Dec 2:00 PM ET, CPI Thu 10 Dec 8:30 AM ET"],
     "The jobs report is back this Friday 🗓️\n\n- Friday 4 Dec: the jobs report at 8:30 AM ET\n- Wednesday 9 Dec: the Fed's last rate decision of the year, at 2:00 PM ET\n- Thursday 10 Dec: CPI at 8:30 AM ET\n\nNews straddles are banned, and every Halcyon account is flat by 4:45 PM ET.\n\nWhich one are you sitting out?\n\n👉 Plan the week with us in our Discord: link in bio\n\n" + DISC,
     slides=[f"wkD_{i}" for i in range(1, 6)])

# ---------- Events, needs, production, facts ----------
E = D['events']
E["2026-11-25"] = ["8:30 AM ET · PCE (Oct) and GDP, second estimate (Q3)"]
E["2026-11-26"] = ["Thanksgiving · stocks closed · futures halt 1:00 PM ET, reopen 6:00 PM ET"]
E["2026-11-27"] = ["Black Friday · stocks close 1:00 PM ET · futures close 1:15 PM ET"]
E["2026-12-04"] = ["8:30 AM ET · Jobs report (Nov)"]
E["2026-12-09"] = ["2:00 PM ET · Fed decision"]
E["2026-12-10"] = ["8:30 AM ET · CPI (Nov)"]

D['needs'] = [
    ["Tue 17", "Dynamic promo wording, including \"no daily loss limit\", and which promo option (A to D)", "Both", "Thu 19 promo on both apps. The evaluation explainer is the backup."],
    ["Fri 20", "The fees ($51 and $53), the four rule values and the wording on the four cards carousel", "Instagram", "Tue 24 four cards. If it isn't cleared, the feed post is skipped that day."],
    ["Tue 24", "The prices Steve says in the Lite, Prime or Dynamic clip, and that Lite and Prime are still sold", "Instagram", "Fri 27 founder clip. The early close single covers the day."],
    ["Tue 24", "How the trailing drawdown moves during the day (does it follow open profit?), for the Trailing or end of day carousel", "Instagram", "Sat 28 carousel. The evening Reel covers the day."],
    ["Fri 20", "Halcyon's session close on Thu 26 and Fri 27", "Both", "The holiday hours singles say \"check Halcyon's holiday close\" until we have it."],
    ["Any time", "Whether a trader comment keyword can be answered by DM from the brand account (by hand or with ManyChat)", "Instagram", "Sat 28 comment keyword test."],
    ["Any time", "Counsel sign-off on the Arena founder shorts, and real reward certificates with each trader's written OK", "TikTok", "Community and proof posts stay on hold until then."],
]
D['prod'] = [
    ["Mon 16", "", "Reply to every comment on the weekend posts within the day."],
    ["Tue 17", "Chase Halcyon on the promo wording (due today).", "Check the Trial Reel setting on \"The instant I go long\" before 9:00 PM ET."],
    ["Wed 18", "", "Build the market mood single after the 9:30 AM ET open (30 minutes)."],
    ["Fri 20", "Re-check the CME holiday hours. Chase the four cards sign-off (due today).", "Schedule the points carousel once you've reviewed it."],
    ["Sat 21", "Build \"Check this before you buy any evaluation\" (narrated, 32 s) for Mon 1:00 AM ET.", "Same file for the Mon 6:00 PM ET Reel."],
    ["Mon 23", "Build the Thanksgiving dinner meme (8 s) for Thu.", "Same file for the Tue 6:00 PM ET Reel. Reply to every chart quiz call."],
    ["Tue 24", "Build the PCE preview (24 s) for Wed 7:00 AM ET. Re-check the BEA time.", "Chase the founder clip prices and the trailing drawdown answer (due today)."],
    ["Wed 25", "", "Build the market mood single after the open."],
    ["Fri 27", "Build \"Same 20-point loss, two accounts\" (narrated, 34 s) for Sat 7:00 AM ET.", "Cut the 10 s loop for the Sat 6:00 PM ET Reel."],
    ["Sat 28", "", "Re-check the 4, 9 and 10 Dec dates. DM the points carousel to everyone who comments SIZE."],
]
D['facts'] = [f for f in D['facts'] if not f[0].startswith("Thu 26")] + [
    ["Wed 25 Nov", "PCE (October) and GDP second estimate (Q3), 8:30 AM ET", "BEA release schedule", "PCE preview and market mood, Wed 25"],
    ["Thu 26 Nov", "Thanksgiving: stocks closed, equity index futures halt 1:00 PM ET and reopen 6:00 PM ET", "CME Group holiday calendar", "Instagram hours single, Thu 26"],
    ["Fri 27 Nov", "Stocks close 1:00 PM ET, equity index futures close 1:15 PM ET", "CME Group holiday calendar, NYSE", "Instagram hours single, Fri 27"],
    ["Fri 4 Dec", "Jobs report (November), 8:30 AM ET", "BLS release schedule", "This week carousel, Sun 29"],
    ["Wed 9 Dec", "Fed decision, 2:00 PM ET (FOMC meets 8 to 9 Dec)", "Federal Reserve calendar", "This week carousel, Sun 29"],
    ["Thu 10 Dec", "CPI (November), 8:30 AM ET", "BLS release schedule", "This week carousel, Sun 29"],
]
D['standby'] = [x for x in D['standby'] if not x[0].startswith("Thanksgiving week")]

s = s[:m.start(1)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):]

# ---------- Drawer: show the script and storyboard ----------
if 'function scriptHTML' not in s:
    fn = '''function scriptHTML(p){
 const c=p.script; if(!c) return "";
 const rows=c.beats.map(b=>`<tr><td style="white-space:nowrap;color:var(--ink2)">${esc(b[0])}</td><td>${esc(b[1])}</td><td style="color:var(--ink2)">${esc(b[2])}</td></tr>`).join("");
 const vo=c.beats.map(b=>b[2]).filter(t=>t&&t[0]!=="(").join(" ");
 return `<div class="lab" style="margin-top:18px">Script and storyboard</div>
 <div class="f" style="margin:8px 0 10px"><div>Hook</div><div><b>${esc(c.hook)}</b></div><div>Length</div><div>${esc(c.len)}</div><div>One device</div><div>${esc(c.device)}</div></div>
 <div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:13px;line-height:1.5"><thead><tr style="text-align:left" class="lab"><th style="padding:6px 8px 6px 0">Time</th><th style="padding:6px 8px">On screen</th><th style="padding:6px 0 6px 8px">Voice</th></tr></thead><tbody class="sb">${rows}</tbody></table></div>
 ${vo?`<div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px" class="lab">Voiceover <button class="btn" id="cv">Copy voiceover</button></div><pre>${esc(vo)}</pre>`:""}
 <ul style="margin:8px 0 18px 18px;font-size:13px;line-height:1.55;color:var(--ink2)">${c.notes.map(n=>`<li>${esc(n)}</li>`).join("")}</ul>`;
}
'''
    s = s.replace('// drawer\nfunction open(id){', fn + '// drawer\nfunction open(id){')
    s = s.replace(' ${fbx}\n <div style="display:flex;justify-content:space-between;align-items:center" class="lab">Caption',
                  ' ${fbx}\n ${scriptHTML(p)}\n <div style="display:flex;justify-content:space-between;align-items:center" class="lab">Caption')
    s = s.replace(' $("#cc").onclick=()=>copy(p.caption,"Caption copied");',
                  ' $("#cc").onclick=()=>copy(p.caption,"Caption copied");\n if($("#cv"))$("#cv").onclick=()=>copy(p.script.beats.map(b=>b[2]).filter(t=>t&&t[0]!=="(").join(" "),"Voiceover copied");')
    s = s.replace('</style>', '.sb td{padding:8px;border-top:1px solid var(--line);vertical-align:top}.sb td:first-child{padding-left:0}.sb td:last-child{padding-right:0}\n</style>', 1)
    assert 'scriptHTML(p)}' in s and 'id="cv"' in s
open('index.html', 'w').write(s)
print("posts", len(D['posts']))

# ---------- Audit fixes (second pass) ----------
s = open('index.html').read()
m = re.search(r'const D = (\{.*?\});\n', s)
D = json.loads(m.group(1))
P = {p['id']: p for p in D['posts']}
P['R5']['caption'] = re.sub(r'\n#\S+( #\S+)*\s*$', '', P['R5']['caption']).rstrip()
REFRESH = dict(
    len="8 s, no voice. Add a trending sound in the app",
    hook="Market's closed. Still refreshing.",
    device="One chart panel with a flat line and a refresh counter that keeps climbing",
    beats=[
        ["0.0 to 2 s", "Hook on screen from frame 0. A chart panel with a dead flat line and a tag: \"No trading right now\"", "(sound only)"],
        ["2 to 5 s", "A refresh icon spins. The counter ticks: refreshed 12 times, 27, 46", ""],
        ["5 to 7 s", "The line stays flat. A small caption appears: \"Maybe now\"", ""],
        ["7 to 8 s", "The counter jumps to 47 and the icon spins again. Loop", ""],
    ],
    notes=["Silent export is fine here because a platform sound is added in the app", "Logo under the panel, everything inside the safe zone",
           "No prices, no P&L and no rule on screen, so no disclaimer"])
post("R18", "Instagram", "2026-11-26", "15:00", "Market's closed. Still refreshing.", "Entertainment",
     "Reel · faceless meme · 8 s · script and storyboard", "To build · Wed 25",
     "Thanksgiving afternoon · futures halted from 1:00 to 6:00 PM ET",
     "Posted while futures are halted, when every trader is doing exactly this. It brings the week's Instagram mix closer to one entertainment post in four.",
     ["Build from the script below", "Add a trending sound in the Instagram app"],
     "Futures halted at 1:00 PM and I'm still checking 👀", day="Reel", script=REFRESH)
post("T17", "TikTok", "2026-11-27", "21:00", "Market's closed. Still refreshing.", "Entertainment",
     "Faceless meme · 8 s · same file as the Instagram Reel", "To build · Wed 25",
     "Black Friday night · futures closed since 1:15 PM ET",
     "Friday 9:00 PM ET is one of the five best TikTok slots, and the market has been shut since lunch. It keeps TikTok at half entertainment for the week.",
     ["Same file as Thursday's Reel", "Add a trending sound in the app"],
     "Futures closed at 1:15 PM ET and I'm still refreshing the chart 👀 #tradinghumor #futurestrading", script=REFRESH)
D['prod'] = [[a, b + (" Build the Still refreshing meme (8 s) for Thu and Fri." if a == "Wed 25" else ""), c] for a, b, c in D['prod']]
s = s[:m.start(1)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):]
open('index.html', 'w').write(s)
