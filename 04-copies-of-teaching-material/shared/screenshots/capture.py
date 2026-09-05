#!/usr/bin/env python3
"""EE414 screenshot driver: run a command in a terminal, capture just its window."""
import subprocess, sys, time, os, shlex, signal
from Xlib import display

S = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(S, "shots")
os.makedirs(SHOTS, exist_ok=True)

_procs = []


def clean_env():
    """This session runs inside the VS Code snap, which exports LOCPATH and GTK
    paths pointing into /snap/core20. Anything launched with those inherited
    dies with `undefined symbol: __libc_pthread_init`. Strip them."""
    e = dict(os.environ)
    for k in ("LOCPATH", "GTK_PATH", "GTK_EXE_PREFIX", "GTK_IM_MODULE_FILE",
              "GIO_MODULE_DIR", "GSETTINGS_SCHEMA_DIR"):
        e.pop(k, None)
    e["XDG_DATA_DIRS"] = "/usr/local/share:/usr/share"
    e["LD_LIBRARY_PATH"] = ":".join(
        p for p in e.get("LD_LIBRARY_PATH", "").split(":")
        if p and not p.startswith("/snap/"))
    e["DISPLAY"] = ":1"
    return e


def find_window(pat, timeout=15, inner=True):
    """Locate a window by title substring.

    X11 gives us both the decorated frame and the content child. `inner` picks
    the content child so captures carry no title bar or window buttons.
    """
    d = display.Display()
    root = d.screen().root
    end = time.time() + timeout
    while time.time() < end:
        out = []

        def walk(w):
            try:
                for c in w.query_tree().children:
                    try:
                        n = c.get_wm_name()
                        g = c.get_geometry()
                        if n and pat.lower() in n.lower() and g.width > 200 and g.height > 150:
                            a = c.translate_coords(root, 0, 0)
                            out.append((-a.x, -a.y, g.width, g.height))
                    except Exception:
                        pass
                    walk(c)
            except Exception:
                pass

        walk(root)
        if out:
            out.sort(key=lambda t: t[2] * t[3])
            if inner and len(out) >= 2:
                return out[-2]      # content child, decorations excluded
            return out[-1]
        time.sleep(0.5)
    return None


def park_pointer():
    """Move the mouse off the capture area so no I-beam lands in a slide."""
    try:
        d = display.Display(); r = d.screen().root
        r.warp_pointer(4300, 2700); d.sync()
    except Exception:
        pass


def move_window(pat, x=40, y=40):
    """Drag a window fully on-screen before capturing it."""
    d = display.Display(); root = d.screen().root
    hits = []

    def walk(w):
        try:
            for c in w.query_tree().children:
                try:
                    n = c.get_wm_name()
                    if n and pat.lower() in n.lower():
                        hits.append(c)
                except Exception:
                    pass
                walk(c)
        except Exception:
            pass

    walk(root)
    for c in hits:
        try:
            c.configure(x=x, y=y); d.sync()
        except Exception:
            pass
    time.sleep(1.0)


def grab(geo, out):
    park_pointer()
    time.sleep(0.3)
    x, y, w, h = geo
    sw, sh = display.Display().screen().width_in_pixels, display.Display().screen().height_in_pixels
    x = max(0, x); y = max(0, y)
    w = min(w, sw - x); h = min(h, sh - y)
    w -= w % 2
    h -= h % 2
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "x11grab",
                    "-video_size", f"{w}x{h}", "-i", f":1+{x},{y}",
                    "-frames:v", "1", "-y", out], check=True, env=clean_env())
    return out


PROMPT = r'''show() {
  printf '\033[38;2;140;194;101m$\033[0m \033[1m%s\033[0m\n' "$*"
  eval "$@"
}
'''


def term_shot(name, cmd, cols=1400, rows=700, settle=4.0):
    """Run cmd in a fresh terminal, wait, capture that window, close it.

    Use show '<cmd>' inside cmd to echo a prompt line before running it, so the
    capture shows what the student types as well as what comes back.
    """
    title = f"EE414shot{name}"
    # terminator's -e mangles complex quoting, so stage the body as a script.
    script = os.path.join(S, f".shot_{name}.sh")
    with open(script, "w") as f:
        f.write(f"source {S}/rosenv.sh\n{PROMPT}\nclear\n{cmd}\necho\nsleep 900\n")
    p = subprocess.Popen(["terminator", f"--geometry={cols}x{rows}+120+120", "-T", title,
                          "-e", f"bash {script}"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True, env=clean_env())
    _procs.append(p)
    time.sleep(settle)
    geo = find_window(title)
    if not geo:
        print(f"  !! window not found for {name}")
        return None
    path = os.path.join(SHOTS, f"{name}.png")
    grab(geo, path)
    try:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
    except Exception:
        pass
    print(f"  OK {name}.png  {geo[2]}x{geo[3]}")
    return path


def raise_window(pat):
    """Bring a window to the front. x11grab captures screen regions, so an
    obscured window would otherwise be photographed as whatever sits on top."""
    from Xlib import X, Xatom
    d = display.Display(); root = d.screen().root
    net_active = d.intern_atom("_NET_ACTIVE_WINDOW")
    for c in root.query_tree().children:
        try:
            n = c.get_wm_name()
            if n and pat.lower() in n.lower():
                c.configure(stack_mode=X.Above)
                ev = display.event.ClientMessage(
                    window=c, client_type=net_active,
                    data=(32, [2, X.CurrentTime, 0, 0, 0]))
                root.send_event(ev, event_mask=X.SubstructureRedirectMask |
                                X.SubstructureNotifyMask)
                d.sync()
        except Exception:
            pass
    time.sleep(1.2)


def win_shot(name, pat, timeout=15, raise_first=True):
    """Capture an already-open window matching pat."""
    if raise_first:
        raise_window(pat)
    geo = find_window(pat, timeout=timeout)
    if not geo:
        print(f"  !! window not found: {pat}")
        return None
    path = os.path.join(SHOTS, f"{name}.png")
    grab(geo, path)
    print(f"  OK {name}.png  {geo[2]}x{geo[3]}")
    return path


def ros(cmd, timeout=30):
    """Run a ros2 command in the clean env, return stdout."""
    r = subprocess.run(["bash", "-c", f"source {S}/rosenv.sh; {cmd}"],
                       capture_output=True, text=True, timeout=timeout,
                       env=clean_env())
    return r.stdout + r.stderr
