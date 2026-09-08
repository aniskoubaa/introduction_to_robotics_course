"""Stage geometry.

Everything is written in design units (a 1920x1080 frame). The desktop runs at
2x, so the capture region is twice that and ffmpeg scales the result back down
to 1080p -- which is why the text in the finished video is sharp.
"""
import os

S = 2                                    # device pixels per design pixel
W, H = 1920, 1080                        # design
DW, DH = W * S, H * S                    # device / capture region
SCREEN_W, SCREEN_H = 4384, 2740
RX, RY = (SCREEN_W - DW) // 2, (SCREEN_H - DH) // 2

HEADER_H  = 62
CAPTION_H = 152
PAD       = 22
GAP       = 44        # vertical gap between stacked windows

STAGE_Y = HEADER_H + PAD
STAGE_H = H - CAPTION_H - PAD - STAGE_Y
STAGE_X = PAD
STAGE_W = W - 2 * PAD

BG     = (11, 15, 19)
PANEL  = (17, 24, 31)
LINE   = (36, 50, 62)
INK    = (233, 238, 242)
MUTE   = (140, 157, 172)
ACCENT = (79, 179, 217)
AMBER  = (224, 164, 88)
GREEN  = (127, 191, 106)

FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")


def slot(name):
    x, y, w, h = STAGE_X, STAGE_Y, STAGE_W, STAGE_H
    if name == "term":
        return {"term": (x, y, w, h)}
    if name == "term_sim":
        tw = 1170
        return {"term": (x, y, tw, h), "sim": (x + tw + PAD, y, w - tw - PAD, h)}
    if name == "term2_sim":
        tw, top = 1170, 250
        return {"node": (x, y, tw, top),
                "term": (x, y + top + GAP, tw, h - top - GAP),
                "sim":  (x + tw + PAD, y, w - tw - PAD, h)}
    if name == "term2":
        top = 250
        return {"node": (x, y, w, top), "term": (x, y + top + GAP, w, h - top - GAP)}
    if name == "code":
        return {"code": (x, y, w, h)}
    if name == "code_term":
        cw = 1100
        return {"code": (x, y, cw, h), "term": (x + cw + PAD, y, w - cw - PAD, h)}
    if name == "code_term2":                 # editor, the node, and commands
        cw, top = 1060, 232
        rx, rw = x + cw + PAD, w - cw - PAD
        return {"code": (x, y, cw, h),
                "node": (rx, y, rw, top),
                "term": (rx, y + top + GAP, rw, h - top - GAP)}
    if name == "gz_scene":                   # launch log, commands, simulator
        tw, top = 980, 232
        return {"node": (x, y, tw, top),
                "term": (x, y + top + GAP, tw, h - top - GAP),
                "sim":  (x + tw + PAD, y, w - tw - PAD, h)}
    if name == "gz":
        return {"sim": (x, y, w, h)}
    raise KeyError(name)


def dev(r):
    """design rect -> device rect"""
    return tuple(v * S for v in r)
