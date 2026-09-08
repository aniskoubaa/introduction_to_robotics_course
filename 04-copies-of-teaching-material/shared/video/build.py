#!/usr/bin/env python3
"""Assembles the finished film: opening card, then each chapter card followed
by its recording, then the closing card. One re-encode, silent audio track."""
import os, subprocess, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scenes

V = os.path.dirname(os.path.abspath(__file__))
CLIPS, CARDS, OUT = (os.path.join(V, d) for d in ("clips", "cards", "out"))
FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
FFPROBE = os.path.expanduser("~/.local/bin/ffprobe")
CARD_SECS = 4.0
OPEN_SECS = 6.0

# If the voice track exists, every card is held long enough to be read aloud.
try:
    DURS = json.load(open(os.path.join(V, "voice", "durations.json")))
except Exception:
    DURS = {}


def card_secs(nid, floor):
    d = DURS.get(nid, 0.0)
    return round(max(floor, d + 1.4), 2) if d else floor


def dur(p):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", p], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def card_clip(png, secs, out):
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error",
                    "-loop", "1", "-framerate", "24", "-t", str(secs), "-i", png,
                    "-vf", "scale=1920:1080,format=yuv420p",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                    "-r", "24", "-y", out], check=True)
    return out


def main():
    os.makedirs(os.path.join(V, "seq"), exist_ok=True)
    seq, chapters_log = [], []

    timeline = []
    d_open = card_secs("open", OPEN_SECS)
    op = card_clip(os.path.join(CARDS, "00_open.png"), d_open,
                   os.path.join(V, "seq", "00_open.mp4"))
    seq.append(op)
    timeline.append({"kind": "card", "nid": "open", "start": 0.0, "dur": d_open})
    t = d_open

    for i, ch in enumerate(scenes.CHAPTERS, 1):
        clip = os.path.join(CLIPS, f"{ch['id']}.mp4")
        if not os.path.exists(clip) or dur(clip) < 3:
            print(f"  -- {ch['id']}: no usable clip, skipped")
            continue
        card = os.path.join(CARDS, f"{i:02d}_{ch['id']}.png")
        d_card = card_secs(f"card:{ch['id']}", CARD_SECS)
        cc = card_clip(card, d_card, os.path.join(V, "seq", f"{i:02d}_card.mp4"))
        seq += [cc, clip]
        chapters_log.append((t, ch["title"], ch["id"]))
        timeline.append({"kind": "card", "nid": f"card:{ch['id']}",
                         "start": round(t, 3), "dur": d_card})
        timeline.append({"kind": "clip", "chapter": ch["id"], "clip": clip,
                         "start": round(t + d_card, 3), "dur": round(dur(clip), 3)})
        t += d_card + dur(clip)

    d_close = card_secs("close", OPEN_SECS)
    cl = card_clip(os.path.join(CARDS, "99_close.png"), d_close,
                   os.path.join(V, "seq", "99_close.mp4"))
    seq.append(cl)
    timeline.append({"kind": "card", "nid": "close", "start": round(t, 3),
                     "dur": d_close})
    json.dump(timeline, open(os.path.join(OUT, "timeline.json"), "w"), indent=1)

    lst = os.path.join(V, "seq", "list.txt")
    with open(lst, "w") as f:
        for p in seq:
            f.write(f"file '{p}'\n")

    out = os.path.join(OUT, "EE414_W03_demo.mp4")
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error",
                    "-f", "concat", "-safe", "0", "-i", lst,
                    "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                    "-shortest",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "21",
                    "-pix_fmt", "yuv420p", "-r", "24",
                    "-c:a", "aac", "-b:a", "64k",
                    "-movflags", "+faststart", "-y", out], check=True)

    # Chapter marks, for the description or a YouTube upload.
    with open(os.path.join(OUT, "chapters.txt"), "w") as f:
        f.write("0:00  Week 3 — Live Demo\n")
        for sec, title, cid in chapters_log:
            f.write(f"{int(sec)//60}:{int(sec)%60:02d}  {title}\n")

    d = dur(out)
    print(f"\n{out}")
    print(f"  {int(d)//60} min {int(d)%60:02d} s   {os.path.getsize(out)/1e6:.1f} MB")
    print("\nchapters:")
    print(open(os.path.join(OUT, "chapters.txt")).read())


if __name__ == "__main__":
    main()
