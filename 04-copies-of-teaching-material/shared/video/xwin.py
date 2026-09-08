#!/usr/bin/env python3
"""Find, move and raise X11 windows without xdotool (not installed here)."""
import time, subprocess, os
from Xlib import display, X

D = ":1"


def _dpy():
    return display.Display(D)


def _toplevels(d):
    return d.screen().root.query_tree().children


def _names(w):
    out = []
    try:
        n = w.get_wm_name()
        if n:
            out.append(n)
    except Exception:
        pass
    try:
        for c in w.query_tree().children:
            out += _names(c)
    except Exception:
        pass
    return out


def _client(w, pat, depth=0):
    """The application's own window, not the frame mutter wraps around it.

    A ConfigureRequest sent to the frame is ignored; sent to the client it is
    honoured and the frame follows. Clients are identified by WM_CLASS.
    """
    try:
        cls = w.get_wm_class()
        n = w.get_wm_name() or ""
        g = w.get_geometry()
    except Exception:
        return None
    # mutter's frame window carries a WM_CLASS and the app's own title, but a
    # ConfigureRequest sent to it is ignored -- always descend past it.
    if cls and "mutter-x11-frames" not in cls[0]:
        if pat in n.lower() and g.width > 60 and g.height > 40:
            return w
    try:
        for c in w.query_tree().children:
            r = _client(c, pat, depth + 1)
            if r is not None:
                return r
    except Exception:
        pass
    return None


def find_client(pat, timeout=25):
    pat = pat.lower()
    end = time.time() + timeout
    while time.time() < end:
        d = _dpy()
        for w in _toplevels(d):
            r = _client(w, pat)
            if r is not None:
                return r, d
        time.sleep(0.4)
    return None, None


def find(pat, timeout=25):
    """Top-level window whose own title, or any descendant's, contains pat."""
    pat = pat.lower()
    end = time.time() + timeout
    while time.time() < end:
        d = _dpy()
        for w in _toplevels(d):
            try:
                g = w.get_geometry()
                if g.width < 60 or g.height < 40:
                    continue
                if any(pat in n.lower() for n in _names(w)):
                    return w, d
            except Exception:
                pass
        time.sleep(0.4)
    return None, None


def place(pat, x, y, w=None, h=None, offset=(0, 0), timeout=25, center=True):
    """Move (and optionally resize) a window into a stage slot.

    Fixed-size windows such as turtlesim ignore the resize; they are centred in
    the slot instead, which is why the slot rectangle is passed in full.
    """
    win, d = find(pat, timeout)
    if win is None:
        print(f"  !! no window matching {pat!r}")
        return None
    ox, oy = offset
    try:
        if w and h:
            win.configure(x=ox + x, y=oy + y, width=w, height=h)
            d.sync(); time.sleep(0.6)
        g = win.get_geometry()
        if center and w and h and (g.width != w or g.height != h):
            cx = ox + x + max(0, (w - g.width) // 2)
            cy = oy + y + max(0, (h - g.height) // 2)
            win.configure(x=cx, y=cy)
        elif not (w and h):
            win.configure(x=ox + x, y=oy + y)
        d.sync(); time.sleep(0.4)
    except Exception as e:
        print(f"  !! place {pat}: {e}")
    return win


def raise_(pat, activate=False):
    d = _dpy()
    root = d.screen().root
    net_active = d.intern_atom("_NET_ACTIVE_WINDOW")
    pat = pat.lower()
    for w in _toplevels(d):
        try:
            if not any(pat in n.lower() for n in _names(w)):
                continue
            w.configure(stack_mode=X.Above)
            if activate:
                ev = display.event.ClientMessage(
                    window=w, client_type=net_active,
                    data=(32, [2, X.CurrentTime, 0, 0, 0]))
                root.send_event(ev, event_mask=X.SubstructureRedirectMask |
                                X.SubstructureNotifyMask)
            d.sync()
        except Exception:
            pass
    time.sleep(0.5)


def park_pointer(x=4300, y=2700):
    try:
        d = _dpy(); d.screen().root.warp_pointer(x, y); d.sync()
    except Exception:
        pass


def undecorate(pat):
    """Strip the title bar via Motif hints, so the app windows sit flush in
    their slots like the terminals do."""
    win, d = find_client(pat, timeout=10)
    if win is None:
        return
    a = d.intern_atom("_MOTIF_WM_HINTS")
    try:
        win.change_property(a, a, 32, [2, 0, 0, 0, 0])
        d.sync()
    except Exception:
        pass
    time.sleep(0.6)


def place_dev(pat, dx, dy, dw=None, dh=None, timeout=25, center=True):
    """Position a window using device pixels. GTK apps here run at 2x, so
    their size comes from --geometry (logical) and only the position is set."""
    win, d = find_client(pat, timeout)
    if win is None:
        print(f"  !! no window matching {pat!r}")
        return None
    try:
        if dw and dh:
            g = win.get_geometry()
            if abs(g.width - dw) > 4 or abs(g.height - dh) > 4:
                win.configure(width=dw, height=dh)
                d.sync(); time.sleep(0.5)
        g = win.get_geometry()
        x, y = dx, dy
        if center and dw and dh:
            x += max(0, (dw - g.width) // 2)
            y += max(0, (dh - g.height) // 2)
        win.configure(x=x, y=y)
        d.sync(); time.sleep(0.35)
    except Exception as e:
        print(f"  !! place_dev {pat}: {e}")
    return win


def geom(pat):
    win, d = find_client(pat, timeout=6)
    if win is None:
        return None
    g = win.get_geometry()
    return (g.x, g.y, g.width, g.height)


def _walk(w, out):
    try:
        out.append(w)
        for c in w.query_tree().children:
            _walk(c, out)
    except Exception:
        pass


def clients_of(cls_pat):
    """Every real client window whose WM_CLASS matches, as {id: window}.

    Used to tell a window this script opened apart from one the user already
    had open -- VS Code windows all share the class 'code'.
    """
    d = _dpy()
    all_w = []
    _walk(d.screen().root, all_w)
    hits = {}
    for w in all_w:
        try:
            c = w.get_wm_class()
            g = w.get_geometry()
        except Exception:
            continue
        if not c or "mutter-x11-frames" in c[0]:
            continue
        if cls_pat.lower() in (c[0] + " " + c[1]).lower() and g.width > 300 and g.height > 200:
            hits[w.id] = w
    return hits


def wait_new_client(cls_pat, before, timeout=60):
    """Block until a client of this class appears that was not there before."""
    end = time.time() + timeout
    while time.time() < end:
        now = clients_of(cls_pat)
        new = [w for i, w in now.items() if i not in before]
        if new:
            new.sort(key=lambda w: w.get_geometry().width * w.get_geometry().height)
            return new[-1]
        time.sleep(0.8)
    return None


def place_win(win, dx, dy, dw=None, dh=None, center=True, tries=4):
    """Move and size a window, verifying afterwards.

    Electron and Qt both ignore a ConfigureRequest that arrives while they are
    still laying out, so the request is repeated until the window lands.
    """
    d = _dpy()
    for attempt in range(tries):
        try:
            if dw and dh:
                g = win.get_geometry()
                if abs(g.width - dw) > 4 or abs(g.height - dh) > 4:
                    win.configure(width=dw, height=dh)
                    d.sync(); time.sleep(0.9)
            g = win.get_geometry()
            x, y = dx, dy
            if center and dw and dh:
                x += max(0, (dw - g.width) // 2)
                y += max(0, (dh - g.height) // 2)
            win.configure(x=x, y=y)
            d.sync(); time.sleep(0.6)
            ax, ay, aw, ah = abs_geom(win)
            if abs(ax - x) <= 6 and abs(ay - y) <= 6:
                return
        except Exception as e:
            print(f"  !! place_win: {e}")
            return
    print(f"  ~~ window settled at {abs_geom(win)}, wanted {dx},{dy}")


def raise_win(win):
    try:
        d = _dpy()
        win.configure(stack_mode=X.Above)
        d.sync()
    except Exception:
        pass
    time.sleep(0.3)


def undecorate_win(win):
    try:
        d = _dpy()
        a = d.intern_atom("_MOTIF_WM_HINTS")
        win.change_property(a, a, 32, [2, 0, 0, 0, 0])
        d.sync()
    except Exception:
        pass
    time.sleep(0.5)


def abs_geom(win):
    d = _dpy()
    g = win.get_geometry()
    t = win.translate_coords(d.screen().root, 0, 0)
    return (-t.x, -t.y, g.width, g.height)
