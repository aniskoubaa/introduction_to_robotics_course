#!/usr/bin/env python3
"""Trim the dead space off terminal captures.

A terminal is sized in whole rows and columns, so a short command leaves a block
of empty background below its output. On a slide that empty block is what gets
scaled to fit, which shrinks the text that matters. This crops back to the last
row that has any content, keeping a small margin.

Only touches the dark terminal captures; GUI windows (turtlesim, Gazebo) are
left alone.
"""
import sys, os, glob
from PIL import Image, ImageChops

MARGIN = 14          # px of background kept below the last line of output
DARK = (28, 28, 34)  # the terminal background from the terminator profile


def is_terminal(im):
    """Terminal captures are overwhelmingly the profile background colour."""
    px = im.convert("RGB").resize((40, 40)).getdata()
    close = sum(1 for r, g, b in px
                if abs(r - DARK[0]) < 12 and abs(g - DARK[1]) < 12 and abs(b - DARK[2]) < 12)
    return close > len(px) * 0.5


def trim(path):
    im = Image.open(path).convert("RGB")
    if not is_terminal(im):
        return None
    bg = Image.new("RGB", im.size, DARK)
    diff = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 26 else 0)
    box = diff.getbbox()
    if not box:
        return None
    left, upper, right, lower = box
    # keep the full width (columns are meaningful), trim only vertically
    lower = min(im.height, lower + MARGIN)
    upper = max(0, upper - MARGIN // 2)
    if lower - upper >= im.height - 4:
        return None
    out = im.crop((0, upper, im.width, lower))
    out.save(path)
    return im.size, out.size


if __name__ == "__main__":
    for p in sorted(glob.glob(sys.argv[1])):
        r = trim(p)
        n = os.path.basename(p)
        print(f"  {n:34s} {'%dx%d -> %dx%d' % (*r[0], *r[1]) if r else 'left alone'}")
