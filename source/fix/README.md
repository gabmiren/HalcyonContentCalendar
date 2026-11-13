# Halcyon video fixes (finished exports, no source needed)

Used 14 Nov to fix scheduled videos whose source pages weren't in any repo. Needs ffmpeg, Pillow, numpy.

- `measure.py a.mp4 b.mp4 ...` size, length, loudness (LUFS, true peak), frame-0 brightness, time of first text, last-frame brightness.
- `hookhold.py in.mp4 out.mp4 [y0 y1] [--t T]` makes the hook readable at frame 0: holds the first frame where the headline is fully lit (auto-detected in the y0..y1 band, or set with --t) from 0.0 s, then plays on. Timing and audio unchanged; audio normalised to -14 LUFS if it's off by more than 1 LU. Cyan lines don't count as bright in the auto-detect, so set --t by eye when the hook's second line is cyan.
- `recap.py spec.json` re-captions a meme: upscales to 1080x1920, one fully opaque plate over the old burned-in captions, new Poppins Bold 56 px lines per segment, AI tag, logo, -14 LUFS. Spec: src, out, plate [x0,y0,x1,y1], segments [[t0,t1,"text"]], ai, logo_y. Use   to keep words together.
- `common.py` helpers, including `norm_audio` (gain plus limiter, iterated to -14 LUFS).

Recolouring a pink element to cyan or grey on a still: remap pixels by how far R exceeds G against the strongest pink sample (see the 14 Nov PR). On video, crop the strip, geq-recolour pixels where r-g > 25, overlay back.
