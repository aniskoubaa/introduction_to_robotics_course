#!/usr/bin/env python3
"""Title cards: the opening frame, one card per chapter, and the closing frame.

Same palette and the same IBM Plex as the stage, so the cards read as part of
the recording rather than something bolted on afterwards.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import frame as F
from stagecfg import BG, PANEL, LINE, INK, MUTE, ACCENT, AMBER, GREEN, DW, DH, S
import scenes

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cards")
DECKS = {"A": "Deck A — Communication Models",
         "B": "Deck B — Your Own Packages and Interfaces"}


def _new():
    img = Image.new("RGB", (DW, DH), BG)
    return img, ImageDraw.Draw(img)


def _rule(d, x, y, h):
    d.rectangle([x, y, x + 5 * S, y + h], fill=ACCENT)


def opening(n_chapters, n_cmds):
    img, d = _new()
    x = 150 * S
    _rule(d, x - 34 * S, 300 * S, 300 * S)
    F._track(d, (x, 330 * S), "EE 414 · INTRODUCTION TO ROBOTICS", F.sans(24, 600),
             ACCENT, 3.0)
    d.text((x, 452 * S), "Week 3 — Live Demo", font=F.sans(84, 600), fill=INK,
           anchor="ls")
    d.text((x, 530 * S), "Nodes, topics, services, actions, parameters,",
           font=F.sans(36), fill=MUTE, anchor="ls")
    d.text((x, 582 * S), "and building two packages of your own.",
           font=F.sans(36), fill=MUTE, anchor="ls")

    d.line([x, 660 * S, (DW // S - 150) * S, 660 * S], fill=LINE, width=S)
    rows = [("Every command", f"{n_cmds} commands, run live on ROS 2 Jazzy"),
            ("Where they come from", "EE414_W03_demo_cue_sheet.html, in slide order"),
            ("What you see", f"{n_chapters} chapters — turtlesim, Gazebo, "
                             "the editor and four terminals")]
    y = 720 * S
    for k, v in rows:
        F._track(d, (x, y), k.upper(), F.sans(17, 600), AMBER, 1.4)
        d.text((x + 330 * S, y), v, font=F.sans(26), fill=INK, anchor="ls")
        y += 58 * S
    d.text((x, 1010 * S), "Alfaisal University · Fall 2026",
           font=F.sans(22), fill=MUTE, anchor="ls")
    return img


def chapter(ch, idx, total):
    img, d = _new()
    x = 150 * S
    _rule(d, x - 34 * S, 380 * S, 210 * S)
    F._track(d, (x, 412 * S), DECKS[ch["deck"]].upper(), F.sans(21, 600), ACCENT, 2.6)
    d.text((x, 510 * S), ch["title"], font=F.sans(66, 600), fill=INK, anchor="ls")
    for i, ln in enumerate(F.wrap(d, ch.get("blurb", ""), F.sans(30),
                                  DW - 2 * 150 * S)[:2]):
        d.text((x, 572 * S + i * 42 * S), ln, font=F.sans(30), fill=MUTE, anchor="ls")

    cmds, seen = [], set()
    for lab, kind, secs, cmd, say in ch["steps"] + ch.get("node_steps", []):
        if kind in ("beat", "files") or not cmd or cmd in seen:
            continue
        seen.add(cmd)
        cmds.append(cmd)
    y = 706 * S
    d.line([x, y - 34 * S, (DW // S - 150) * S, y - 34 * S], fill=LINE, width=S)
    for c in cmds[:6]:
        d.text((x, y), "$", font=F.mono(21, True), fill=GREEN, anchor="ls")
        shown = c if len(c) <= 94 else c[:93] + "\u2026"
        d.text((x + 26 * S, y), shown, font=F.mono(21), fill=INK, anchor="ls")
        y += 42 * S
    if len(cmds) > 6:
        d.text((x + 26 * S, y), f"+ {len(cmds) - 6} more", font=F.sans(21),
               fill=MUTE, anchor="ls")

    tag = f"{idx} / {total}"
    d.text((DW - 150 * S, 412 * S), tag, font=F.mono(21, True), fill=MUTE, anchor="rs")
    return img


def closing():
    img, d = _new()
    x = 150 * S
    _rule(d, x - 34 * S, 380 * S, 190 * S)
    F._track(d, (x, 412 * S), "END OF THE WEEK 3 DEMO", F.sans(21, 600), ACCENT, 2.6)
    d.text((x, 512 * S), "What you should be able to do now",
           font=F.sans(58, 600), fill=INK, anchor="ls")
    items = [
        "Ask any node what it offers, with one command.",
        "Tell a topic, a service and an action apart, and say why each exists.",
        "Write a .msg and a .srv file, build them, and use them from a node.",
        "Recognise the deadlock: a callback that waits never returns.",
        "Read and change a parameter while the node keeps running.",
    ]
    y = 620 * S
    for i, it in enumerate(items, 1):
        d.text((x, y), f"{i}", font=F.mono(24, True), fill=AMBER, anchor="ls")
        d.text((x + 44 * S, y), it, font=F.sans(28), fill=INK, anchor="ls")
        y += 56 * S
    d.line([x, y + 4 * S, (DW // S - 150) * S, y + 4 * S], fill=LINE, width=S)
    d.text((x, y + 62 * S), "The runbook for every command in this video:",
           font=F.sans(24), fill=MUTE, anchor="ls")
    d.text((x, y + 104 * S), "week03/ros2_lab/EE414_W03_demo_cue_sheet.html",
           font=F.mono(26, True), fill=ACCENT, anchor="ls")
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    chs = scenes.CHAPTERS
    n_cmds = sum(1 for c in chs for s in c["steps"] + c.get("node_steps", [])
                 if s[1] not in ("beat", "files"))
    made = []

    def save(img, name):
        p = os.path.join(OUT, name + ".png")
        img.resize((DW // S, DH // S), Image.LANCZOS).save(p)
        made.append(p)

    save(opening(len(chs), n_cmds), "00_open")
    for i, ch in enumerate(chs, 1):
        save(chapter(ch, i, len(chs)), f"{i:02d}_{ch['id']}")
    save(closing(), "99_close")
    for p in made:
        print(" ", os.path.basename(p))


if __name__ == "__main__":
    main()
