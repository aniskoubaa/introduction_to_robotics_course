#!/usr/bin/env python3
"""Orchestration helpers: environments, window launching, ffmpeg recording."""
import os, sys, json, time, signal, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stagecfg as C
import xwin

V     = os.path.dirname(os.path.abspath(__file__))
# The throwaway home the demo runs in. It sits outside the scratchpad on
# purpose: `ros2 pkg create` echoes its destination directory, and the
# scratchpad path carries the real user name.
HOME  = "/tmp/ee414home"
STATE = os.path.join(V, "stage.json")
CLIPS = os.path.join(V, "clips")
FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
ANACONDA = "/home/alfaisalx/anaconda3/bin/python3"

_procs = []

# Where the stage window actually landed. Mutter will not place a managed
# window under the top bar, so the capture region is read back from the stage
# rather than assumed, and every slot is positioned relative to it.
ORIGIN = [C.RX, C.RY]


def base_env(demo_home=True):
    """Environment for anything launched into the recording.

    Snap GTK paths and snap libraries are stripped (they kill GUI apps started
    from this session) and anaconda is removed from PATH (it breaks the
    rosidl generator). HOME points at a throwaway home so no real path or user
    name can appear on screen.
    """
    e = dict(os.environ)
    for k in ("LOCPATH", "GTK_PATH", "GTK_EXE_PREFIX", "GTK_IM_MODULE_FILE",
              "GIO_MODULE_DIR", "GSETTINGS_SCHEMA_DIR", "PYTHONPATH",
              "PYTHONHOME", "CONDA_PREFIX", "CONDA_DEFAULT_ENV"):
        e.pop(k, None)
    e["XDG_DATA_DIRS"] = "/usr/local/share:/usr/share"
    e["PATH"] = ":".join(p for p in e.get("PATH", "").split(":")
                         if p and "anaconda3" not in p)
    e["LD_LIBRARY_PATH"] = ":".join(p for p in e.get("LD_LIBRARY_PATH", "").split(":")
                                    if p and not p.startswith("/snap/"))
    e["DISPLAY"] = ":1"
    # `ros2 pkg create` prints getpass.getuser() as the maintainer.
    e["USER"] = e["LOGNAME"] = e["USERNAME"] = "ee414"
    e["HOSTNAME"] = "ros2"
    e["GDK_SCALE"] = "2"          # GTK apps draw at 2x; the region is 2x too
    e["GDK_DPI_SCALE"] = "1"
    e["XDG_CONFIG_HOME"] = os.path.join(V, "tcfg")
    e["STAGE_STATE"] = STATE
    if demo_home:
        e["HOME"] = HOME
    return e


def gui_env():
    """Same, but keeping the real HOME and anaconda (for the Tk stage)."""
    e = base_env(demo_home=False)
    e["PATH"] = "/home/alfaisalx/anaconda3/bin:" + e["PATH"]
    e.pop("XDG_CONFIG_HOME", None)
    return e


# ---------------------------------------------------------------- stage ----
def set_stage(log=False, **kw):
    try:
        s = json.load(open(STATE))
    except Exception:
        s = {}
    s.update(kw)
    json.dump(s, open(STATE, "w"))
    if log and os.environ.get("CAP_LOG"):
        with open(os.environ["CAP_LOG"], "a") as f:
            f.write(f"{time.time():.3f}\t{kw.get('say','')}\n")
    time.sleep(0.35)


def start_stage():
    set_stage(chapter="", layout="term", labels={}, pg="", cmd="", say="")
    p = subprocess.Popen([ANACONDA, os.path.join(V, "stage.py"), STATE],
                         env=gui_env(), start_new_session=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    _procs.append(p)
    time.sleep(3.0)
    raise_stage()
    win, d = xwin.find_client("EE414STAGE", timeout=8)
    if win is not None:
        x, y, w, h = xwin.abs_geom(win)
        ORIGIN[:] = [x, y]
        print(f"  stage region: {w}x{h}+{x}+{y}")
    return p


def raise_stage():
    """The stage sits above whatever the user had on screen; the demo windows
    are then raised above the stage."""
    xwin.raise_("EE414STAGE")
    win, d = xwin.find_client("EE414STAGE", timeout=6)
    if win is not None:
        xwin.place_win(win, C.RX, C.RY, C.DW, C.DH, center=False, tries=1)
        xwin.raise_win(win)


# ------------------------------------------------------------ terminals ----
def term(title, script_body, slot, profile="wide", env=None, cwd=None):
    """Open a borderless terminator in a stage slot running script_body."""
    x, y, w, h = slot
    path = os.path.join(V, f".sh_{title}.sh")
    with open(path, "w") as f:
        f.write(f"source {V}/env.sh\nsource {V}/drive.sh\n"
                f"cd {cwd or HOME}\nclear\n{script_body}\n")
    e = env or base_env()
    p = subprocess.Popen(
        ["terminator", "-p", profile, "-T", title, f"--geometry={w}x{h}",
         "-e", f"bash {path}"],
        env=e, start_new_session=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    _procs.append(p)
    xwin.place_dev(title, ORIGIN[0] + x * C.S, ORIGIN[1] + y * C.S, center=False)
    return p


def kill(p):
    try:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
    except Exception:
        pass


def killall():
    for p in _procs:
        kill(p)


# ------------------------------------------------------------- recording ---
class Rec:
    """ffmpeg x11grab over the stage region."""

    def __init__(self, name, fps=24):
        self.out = os.path.join(CLIPS, f"{name}.mp4")
        self.fps = fps
        self.p = None

    def __enter__(self):
        xwin.park_pointer()
        os.makedirs(CLIPS, exist_ok=True)
        self.p = subprocess.Popen(
            [FFMPEG, "-hide_banner", "-loglevel", "error",
             "-f", "x11grab", "-framerate", str(self.fps), "-draw_mouse", "0",
             "-video_size", f"{C.DW}x{C.DH}", "-i", f":1+{ORIGIN[0]},{ORIGIN[1]}",
             "-vf", "scale=1920:1080:flags=lanczos",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
             "-pix_fmt", "yuv420p", "-y", self.out],
            env=base_env(demo_home=False), stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True)
        time.sleep(1.2)
        return self

    def __exit__(self, *a):
        time.sleep(0.8)
        try:
            self.p.send_signal(signal.SIGINT)
            self.p.wait(timeout=25)
        except Exception:
            kill(self.p)
        return False


def kill_marked(marker, sig=signal.SIGTERM):
    """Kill processes this script started, found by a marker in their command
    line. Never matches this process, whose own command line has no marker."""
    me = os.getpid()
    safe = set()
    pid = me
    while pid > 1:                       # never kill an ancestor of this run
        safe.add(pid)
        try:
            pid = int(open(f"/proc/{pid}/stat").read().split(") ", 1)[1].split()[1])
        except Exception:
            break
    for pid in os.listdir("/proc"):
        if not pid.isdigit() or int(pid) in safe:
            continue
        try:
            cl = open(f"/proc/{pid}/cmdline", "rb").read().decode("utf8", "replace")
        except Exception:
            continue
        if marker in cl:
            try:
                os.kill(int(pid), sig)
            except Exception:
                pass


def start_code(folder, slot_rect, wait=45):
    """Open the editor on a folder, in a clean profile with no account, no
    telemetry and no git, and drop it into a stage slot."""
    before = xwin.clients_of("code")
    # Start from a pristine profile: an editor that was killed reopens with a
    # "window terminated unexpectedly" dialog over the code.
    shutil.rmtree(os.path.join(V, "vscode-user"), ignore_errors=True)
    shutil.copytree(os.path.join(V, "vscode-seed"), os.path.join(V, "vscode-user"))
    e = base_env()
    e["GDK_SCALE"] = "1"                 # Electron scales itself
    p = subprocess.Popen(
        ["/snap/bin/code", "--new-window",
         f"--user-data-dir={V}/vscode-user", f"--extensions-dir={V}/vscode-ext",
         "--disable-workspace-trust", "--force-device-scale-factor=2", folder],
        env=e, start_new_session=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    _procs.append(p)
    win = xwin.wait_new_client("code", before, timeout=wait)
    if win is None:
        print("  !! editor window never appeared")
        return None
    time.sleep(4)
    x, y, w, h = C.dev(slot_rect)
    xwin.place_win(win, ORIGIN[0] + x, ORIGIN[1] + y, w, h, center=False)
    return win


def kill_editor():
    """Close the editor for good.

    SIGTERM makes Electron treat it as a crash and reopen a recovery window,
    which sits above the stage for the rest of the recording. SIGKILL leaves
    nothing behind, and the profile is recreated from the seed next time.
    """
    kill_marked("vscode-user", signal.SIGKILL)
    for _ in range(20):
        time.sleep(0.4)
        if not xwin.clients_of("code"):
            break
