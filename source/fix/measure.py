import sys,os,subprocess,numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
def frame(path,t,w=270):
    r=subprocess.run(["ffmpeg","-v","error","-ss",str(t),"-i",path,"-frames:v","1","-vf",f"scale={w}:-2,format=gray","-f","rawvideo","-"],capture_output=True).stdout
    h=len(r)//w; return np.frombuffer(r,np.uint8)[:h*w].reshape(h,w)
def first_text(path,dur):
    # first time at which a frame has bright text-like pixels (>200) count > 150 at 270px
    for t in np.arange(0,min(dur,4),0.1):
        f=frame(path,t); 
        if (f>200).sum()>150: return round(float(t),1)
    return None
for p in sys.argv[1:]:
    pr=probe(p); I,P=loudness(p) if pr['audio'] else (None,None)
    f0=frame(p,0); fl=frame(p,max(0,pr['dur']-0.05))
    print(f"{os.path.basename(p):42s} {pr['w']}x{pr['h']} {pr['dur']:5.1f}s LUFS={I} TP={P} f0luma={f0.mean():.0f} f0bright={(f0>200).sum()} firsttext={first_text(p,pr['dur'])} lastluma={fl.mean():.0f}")
