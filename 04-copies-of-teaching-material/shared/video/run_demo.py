#!/usr/bin/env python3
"""Records the Week 3 screencast, one clip per chapter.

Nothing is typed by a human: each terminal runs a generated script that prints
the prompt itself, types the command out a character at a time and then runs
it. The output is real -- these are the cue sheet's commands against a live
ROS 2 system.
"""
import os, sys, time, json, shlex, shutil, subprocess, signal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rec, xwin, scenes
import stagecfg as C

V = rec.V
FLAGS = os.path.join(V, "flags")
WS = "/tmp/ee414home/ee414_ws"
q = shlex.quote

ONLY = set(sys.argv[1:])
CURRENT = [""]                       # chapter id, for the caption log filename


# How long each caption takes to narrate, if the voice track has been made.
try:
    DURS = json.load(open(os.path.join(V, "voice", "durations.json")))
except Exception:
    DURS = {}


def spoken(say):
    return DURS.get("src:" + (say or "").strip(), 0.0)


def pause_for(say, cmd, already=0.0):
    """Extra seconds to hold so the narration for this caption can finish.

    A step already spends 0.9 s showing the caption, then types the command,
    then runs it, then waits STEP_PAUSE. Only the remainder is added here.
    """
    d = spoken(say)
    if not d:
        return 0.0
    spent = 0.9 + len(cmd) * 0.022 + 1.8 + already
    return max(0.0, round(d + 1.0 - spent, 1))


def flag(name):
    return os.path.join(FLAGS, name)


def clear_flags():
    shutil.rmtree(FLAGS, ignore_errors=True)
    os.makedirs(FLAGS, exist_ok=True)


def flag_env(ch=None):
    e = rec.base_env()
    if ch is not None and ch.get("starts_sim"):
        e["QT_SCALE_FACTOR"] = "2.6"      # turtlesim is 500x500 at 1:1
    e["GO_FILE"] = flag("go")
    e["DONE_FILE"] = flag("done")
    e["READY_FILE"] = flag("ready")
    e["RESTART_FILE"] = flag("restart")
    e["HOST_FILE"] = flag("host")
    e["HOST_DONE"] = flag("hostdone")
    e["CAP_LOG"] = os.path.join(V, "caplog", f"{CURRENT[0]}.tsv")
    os.makedirs(os.path.dirname(e["CAP_LOG"]), exist_ok=True)
    os.environ["CAP_LOG"] = e["CAP_LOG"]
    return e


def wait_flag(name, timeout=600):
    end = time.time() + timeout
    while time.time() < end:
        if os.path.exists(flag(name)):
            return True
        time.sleep(0.3)
    return False


def sh(cmd, timeout=60):
    return subprocess.run(["bash", "-c", f"source {V}/env.sh; {cmd}"],
                          env=rec.base_env(), capture_output=True, text=True,
                          timeout=timeout)


# ------------------------------------------------------------- scripts ----
def main_script(ch):
    # Only wait for the other terminal when there actually is one; a chapter
    # that opens its own window signals readiness the other way round.
    needs_node = bool(ch.get("node_steps")) or any(s[1] == "shown" for s in ch["steps"])
    out = ["wait_go"] + (["wait_ready"] if needs_node else [])
    for lab, kind, secs, cmd, say in ch["steps"]:
        if kind == "shown":
            continue                       # the T4 terminal runs this one
        if kind == "sim":
            out.append(f"step_launch {q(lab)} {q(say)} {q(cmd)}")
            out.append(f"hold {max(secs or 10, pause_for(say, cmd, already=8)):.1f}")
        elif kind == "beat":
            out.append(f"beat {q(lab)} {q(say)} {max(secs or 3, spoken(say) + 1.2):.1f}")
        elif kind == "files":
            out.append(f"ask_host {q(lab)} {q(say)}")
        elif kind == "int":
            out.append(f"step_int {q(lab)} {q(say)} {secs} {q(cmd)}")
            extra = pause_for(say, cmd, already=secs)
            if extra:
                out.append(f"hold {extra}")
        elif kind == "restart":
            out.append(f"restart_node {q(lab)} {q(say)} {q(cmd)} "
                       f"{max(secs or 7, spoken(say) + 2):.0f}")
        else:
            out.append(f"step {q(lab)} {q(say)} {q(cmd)}")
            hold = max(secs, pause_for(say, cmd, already=secs))
            if hold:
                out.append(f"hold {hold}")
    out += ["sleep 2", "say_done", "sleep 900"]
    return "\n".join(out)


def node_script(ch):
    """The T4 / T3 terminal: start what has to stay running."""
    steps = ch.get("node_steps")
    ready = ch.get("node_ready_after", 5)
    if not steps:
        shown = [s for s in ch["steps"] if s[1] == "shown"]
        if not shown:
            return None
        lab, _, _, cmd, say = shown[0]
        restart = [s for s in ch["steps"] if s[1] == "restart"]
        ready = max(ready, spoken(say) + 2)
        out = ["wait_go",
               f"run_until {q(lab)} {q(say)} {q(flag('restart') if restart else flag('done'))} {ready} {q(cmd)}"]
        if restart:
            rlab, _, _, rcmd, rsay = restart[0]
            out.append(f"run_until {q(rlab)} {q(rsay)} {q(flag('done'))} 0 {q(rcmd)}")
        out.append("sleep 900")
        return "\n".join(out)

    out = ["wait_go"]
    for i, (lab, kind, secs, cmd, say) in enumerate(steps):
        last = i == len(steps) - 1
        if last:
            out.append(f"run_until {q(lab)} {q(say)} {q(flag('done'))} {ready} {q(cmd)}")
        else:
            out.append(f"step {q(lab)} {q(say)} {q(cmd)}")
    out.append("sleep 900")
    return "\n".join(out)


# --------------------------------------------------------------- pieces ----
SIM_PROC = [None]
GZ_PROC = [None]


def start_sim(slot):
    if SIM_PROC[0] is not None:
        return
    e = rec.base_env()
    e["QT_SCALE_FACTOR"] = "2.6"
    p = subprocess.Popen(["bash", "-c", f"source {V}/env.sh; exec ros2 run turtlesim turtlesim_node"],
                         env=e, start_new_session=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    SIM_PROC[0] = p
    rec._procs.append(p)
    time.sleep(7)
    xwin.undecorate("turtlesim")
    place_sim(slot)


def place_sim(slot):
    x, y, w, h = C.dev(slot)
    xwin.place_dev("turtlesim", rec.ORIGIN[0] + x, rec.ORIGIN[1] + y, None, None,
                   center=False)
    win, d = xwin.find_client("turtlesim", 6)
    if win:
        g = win.get_geometry()
        xwin.place_win(win, rec.ORIGIN[0] + x + max(0, (w - g.width) // 2),
                       rec.ORIGIN[1] + y + max(0, (h - g.height) // 2),
                       center=False, tries=2)


def place_gazebo(slot):
    x, y, w, h = C.dev(slot)
    win = None
    for pat in ("Gazebo", "gz sim", "Gazebo Sim"):
        win, d = xwin.find_client(pat, timeout=8)
        if win:
            break
    if not win:
        print("  !! Gazebo window not found")
        return
    xwin.undecorate_win(win)
    xwin.place_win(win, rec.ORIGIN[0] + x, rec.ORIGIN[1] + y, w, h, center=False)


def reset_turtlesim():
    sh("ros2 service call /kill turtlesim/srv/Kill \"{name: 'scout'}\"", 25)
    sh("ros2 service call /reset std_srvs/srv/Empty '{}'", 25)
    for ch_, v in (("r", 69), ("g", 86), ("b", 255)):
        sh(f"ros2 param set /turtlesim background_{ch_} {v}", 20)


# ------------------------------------------------------------- chapters ----
def run_chapter(ch):
    cid = ch["id"]
    CURRENT[0] = cid
    print(f"\n=== {cid}  {ch['title']} ===", flush=True)
    clear_flags()
    caplog = os.path.join(V, "caplog", f"{cid}.tsv")
    os.makedirs(os.path.dirname(caplog), exist_ok=True)
    open(caplog, "w").close()
    slots = C.slot(ch["layout"])
    labels = dict(ch["labels"])
    if ch.get("node_label") and "node" in labels:
        labels["node"] = ch["node_label"]

    rec.set_stage(chapter=ch["title"], layout=ch["layout"], labels=labels,
                  pg="", cmd="", say=ch.get("blurb", ""))
    rec.raise_stage()

    if ch.get("reset"):
        reset_turtlesim()

    # A chapter that finishes with turtlesim closes it first, so the terminal
    # that owns it cannot show through beside the new, narrower windows.
    if ch.get("stops_sim") and SIM_PROC[0]:
        rec.kill(SIM_PROC[0])
        SIM_PROC[0] = None
        time.sleep(1.5)

    env = flag_env(ch)
    profile = {"term": "wide", "term_sim": "narrow", "term2_sim": "narrow",
               "term2": "wide", "code_term": "small", "code_term2": "small",
               "gz_scene": "small"}[ch["layout"]]

    code_win = None
    if "code" in slots:
        code_win = rec.start_code(ch.get("code_folder", WS), slots["code"])
        # A chapter without a "files" step opens its file straight away, so the
        # editor is already showing the right thing when recording starts.
        if code_win and not any(s[1] == "files" for s in ch["steps"]):
            for path, _note in ch.get("code_files", []):
                subprocess.run(["/snap/bin/code", "--reuse-window",
                                f"--user-data-dir={V}/vscode-user",
                                f"--extensions-dir={V}/vscode-ext", path],
                               env={**rec.base_env(), "GDK_SCALE": "1"},
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(2.5)

    node_p = None
    ns = node_script(ch)
    if ns and "node" in slots:
        node_p = rec.term(f"{cid}_node", ns, slots["node"],
                          profile="small" if ch["layout"] == "gz_scene" else profile,
                          env=env, cwd="/tmp/ee414home")

    term_p = rec.term(f"{cid}_t2", main_script(ch), slots["term"], profile=profile,
                      env=env, cwd="/tmp/ee414home")

    # Raise everything above the stage, in a stable order.
    time.sleep(1.5)
    rec.raise_stage()
    if code_win:
        xwin.raise_win(code_win)
    if node_p:
        xwin.raise_(f"{cid}_node")
    xwin.raise_(f"{cid}_t2")
    if "sim" in slots and SIM_PROC[0]:
        place_sim(slots["sim"])
        xwin.raise_("turtlesim")
    xwin.park_pointer()
    time.sleep(1.0)

    with rec.Rec(cid):
        open(flag("go"), "w").close()
        if ch.get("starts_sim"):
            # turtlesim is started by the command typed in the terminal, so the
            # viewer sees the window open in response to it. That terminal owns
            # the process and is kept alive for the rest of Deck A.
            xwin.find_client("turtlesim", timeout=25)
            time.sleep(1.0)
            xwin.undecorate("turtlesim")
            place_sim(slots["sim"])
            xwin.raise_("turtlesim")
            xwin.park_pointer()
            SIM_PROC[0] = term_p
            open(flag("ready"), "w").close()
        elif ch.get("needs") and "gazebo" in ch["needs"]:
            time.sleep(ch.get("node_ready_after", 34))
            place_gazebo(slots["sim"])
            xwin.raise_("Gazebo")
            xwin.park_pointer()
        elif not node_p:
            open(flag("ready"), "w").close()

        if any(s[1] == "files" for s in ch["steps"]):
            host_files(ch, code_win)

        for nm in (f"{cid}_t2", f"{cid}_node", "turtlesim"):
            g = xwin.geom(nm)
            if g:
                print(f"   [{nm}] {g[2]}x{g[3]}+{g[0]}+{g[1]}"
                      f"  -> design {(g[0]-rec.ORIGIN[0])//2},{(g[1]-rec.ORIGIN[1])//2}",
                      flush=True)
        print(f"   ORIGIN {rec.ORIGIN}  stage {xwin.geom('EE414STAGE')}", flush=True)
        ok = wait_flag("done", timeout=900)
        if not ok:
            print("  !! chapter timed out")
        time.sleep(1.5)

    for p in (term_p, node_p):
        if p and not (p is SIM_PROC[0]):
            rec.kill(p)
    rec.kill_editor()
    time.sleep(1.5)


def host_files(ch, code_win):
    """Add the finished files to the package and show each one in the editor."""
    if not wait_flag("host", timeout=600):
        return
    src = os.path.join(V, "ref")
    for pkg in ("ee414_w03_interfaces", "ee414_w03_nodes"):
        dst = os.path.join(WS, "src", pkg)
        for root, dirs, files in os.walk(os.path.join(src, pkg)):
            rel = os.path.relpath(root, os.path.join(src, pkg))
            os.makedirs(os.path.join(dst, rel), exist_ok=True)
            for f in files:
                shutil.copy2(os.path.join(root, f), os.path.join(dst, rel, f))
    time.sleep(1.5)
    for path, note in ch.get("code_files", []):
        subprocess.run(["/snap/bin/code", "--reuse-window",
                        f"--user-data-dir={V}/vscode-user",
                        f"--extensions-dir={V}/vscode-ext", path],
                       env={**rec.base_env(), "GDK_SCALE": "1"},
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2.0)
        rec.set_stage(log=True, cmd=os.path.basename(path), say=note)
        if code_win:
            xwin.raise_win(code_win)
        xwin.park_pointer()
        time.sleep(max(6.5, spoken(note) + 1.5))
    open(flag("hostdone"), "w").close()


def main():
    rec.kill_editor()
    os.makedirs(FLAGS, exist_ok=True)
    rec.start_stage()

    chapters = [c for c in scenes.CHAPTERS if not ONLY or c["id"] in ONLY]
    for ch in chapters:
        if ch["id"] == "b1":
            shutil.rmtree(WS, ignore_errors=True)
            os.makedirs(os.path.join(WS, "src"), exist_ok=True)
        try:
            run_chapter(ch)
        except Exception as e:
            import traceback
            print(f"  !! {ch['id']} failed: {e}")
            traceback.print_exc()
        if ch.get("needs") and "gazebo" in ch["needs"]:
            rec.kill_marked("turtlebot3_world"); rec.kill_marked("gz sim")
            subprocess.run(["pkill", "-x", "ruby"], capture_output=True)
            subprocess.run(["pkill", "-x", "gzserver"], capture_output=True)
    rec.killall()
    print("\nclips:")
    for f in sorted(os.listdir(rec.CLIPS)):
        p = os.path.join(rec.CLIPS, f)
        print(f"  {f:16} {os.path.getsize(p)/1e6:7.1f} MB")


if __name__ == "__main__":
    main()
