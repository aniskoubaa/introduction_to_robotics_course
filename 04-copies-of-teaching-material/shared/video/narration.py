#!/usr/bin/env python3
"""The spoken script.

One line per thing the viewer sees: the opening card, each chapter card, and
each command. The command lines are the cue sheet's own explanations, so the
narration, the caption on screen and the printed runbook all say the same
thing in the same words. The commands themselves are never read aloud -- they
are on screen, and read out they are unintelligible.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scenes

V = os.path.dirname(os.path.abspath(__file__))

OPEN = ("E E four one four, Introduction to Robotics. Week three, live demo. "
        "Every command you will see comes from the week three cue sheet, and every "
        "one of them is run for real on ROS 2 Jazzy.")

CLOSE = ("That is the end of the week three demo. "
         "You should now be able to ask any node what it offers with one command; "
         "tell a topic, a service and an action apart, and say why each one exists; "
         "write a message file and a service file, build them, and use them from a node; "
         "recognise the deadlock, where a callback that waits never returns; "
         "and read and change a parameter while the node keeps running. "
         "The runbook for every command in this video is the week three demo cue sheet.")


def speakable(t):
    """Small fixes so the reader does not stumble."""
    t = t.strip()
    t = re.sub(r"\bROS 2\b", "ROS two", t)
    t = re.sub(r"\bT(\d)\b", r"terminal \1", t)
    t = t.replace("--once", "dash dash once").replace("--feedback", "dash dash feedback")
    t = t.replace("-t ", "dash t ")
    t = re.sub(r"\s+", " ", t)
    if t and t[-1] not in ".!?":
        t += "."
    return t


def build():
    """Every caption the video puts on screen gets a spoken line.

    The audio is matched back to the video by caption text, not by position,
    so this list has to cover the node terminal's own caption and the editor
    file notes as well as the ordinary commands.
    """
    lines = [{"id": "open", "kind": "card", "text": OPEN}]
    seen = set()

    def add(lid, kind, source, chapter=None):
        t = speakable(source)
        if not t or t in seen:
            return
        seen.add(t)
        lines.append({"id": lid, "kind": kind, "text": t, "source": source.strip(),
                      "chapter": chapter})

    for ch in scenes.CHAPTERS:
        cid = ch["id"]
        lines.append({"id": f"card:{cid}", "kind": "card", "chapter": cid,
                      "text": speakable(f"{ch['title']}. {ch.get('blurb','')}")})
        n = 0
        for lab, kind, secs, cmd, say in ch.get("node_steps", []) + ch["steps"]:
            add(f"{cid}:{n}", "step", say, cid)
            n += 1
        for _path, note in ch.get("code_files", []):
            add(f"{cid}:{n}", "step", note, cid)
            n += 1
    lines.append({"id": "close", "kind": "card", "text": CLOSE})
    return lines


if __name__ == "__main__":
    lines = build()
    out = os.path.join(V, "narration.json")
    json.dump(lines, open(out, "w"), indent=1)
    words = sum(len(l["text"].split()) for l in lines)
    print(f"{len(lines)} lines, {words} words, about {words/2.6:.0f} s of speech")
    for l in lines[:6]:
        print(f"  [{l['id']:10}] {l['text'][:110]}")
