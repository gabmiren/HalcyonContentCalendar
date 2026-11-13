"""Re-caption a meme video: upscale to 1080x1920, cover old burned-in captions with one
fixed dark plate, typeset new captions (Poppins Bold 56 px), add logo + AI tag, -14 LUFS.

usage: python3 recap.py spec.json
spec = {"src":..., "out":..., "plate":[x0,y0,x1,y1] (1080p coords),
        "segments":[[t0,t1,"text"],...], "ai":true, "logo_y":1290}
"""
import json, os, sys, tempfile
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from common import *

spec = json.load(open(sys.argv[1]))
src, out = spec["src"], spec["out"]
x0, y0, x1, y1 = spec["plate"]
tmp = tempfile.mkdtemp()
f = font(FB, spec.get("size", 56))

# base layer: plate + logo + AI tag (constant for the whole clip)
base = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
d = ImageDraw.Draw(base)
d.rounded_rectangle([x0, y0, x1, y1], radius=32, fill=(11, 12, 13, 255))
if spec.get("ai", True):
    ai_tag(base)
if spec.get("logo_y"):
    lg = logo("logo_full", width=200)
    base.alpha_composite(lg, ((1080 - lg.width) // 2, spec["logo_y"]))
base.save(f"{tmp}/base.png")

inputs, chains = ["-i", src, "-i", f"{tmp}/base.png"], []
for i, (t0, t1, text) in enumerate(spec["segments"]):
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    lines = [l.replace('\u00a0', ' ') for l in wrap(dd, text, f, x1 - x0 - 96)]
    assert len(lines) <= 2, text
    lh = round(f.size * 1.15)
    cy = (y0 + y1) / 2 - (len(lines) - 1) * lh / 2
    for j, ln in enumerate(lines):
        dd.text((540, cy + j * lh), ln, font=f, fill=INK + (255,), anchor="mm")
    p = f"{tmp}/c{i}.png"; im.save(p)
    inputs += ["-i", p]

fc = "[0:v]scale=1080:1920:flags=lanczos,setsar=1[v0];[v0][1:v]overlay=0:0[b0]"
last = "b0"
for i, (t0, t1, text) in enumerate(spec["segments"]):
    fc += f";[{last}][{i+2}:v]overlay=0:0:enable='between(t,{t0},{t1-0.001})'[b{i+1}]"
    last = f"b{i+1}"
norm_audio(src, f"{tmp}/a.wav")
inputs += ["-i", f"{tmp}/a.wav"]
aidx = len(inputs)//2 - 1
run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", f"[{last}]", "-map", f"{aidx}:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
     "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out])
print(out, probe(out), loudness(out))
