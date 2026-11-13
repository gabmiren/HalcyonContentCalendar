"""Render a Halcyon kit set to JPGs plus a 360px phone contact sheet.

usage: python3 source/kit/render.py source/kit/sets/dyB.html media/ig/dyB
Each <section class="slide"> becomes <prefix>_<n>.jpg (1080 wide). A slide with
data-pg="2/6" gets the standard footer; data-pg="end" gets the footer without the arrow;
data-name="x" overrides the file name. Needs Playwright and Chrome (or Chromium).
"""
import asyncio, os, sys, shutil
from playwright.async_api import async_playwright
from PIL import Image

KIT = os.path.dirname(os.path.abspath(__file__))
FOOT_JS = """
document.querySelectorAll('.slide[data-pg]').forEach(s=>{
  const pg=s.dataset.pg, end=pg.startsWith('end');
  const n=end?pg.slice(4):pg;
  s.insertAdjacentHTML('beforeend',`<div class="foot"><div class="lock"><img class="m" src="${KIT}/brand/logo_mark.png"><img class="w" src="${KIT}/brand/logo_word.png"></div>
  <div class="pg">${n||''}${end?'':'<svg width="40" height="24" viewBox="0 0 40 24"><path d="M2 12h34M26 3l10 9-10 9" stroke="#AFAFAF" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'}</div></div>`);
});
"""


async def main(src, prefix):
    exe = shutil.which("google-chrome") or shutil.which("chromium")
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=exe, args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        await pg.goto("file://" + os.path.abspath(src))
        await pg.evaluate("KIT=>{window.KIT=KIT}", KIT)
        await pg.evaluate(FOOT_JS.replace("${KIT}", KIT))
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(500)
        slides = await pg.query_selector_all(".slide")
        outs = []
        for i, s in enumerate(slides, 1):
            name = await s.get_attribute("data-name") or f"{os.path.basename(prefix)}_{i}"
            out = os.path.join(os.path.dirname(prefix), name + ".jpg")
            await s.screenshot(path=out, type="jpeg", quality=93)
            outs.append(out)
        await b.close()
    ims = [Image.open(o) for o in outs]
    ims = [im.resize((360, round(im.height * 360 / im.width)), Image.LANCZOS) for im in ims]
    sheet = Image.new("RGB", (370 * len(ims) + 10, max(im.height for im in ims) + 20), (40, 40, 40))
    for i, im in enumerate(ims):
        sheet.paste(im, (10 + i * 370, 10))
    sp = f"/tmp/{os.path.basename(prefix)}_sheet360.jpg"
    sheet.save(sp, quality=90)
    print("\n".join(outs)); print("sheet:", sp)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))
