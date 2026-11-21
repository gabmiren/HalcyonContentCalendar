import sys,asyncio,os
from playwright.async_api import async_playwright
# usage: rend.py stills t1 t2 ... | rend.py frames outdir [plates|alpha]
async def main():
    mode=sys.argv[1]
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':1080,'height':1920})
        q='?plates=1' if (mode=='stills' or (len(sys.argv)>3 and sys.argv[3]=='plates')) else ''
        await pg.goto('file:///home/claude/dd90/build/dd.html'+q);await pg.evaluate("Promise.all(['500 26px P','600 30px P','700 30px P','800 64px P','400 20px P'].map(f=>document.fonts.load(f)))");await pg.wait_for_timeout(500)
        if mode=='stills':
            os.makedirs('st',exist_ok=True)
            for t in sys.argv[2:]:
                await pg.evaluate(f'seek({t})');await pg.screenshot(path=f'st/s_{t}.png')
        else:
            out=sys.argv[2];os.makedirs(out,exist_ok=True);alpha=not q
            dur=await pg.evaluate('DUR');n=int(dur*30)
            for i in range(n):
                await pg.evaluate(f'seek({i/30})')
                await (pg.screenshot(path=f'{out}/{i:05d}.png',omit_background=True) if alpha else pg.screenshot(path=f'{out}/{i:05d}.jpg',type='jpeg',quality=92))
        await b.close()
asyncio.run(main())
