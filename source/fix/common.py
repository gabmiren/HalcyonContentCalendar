"""Shared helpers for Halcyon video fixes: loudness, probing, overlays."""
import json, os, re, subprocess
from PIL import Image, ImageDraw, ImageFont

BRAND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit", "brand")
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FM = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
FR = "/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf"
GROUND = (11, 12, 13)
INK = (242, 242, 242)
GREY = (175, 175, 175)
CYAN = (0, 251, 244)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr[-3000:])
    return r


def probe(path):
    r = run(["ffprobe", "-v", "error", "-show_entries",
             "stream=codec_type,width,height,r_frame_rate:format=duration", "-of", "json", path])
    j = json.loads(r.stdout)
    v = [s for s in j["streams"] if s["codec_type"] == "video"][0]
    a = [s for s in j["streams"] if s["codec_type"] == "audio"]
    return dict(w=v["width"], h=v["height"], fps=v["r_frame_rate"],
                dur=float(j["format"]["duration"]), audio=bool(a))


def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = r[r.rfind("Summary:"):]
    I = re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", tail)
    P = re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", tail)
    return (float(I.group(1)) if I and I.group(1) != "-inf" else None,
            float(P.group(1)) if P and P.group(1) != "-inf" else None)


def gain_filter(path, I=-14.0):
    """Static gain to hit I LUFS plus a true-peak-safe limiter at -1.5 dBFS."""
    cur, _ = loudness(path)
    if cur is None:
        return "anull"
    g = I - cur
    return f"volume={g:.2f}dB,alimiter=limit=0.84:attack=5:release=50:level=false"


def loudnorm_filter(path, I=-14, TP=-1.5, LRA=11):
    """Two-pass loudnorm: measure, then return the filter string for pass 2."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af",
                        f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    j = json.loads(r[r.rfind("{"):r.rfind("}") + 1])
    return (f"loudnorm=I={I}:TP={TP}:LRA={LRA}:measured_I={j['input_i']}:measured_TP={j['input_tp']}"
            f":measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}"
            f":offset={j['target_offset']}:linear=true")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, f, maxw):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def logo(name, width=None, height=None):
    im = Image.open(f"{BRAND}/{name}.png").convert("RGBA")
    if width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    elif height:
        im = im.resize((round(im.width * height / im.height), height), Image.LANCZOS)
    return im


def ai_tag(canvas, x=90, y=262):
    """'AI generated' pill, 26 px text, top-left safe area."""
    d = ImageDraw.Draw(canvas)
    f = font(FM, 26)
    tw = d.textlength("AI generated", font=f)
    d.rounded_rectangle([x, y, x + tw + 44, y + 50], radius=25, fill=(11, 12, 13, 210),
                        outline=(175, 175, 175, 90), width=2)
    d.text((x + 22, y + 25), "AI generated", font=f, fill=GREY + (255,), anchor="lm")


def norm_audio(src, dst_wav, I=-14.0, tol=0.5):
    """Iterate gain + limiter on a wav until integrated loudness is within tol of I."""
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vn", "-ac", "2", "-ar", "48000", dst_wav + ".in.wav"])
    cur, _ = loudness(dst_wav + ".in.wav")
    if cur is None:
        run(["cp", dst_wav + ".in.wav", dst_wav]); return None
    g = I - cur
    for _ in range(5):
        run(["ffmpeg", "-y", "-v", "error", "-i", dst_wav + ".in.wav", "-af",
             f"volume={g:.2f}dB,alimiter=limit=0.7:attack=3:release=60:level=false:asc=1",
             "-ar", "48000", dst_wav])
        got, pk = loudness(dst_wav)
        if abs(got - I) <= tol:
            break
        g += (I - got)
    return got, pk
