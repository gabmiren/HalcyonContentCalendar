import json,subprocess,sys
OFF=0.42
ASR=[0.0,0.2,0.64,0.76,1.6,1.8,2.24,2.4,2.64,3.04,3.36,4.08,4.4,4.64,5.08,5.2,5.36,5.6,6.0,6.32,6.72,7.28,7.48,7.84,8.08,8.6,8.88,9.8,10.0,10.16,10.4,10.84,11.24,11.6,11.92,12.44,12.72,13.04,13.24,13.44,14.08,14.4,14.88,15.44,15.68,15.96,16.48,16.88,17.2,17.76,18.04,18.48,18.84,19.0,19.2,19.36,19.64,20.08,20.72,21.2,21.8,22.12,22.48,22.6,22.76,23.04,23.36,23.84,24.2,24.56,24.72,25.36,25.6,25.92,26.32,26.72,26.92,27.32]
T=lambda i:ASR[i]+OFF
DUR=31.6
ev=[]  # (file, time, gain)
for c in [4.18,7.5,12.6,18.0,20.77,25.5]: ev.append(('sfx/static.wav',c-0.07,0.22))
for i in [1,7,16,73]: ev.append(('/home/claude/mo/blip.wav',T(i)-0.05,0.35))
ev.append(('/home/claude/mo/chime.wav',T(25)-0.05,0.35))
ev.append(('/home/claude/mo/blip.wav',T(29)-0.05,0.25))
# typing ticks
import numpy as np
for a,b in [(T(64)-0.1,T(66)+0.25),(T(67)-0.05,T(70)+0.05)]:
    t=a
    while t<b: ev.append(('sfx/key.wav',t,0.35)); t+=0.075
ev.append(('sfx/off.wav',28.35,0.5))
ev.append(('/home/claude/mo/confirm.wav',28.8,0.25))
vid=sys.argv[1]; out=sys.argv[2]; LN=sys.argv[3] if len(sys.argv)>3 else ''
inp=['-i',vid,'-i','vo.mp3','-i','music.mp3']
for f,_,_ in ev: inp+=['-i',f]
fc=[f"[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay=200|200,apad=whole_dur={DUR},asplit[vo][vo2]",
    f"[2:a]aresample=48000,atrim=0:{DUR},volume=0.22,afade=t=in:d=0.05,afade=t=out:st={DUR-1.4}:d=1.4[mu]"]
lab=[]
for k,(f,t,g) in enumerate(ev):
    ms=int(max(0,t)*1000);fc.append(f"[{k+3}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g},adelay={ms}|{ms}[s{k}]");lab.append(f"[s{k}]")
# duck music under voice
fc.append("[mu][vo]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[mud]")
fc.append(f"[mud]{''.join(lab)}amix=inputs={len(lab)+1}:normalize=0[bed]")
fc.append("[bed][vo2]amix=inputs=2:normalize=0,atrim=0:%s,loudnorm=I=-14:TP=-1.5:LRA=11%s[a]"%(DUR,LN))
cmd=['ffmpeg','-nostdin','-v','error','-y']+inp+['-filter_complex',';'.join(fc),'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',out]
subprocess.run(cmd,check=True);print('ok',out)
