"""Draws the stage: dark ground, header, slot frames, caption strip.

Typeset with IBM Plex, the same superfamily as the printed cue sheet, so the
video and the page look like one piece of material.
"""
import os
from PIL import Image, ImageDraw, ImageFont
from stagecfg import *          # noqa: F403

_VF = os.path.join(FONTS, "IBMPlexSans-VF.ttf")
_MO = os.path.join(FONTS, "IBMPlexMono-Regular.ttf")
_MB = os.path.join(FONTS, "IBMPlexMono-SemiBold.ttf")
_cache = {}


def sans(px, weight=400):
    k = ("s", px, weight)
    if k not in _cache:
        f = ImageFont.truetype(_VF, px * S)
        try:
            f.set_variation_by_axes([weight, 100])
        except Exception:
            pass
        _cache[k] = f
    return _cache[k]


def mono(px, bold=False):
    k = ("m", px, bold)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(_MB if bold else _MO, px * S)
    return _cache[k]


def _track(d, xy, text, font, fill, extra=0):
    """Draw with letter-spacing, which PIL has no option for."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill, anchor="ls")
        x += d.textlength(ch, font=font) + extra * S
    return x


def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) > width and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def base(state):
    """Header, ground and slot frames -- everything that does not change
    between commands within one scene."""
    img = Image.new("RGB", (DW, DH), BG)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, DW, HEADER_H * S], fill=PANEL)
    d.line([0, HEADER_H * S, DW, HEADER_H * S], fill=LINE, width=S)
    bl = int((HEADER_H * 0.63)) * S
    e = _track(d, (PAD * S + 2, bl), "EE 414", sans(17, 600), ACCENT, 1.2)
    d.line([e + 16 * S, 17 * S, e + 16 * S, (HEADER_H - 17) * S], fill=LINE, width=S)
    d.text((e + 32 * S, bl), state.get("chapter", ""), font=sans(26, 600),
           fill=INK, anchor="ls")

    pg = state.get("pg", "")
    if pg:
        f = mono(17, True)
        tw = d.textlength(pg, font=f)
        x1 = DW - PAD * S
        x0 = x1 - tw - 26 * S
        d.rounded_rectangle([x0, 14 * S, x1, (HEADER_H - 14) * S], radius=5 * S,
                            fill=(24, 39, 50), outline=LINE, width=S)
        d.text(((x0 + x1) / 2, bl - 1 * S), pg, font=f, fill=ACCENT, anchor="ms")

    labels = state.get("labels", {})
    for key, r in slot(state.get("layout", "term")).items():
        x, y, w, h = dev(r)
        d.rectangle([x - S, y - S, x + w + S, y + h + S], fill=PANEL, outline=LINE,
                    width=S)
        lab = labels.get(key)
        if lab:
            _track(d, (x + 2 * S, y - 13 * S), lab.upper(), sans(13, 600), MUTE, 1.0)
    return img


def render(state, base_img=None):
    img = (base_img or base(state)).copy()
    d = ImageDraw.Draw(img)
    cy = (H - CAPTION_H) * S
    d.rectangle([0, cy, DW, DH], fill=PANEL)
    d.line([0, cy, DW, cy], fill=LINE, width=S)
    d.rectangle([0, cy, 5 * S, DH], fill=ACCENT)

    x = (PAD + 12) * S
    y = cy + 44 * S
    cmd = state.get("cmd", "")
    if cmd:
        f = mono(24, True)
        d.text((x, y), "$", font=f, fill=GREEN, anchor="ls")
        d.text((x + 26 * S, y), cmd, font=f, fill=AMBER, anchor="ls")
        y += 44 * S
    say = state.get("say", "")
    if say:
        f = sans(23)
        for i, ln in enumerate(wrap(d, say, f, DW - 2 * (PAD + 12) * S)[:2]):
            d.text((x, y + i * 30 * S), ln, font=f, fill=INK if i == 0 else MUTE,
                   anchor="ls")
    return img
