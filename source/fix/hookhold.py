"""Make the hook readable at frame 0: hold the first frame where the headline is fully lit
from 0.0 s until that moment, then play on. Timing and audio are unchanged.
Also normalises audio to -14 LUFS when it is off by more than 1 LU.

usage: python3 hookhold.py in.mp4 out.mp4 [y0 y1] [--t T]
y0,y1 = headline band in 1080x1920 px (default 150 500)
"""
import sys, os, subprocess, tempfile, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from common import *

args = [a for a in sys.argv[1:] if not a.startswith("--")]
src, out = args[0], args[1]
y0, y1 = (int(args[2]), int(args[3])) if len(args) > 3 else (150, 500)
T = None
if "--t" in sys.argv:
    T = float(sys.argv[sys.argv.index("--t") + 1])

if T is None:
    w = 540
    r = subprocess.run(["ffmpeg", "-v", "error", "-t", "3", "-i", src, "-vf",
                        f"crop=1080:{y1-y0}:0:{y0},scale={w}:-2,format=gray", "-f", "rawvideo", "-"],
                       capture_output=True).stdout
    h = (y1 - y0) // 2
    n = len(r) // (w * h)
    fr = np.frombuffer(r, np.uint8)[:n * w * h].reshape(n, h, w)
    cnt = (fr > 215).sum((1, 2))
    peak = cnt.max()
    i = int(np.argmax(cnt >= 0.95 * peak))
    T = round(i / 30 + 1 / 30, 3)
    print("headline bright counts:", cnt[:: 3].tolist(), "-> T =", T)

tmp = tempfile.mkdtemp()
run(["ffmpeg", "-y", "-v", "error", "-ss", str(T), "-i", src, "-frames:v", "1", f"{tmp}/hold.png"])
pr = probe(src)
amap, ain = ["-map", "0:a?", "-c:a", "copy"], []
if pr["audio"]:
    I, _ = loudness(src)
    if I is not None and abs(I + 14) > 1:
        norm_audio(src, f"{tmp}/a.wav")
        ain = ["-i", f"{tmp}/a.wav"]
        amap = ["-map", "2:a", "-c:a", "aac", "-b:a", "256k"]
run(["ffmpeg", "-y", "-v", "error", "-i", src, "-loop", "1", "-t", str(T + 0.1), "-i", f"{tmp}/hold.png", *ain,
     "-filter_complex", f"[0:v][1:v]overlay=0:0:enable='lt(t,{T})'[v]", "-map", "[v]", *amap,
     "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", "30",
     "-movflags", "+faststart", "-shortest" if False else "-y", out])
print(out, probe(out), loudness(out))
