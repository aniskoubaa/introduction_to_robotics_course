#!/usr/bin/env python3
"""
EE 414 -- setup check.

Run this AFTER installing, and bring the output to Week 2.

    python3 check_ros2_setup.py

Every row must say PASS. A row that says FAIL prints what to do about it; a row
that says WARN will not stop you working, but read it.

DESIGN NOTES -- read before editing.

  * NO third-party imports. This script runs on a machine where the student may
    have installed nothing successfully, and an ImportError from the checker
    itself is the worst possible first experience. Standard library only.

  * NO ros2 CLI calls for things that can be checked in-process. `import rclpy`
    is a stronger test than `ros2 --help`: it proves the Python bindings match
    the interpreter, which is the single most common real failure (a student on
    Ubuntu 24.04 running python3.11 from a conda env).

  * Every FAIL carries a FIX. A checker that says "rclpy: FAIL" and stops has
    told the student what they already knew.

  * Exit code is 0 only when nothing FAILed, so this can gate a lab script.
"""

import os
import platform
import shutil
import subprocess
import sys

# The pinned stack. These four values and the three lines in setup/README.md are
# the same fact; the beamer decks reach it through \rosver. Change all of them
# together or none of them.
ROS_DISTRO_EXPECTED = "jazzy"
UBUNTU_EXPECTED = "24.04"
PY_EXPECTED = (3, 12)
GAZEBO_EXPECTED = "Harmonic"

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"
results = []


def record(name, status, detail="", fix=""):
    results.append((name, status, detail, fix))


def run(cmd, timeout=15):
    """Return (ok, stdout+stderr). Never raises."""
    try:
        p = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
        return p.returncode == 0, (p.stdout + p.stderr).strip()
    except FileNotFoundError:
        return False, "command not found"
    except subprocess.TimeoutExpired:
        return False, f"timed out after {timeout}s"
    except Exception as exc:                       # pragma: no cover
        return False, f"{type(exc).__name__}: {exc}"


# ---------------------------------------------------------------------------
# 1. The platform underneath everything
# ---------------------------------------------------------------------------

def check_os():
    if platform.system() != "Linux":
        record("Operating system", FAIL, platform.system(),
               "ROS 2 needs Linux. Use WSL2 (Windows) or Docker (macOS) -- "
               "see setup/README.md, routes B and C. Running this script on "
               "the host instead of inside WSL2/Docker gives exactly this.")
        return

    pretty, version = "", ""
    try:
        with open("/etc/os-release", encoding="utf-8") as fh:
            info = dict(
                line.strip().split("=", 1)
                for line in fh if "=" in line
            )
        pretty = info.get("PRETTY_NAME", "").strip('"')
        version = info.get("VERSION_ID", "").strip('"')
    except OSError:
        pass

    in_wsl = "microsoft" in platform.release().lower()
    where = " (WSL2)" if in_wsl else ""

    if version == UBUNTU_EXPECTED:
        record("Operating system", PASS, f"{pretty}{where}")
    elif version:
        record("Operating system", WARN, f"{pretty}{where}",
               f"The course is built on Ubuntu {UBUNTU_EXPECTED}. Another "
               "version may work, but when something breaks in Week 6 this "
               "will be the first thing we suspect.")
    else:
        record("Operating system", WARN, "Linux, version unknown", "")


def check_python():
    v = sys.version_info
    got = f"{v.major}.{v.minor}.{v.micro}"
    if (v.major, v.minor) == PY_EXPECTED:
        record("Python", PASS, f"{got}  ({sys.executable})")
    else:
        want = f"{PY_EXPECTED[0]}.{PY_EXPECTED[1]}"
        record("Python", FAIL, f"{got}  ({sys.executable})",
               f"ROS 2 {ROS_DISTRO_EXPECTED.title()} builds its Python "
               f"bindings against {want}. A conda or pyenv interpreter earlier "
               "on your PATH is the usual cause. Run "
               "`conda deactivate`, open a fresh terminal, and try "
               "`/usr/bin/python3 check_ros2_setup.py`.")


# ---------------------------------------------------------------------------
# 2. Is ROS 2 installed, and is this shell aware of it?
# ---------------------------------------------------------------------------

def check_distro_env():
    distro = os.environ.get("ROS_DISTRO", "")
    if not distro:
        record("ROS_DISTRO", FAIL, "not set",
               "This shell has not sourced ROS 2. Run\n"
               f"    source /opt/ros/{ROS_DISTRO_EXPECTED}/setup.bash\n"
               "This is NOT a broken installation -- it is a fresh "
               "shell, and it will happen every time you open one. Add that "
               "line to ~/.bashrc once you have a PASS here.")
    elif distro == ROS_DISTRO_EXPECTED:
        record("ROS_DISTRO", PASS, distro)
    else:
        record("ROS_DISTRO", FAIL, distro,
               f"The course is pinned to {ROS_DISTRO_EXPECTED}. You have "
               f"{distro} sourced. Sourcing two distributions into one shell "
               "produces errors nobody can read -- open a clean terminal.")


def check_rclpy():
    """The real test. If this passes, the interpreter and ROS 2 agree."""
    try:
        import rclpy                                   # noqa: F401
        from rclpy.node import Node                    # noqa: F401
        record("rclpy (Python bindings)", PASS, "import rclpy succeeded")
    except ImportError as exc:
        record("rclpy (Python bindings)", FAIL, str(exc),
               "Either ROS 2 is not installed, or this shell is not sourced, "
               "or you are running a different Python than the one ROS 2 was "
               "built for. Check the Python row above first -- it is the "
               "cause more often than the installation is.")


def check_messages():
    """The interface packages every week of this course depends on."""
    needed = {
        "std_msgs.msg": "String",
        "geometry_msgs.msg": "Twist",
        "sensor_msgs.msg": "LaserScan",
        "nav_msgs.msg": "Odometry",
    }
    missing = []
    for module, symbol in needed.items():
        try:
            mod = __import__(module, fromlist=[symbol])
            getattr(mod, symbol)
        except Exception:
            missing.append(f"{module}.{symbol}")
    if not missing:
        record("Standard message types", PASS,
               "std_msgs, geometry_msgs, sensor_msgs, nav_msgs")
    else:
        record("Standard message types", FAIL, ", ".join(missing),
               "Install the full desktop variant:\n"
               f"    sudo apt install ros-{ROS_DISTRO_EXPECTED}-desktop\n"
               "The `-ros-base` variant does not carry these, and you "
               "will hit it again in Week 6.")


def check_cli():
    if shutil.which("ros2") is None:
        record("ros2 command", FAIL, "not on PATH",
               "Source the underlay (see the ROS_DISTRO row).")
        return
    ok, out = run(["ros2", "pkg", "list"], timeout=30)
    if not ok:
        record("ros2 command", FAIL, out.splitlines()[0] if out else "failed",
               "`ros2` exists but cannot list packages. Usually a half-sourced "
               "shell. Open a clean terminal and source once.")
        return
    pkgs = set(out.split())
    record("ros2 command", PASS, f"{len(pkgs)} packages visible")
    return pkgs


def check_turtlesim(pkgs):
    """Week 2B is built on turtlesim. Without it the session does not run."""
    if pkgs is None:
        record("turtlesim (Week 2)", FAIL, "could not check",
               "The package list could not be read, so this could not be "
               "tested. Fix the `ros2 command` row above and run this again.")
        return
    if "turtlesim" in pkgs:
        record("turtlesim (Week 2)", PASS, "installed")
    else:
        record("turtlesim (Week 2)", FAIL, "not installed",
               f"    sudo apt install ros-{ROS_DISTRO_EXPECTED}-turtlesim\n"
               "Week 2's practice session opens with this and does not "
               "work without it.")


def check_colcon():
    if shutil.which("colcon") is None:
        record("colcon (build tool)", FAIL, "not on PATH",
               "sudo apt install python3-colcon-common-extensions")
        return
    ok, out = run(["colcon", "--help"])
    record("colcon (build tool)", PASS if ok else FAIL,
           shutil.which("colcon"),
           "" if ok else "colcon is present but will not run: " + out[:120])


# ---------------------------------------------------------------------------
# 3. Things that are not needed in Week 2, but are needed later
# ---------------------------------------------------------------------------

def check_gazebo():
    """Weeks 4 onward. A WARN here is survivable until then."""
    for exe in ("gz", "ign"):
        if shutil.which(exe):
            ok, out = run([exe, "sim", "--version"])
            first = out.splitlines()[0] if out else ""
            if ok:
                record(f"Gazebo ({GAZEBO_EXPECTED})", PASS, first or exe)
            else:
                record(f"Gazebo ({GAZEBO_EXPECTED})", WARN, first or exe,
                       "Found the binary but could not read a version. "
                       "Not needed until Week 4.")
            return
    record(f"Gazebo ({GAZEBO_EXPECTED})", WARN, "not found",
           f"    sudo apt install ros-{ROS_DISTRO_EXPECTED}-ros-gz\n"
           "Not needed for Week 2 or 3. Fix it before Week 4.")


def check_gui():
    """RViz2 needs a display. On WSL2 this is WSLg; in Docker it is the VNC."""
    if not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
        record("Graphical display", WARN, "DISPLAY and WAYLAND_DISPLAY unset",
               "Nothing with a window will open -- RViz2, Gazebo, turtlesim. "
               "On WSL2 this normally means WSLg is not running: restart with "
               "`wsl --shutdown` from Windows. In Docker, connect to the VNC.")
        return
    which = "Wayland" if os.environ.get("WAYLAND_DISPLAY") else \
            os.environ.get("DISPLAY", "")
    record("Graphical display", PASS, which)


# ---------------------------------------------------------------------------
# 4. The one that costs a whole session if it is wrong
# ---------------------------------------------------------------------------

def check_domain_id():
    raw = os.environ.get("ROS_DOMAIN_ID")
    if raw is None:
        record("ROS_DOMAIN_ID", FAIL, "not set",
               "You were assigned a number in Week 1. Put it in ~/.bashrc:\n"
               "    echo 'export ROS_DOMAIN_ID=<your number>' >> ~/.bashrc\n"
               "Without it, every student in the room shares one graph: "
               "your nodes see theirs, theirs see yours, and nobody can tell "
               "which robot they are driving.")
        return
    try:
        n = int(raw)
    except ValueError:
        record("ROS_DOMAIN_ID", FAIL, repr(raw), "It must be a number, 0-101.")
        return
    if 0 <= n <= 101:
        extra = "  (0 is the default -- everyone who set nothing is here too)" \
                if n == 0 else ""
        status = WARN if n == 0 else PASS
        record("ROS_DOMAIN_ID", status, f"{n}{extra}",
               "Use the number you were assigned, not 0." if n == 0 else "")
    else:
        record("ROS_DOMAIN_ID", FAIL, str(n),
               "Must be 0-101. Higher values are not portable across systems.")


# ---------------------------------------------------------------------------

def main():
    print()
    print("EE 414 -- Introduction to Robotics : setup check")
    print(f"Target stack: ROS 2 {ROS_DISTRO_EXPECTED.title()} / "
          f"Ubuntu {UBUNTU_EXPECTED} / Python "
          f"{PY_EXPECTED[0]}.{PY_EXPECTED[1]} / Gazebo {GAZEBO_EXPECTED}")
    print()

    check_os()
    check_python()
    check_distro_env()
    check_rclpy()
    check_messages()
    pkgs = check_cli()
    check_turtlesim(pkgs)
    check_colcon()
    check_gazebo()
    check_gui()
    check_domain_id()

    width = max(len(name) for name, _, _, _ in results)
    print("-" * (width + 58))
    for name, status, detail, _ in results:
        if len(detail) > 52:
            detail = detail[:49] + "..."
        print(f"  {name.ljust(width)}   {status:4}   {detail}")
    print("-" * (width + 58))
    print()

    problems = [r for r in results if r[1] in (FAIL, WARN) and r[3]]
    if problems:
        print("What to do about it")
        print()
        for name, status, _, fix in problems:
            print(f"  [{status}] {name}")
            for line in fix.splitlines():
                print(f"      {line}")
            print()

    failed = sum(1 for _, s, _, _ in results if s == FAIL)
    warned = sum(1 for _, s, _, _ in results if s == WARN)

    if failed:
        print(f"{failed} check(s) FAILED. Week 2's practice session needs "
              "these fixed.")
        print("Work top to bottom -- a failure high in the list usually "
              "causes the ones below it.")
    elif warned:
        print(f"No failures, {warned} warning(s). You are ready for Week 2.")
    else:
        print("Everything passed. You are ready for Week 2.")

    print()
    print("Bring this output to the session -- a screenshot is fine.")
    print()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
