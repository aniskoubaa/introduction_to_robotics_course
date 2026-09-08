#!/usr/bin/env python3
"""The stage window: one undecorated window filling the capture region.

It is a normal managed window, not override-redirect. Mutter keeps
override-redirect windows above everything, which would bury the terminals;
as an ordinary window it can be raised above the user's desktop and then have
the demo windows raised above it in turn.
"""
import json, os, sys, tkinter as tk
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import ImageTk
from Xlib import display as _xd
import frame
from stagecfg import DW, DH, RX, RY

STATE = sys.argv[1]
TITLE = "EE414STAGE"

root = tk.Tk()
root.title(TITLE)
root.withdraw()
root.geometry(f"{DW}x{DH}+{RX}+{RY}")
root.configure(bg="#0b0f13")
root.resizable(False, False)
lab = tk.Label(root, bd=0, highlightthickness=0, bg="#0b0f13")
lab.pack(fill="both", expand=True)
root.update_idletasks()

# Undecorate before it is ever mapped, so mutter never draws a title bar.
_d = _xd.Display()
_w = _d.create_resource_object("window", root.winfo_id())
_a = _d.intern_atom("_MOTIF_WM_HINTS")
_w.change_property(_a, _a, 32, [2, 0, 0, 0, 0])
for st in ("_NET_WM_STATE_SKIP_TASKBAR", "_NET_WM_STATE_SKIP_PAGER"):
    try:
        _w.change_property(_d.intern_atom("_NET_WM_STATE"), 4, 32,
                           [_d.intern_atom(st)], mode=1)
    except Exception:
        pass
_d.sync()

root.deiconify()
root.update()
root.geometry(f"{DW}x{DH}+{RX}+{RY}")

_last = _basekey = _base = _photo = None


def tick():
    global _last, _base, _basekey, _photo
    try:
        s = json.load(open(STATE))
    except Exception:
        s = {"layout": "term"}
    if s != _last:
        _last = s
        k = (s.get("chapter"), s.get("layout"), s.get("pg"),
             json.dumps(s.get("labels", {}), sort_keys=True))
        if k != _basekey:
            _basekey, _base = k, frame.base(s)
        _photo = ImageTk.PhotoImage(frame.render(s, _base))
        lab.configure(image=_photo)
    root.after(100, tick)


tick()
root.mainloop()
