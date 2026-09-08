#!/usr/bin/env python3
"""When does the caption strip change?

The narration has to land on the frame where the caption it belongs to appears.
Rather than trusting wall-clock arithmetic between the recorder and the shell
scripts, the times are read back out of the finished clip: the caption strip is
drawn by PIL and is perfectly static between `cap` calls, so a change in those
pixels is a caption change, to the frame.
"""
import os, subprocess, sys

FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
W, H = 240, 20          # the strip, downscaled; enough to see a text change
FPS = 10
CAP_Y, CAP_H = 928, 152


def changes(clip, fps=FPS, thresh=2.0):
    """Times in seconds where the caption strip changes."""
    p = subprocess.run(
        [FFMPEG, "-hide_banner", "-loglevel", "error", "-i", clip,
         "-vf", f"crop=1920:{CAP_H}:0:{CAP_Y},scale={W}:{H},format=gray",
         "-r", str(fps), "-f", "rawvideo", "-"],
        capture_output=True)
    buf, n = p.stdout, W * H
    frames = [buf[i:i + n] for i in range(0, len(buf) - n + 1, n)]
    out, prev = [], None
    for i, f in enumerate(frames):
        if prev is not None:
            d = sum(abs(a - b) for a, b in zip(f, prev)) / n
            if d > thresh:
                out.append(i / fps)
        prev = f
    return out, len(frames) / fps


def merge(times, gap=0.35):
    """A caption fades in over a frame or two; keep only the first of a run."""
    keep = []
    for t in times:
        if not keep or t - keep[-1] > gap:
            keep.append(t)
    return keep


if __name__ == "__main__":
    for clip in sys.argv[1:]:
        t, dur = changes(clip)
        m = merge(t)
        print(f"{os.path.basename(clip):10} {dur:6.1f}s  {len(m):2} caption changes: "
              + ", ".join(f"{x:.1f}" for x in m[:12]))
