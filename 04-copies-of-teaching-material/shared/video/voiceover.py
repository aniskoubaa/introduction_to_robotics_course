#!/usr/bin/env python3
"""Lays the spoken lines onto the finished film.

Each caption's moment is found twice over: the caption log written during the
recording gives the exact spacing between captions, and the first visible
change of the caption strip in the clip anchors that sequence to the video.
Nothing depends on the recorder's clock agreeing with the shell's.
"""
import array, json, os, subprocess, sys, wave
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import captiming

V = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(V, "out")
VOICE = os.path.join(V, "voice")
FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
RATE = 24000
LEAD = 0.35          # a caption appears, then the voice starts
MIN_GAP = 0.25       # never let two lines run into each other


def load_wav(path):
    with wave.open(path) as w:
        assert w.getframerate() == RATE and w.getnchannels() == 1
        return array.array("h", w.readframes(w.getnframes()))


def by_text():
    """caption source text -> wav path"""
    lines = json.load(open(os.path.join(V, "narration.json")))
    m = {}
    for ln in lines:
        p = os.path.join(VOICE, ln["id"].replace(":", "_") + ".wav")
        if not os.path.exists(p):
            continue
        m[ln["id"]] = p
        if ln.get("source"):
            m["src:" + ln["source"]] = p
    return m


def caption_times(clip, caplog):
    """[(clip_time, caption_text)] for one chapter."""
    rows = []
    for line in open(caplog):
        if "\t" not in line:
            continue
        t, say = line.rstrip("\n").split("\t", 1)
        rows.append((float(t), say.strip()))
    if not rows:
        return []
    hits, dur = captiming.changes(clip)
    hits = captiming.merge(hits)
    anchor = hits[0] if hits else 1.5
    t0 = rows[0][0]
    out = [(anchor + (t - t0), say) for t, say in rows]
    return [(t, s) for t, s in out if 0 <= t < dur]


def main():
    timeline = json.load(open(os.path.join(OUT, "timeline.json")))
    wavs = by_text()
    total = max(e["start"] + e["dur"] for e in timeline) + 2.0
    master = array.array("h", bytes(int(total * RATE) * 2))

    placed = missing = 0
    cursor = 0.0
    lags = []
    for e in timeline:
        cues = []
        if e["kind"] == "card":
            cues = [(0.6, e["nid"])]
        else:
            log = os.path.join(V, "caplog", f"{e['chapter']}.tsv")
            if os.path.exists(log):
                cues = [(t + LEAD, "src:" + s)
                        for t, s in caption_times(e["clip"], log)]
        for offset, key in cues:
            path = wavs.get(key)
            if not path:
                missing += 1
                continue
            pcm = load_wav(path)
            start = max(e["start"] + offset, cursor + MIN_GAP)
            i = int(start * RATE)
            if i + len(pcm) > len(master):
                master.extend(bytes((i + len(pcm) - len(master)) * 2))
            for k, v in enumerate(pcm):
                j = i + k
                x = master[j] + v
                master[j] = -32768 if x < -32768 else (32767 if x > 32767 else x)
            lag = start - (e["start"] + offset)
            lags.append((lag, e.get("chapter", e.get("nid")), key[:52]))
            cursor = start + len(pcm) / RATE
            placed += 1

    narr = os.path.join(OUT, "narration.wav")
    with wave.open(narr, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(master.tobytes())

    silent = os.path.join(OUT, "EE414_W03_demo.mp4")
    final = os.path.join(OUT, "EE414_W03_demo_narrated.mp4")
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error",
                    "-i", silent, "-i", narr,
                    "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                    "-shortest", "-movflags", "+faststart", "-y", final], check=True)
    lags.sort(reverse=True)
    worst = lags[0][0] if lags else 0
    over = sum(1 for l, _, _ in lags if l > 1.0)
    print(f"placed {placed} spoken lines, {missing} with no audio")
    print(f"sync: worst lag behind its caption {worst:.1f}s; {over} lines over 1.0s")
    for l, c, k in lags[:6]:
        print(f"   {l:5.1f}s  {c:4}  {k}")
    print(f"voice runs to {cursor/60:.1f} min; film is {total/60:.1f} min")
    print(final)


if __name__ == "__main__":
    main()
