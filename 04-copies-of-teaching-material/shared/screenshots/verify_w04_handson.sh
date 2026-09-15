#!/usr/bin/env bash
# Walk the Week 4 hands-on lab from an empty directory to a moving robot.
#
# EE414_W04_hands_on_lab.html promises that a student who types every line in
# order ends up with a turtle driving a circle. This script is that student: it
# clones the repository into a scratch workspace, builds it, runs the two 2023
# demonstrations, creates my_turtle_circle with `ros2 pkg create`, installs the
# two files from week04/ros2_lab/handson/, builds again and measures the circle
# the node actually traces. The table lands in week04/ros2_lab/handson_check.txt.
#
# Two rows are expected to FAIL-as-documented rather than pass, and the script
# says so: `mover` ends in an RCLError on Jazzy, and the cleaner's rotate never
# terminates past 180 degrees. Both are in the lab sheet as warnings, so a run
# in which they suddenly succeed is a change the sheet has to be told about.
#
#   bash verify_w04_handson.sh              # ~10 minutes, needs a display
#   KEEP=1 bash verify_w04_handson.sh       # leave the scratch workspace behind
set -o pipefail       # NOT set -u: ROS 2 setup.bash reads unset variables

# Job control ON. Without it bash hands every background job SIGINT = SIG_IGN,
# the disposition is inherited down to python, and the Ctrl-C row below would
# be signalling a process tree that cannot be signalled. See the same comment
# in verify_w04_commands.sh -- it cost a morning there.
set -m

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/rosenv.sh"
source "$HERE/procgroup.sh"
export PYTHONUNBUFFERED=1

LAB="$(cd "$HERE/../../week04/ros2_lab" && pwd)"
SRC="$LAB/handson"
REPORT="$LAB/handson_check.txt"
WS="${WS_OVERRIDE:-$HOME/.cache/ee414_handson_ws}"
REPO=https://github.com/aniskoubaa/ros2_course_packages.git
LOGS="$(mktemp -d)"

pass=0; fail=0; rows=()
note() { printf '%s\n' "$*" >> "$REPORT"; }
ok()   { rows+=("  PASS   $1"); pass=$((pass + 1)); }
bad()  { rows+=("  FAIL   $1"); rows+=("         $2"); fail=$((fail + 1)); }

# A command that must finish, exit 0, and print no traceback.
check() {
  local secs="$1" label="$2"; shift 2
  local log="$LOGS/$(echo "$label" | tr -c 'A-Za-z0-9' '_').log"
  timeout "$secs" bash -c "source '$HERE/rosenv.sh'; source '$WS/install/setup.bash' 2>/dev/null; $*" > "$log" 2>&1
  local rc=$? traces
  traces=$(grep -cE 'Traceback|RCLError|Process exited with failure' "$log")
  if [ "$rc" -eq 0 ] && [ "$traces" -eq 0 ]; then ok "$label"
  else bad "$label   (exit $rc, $traces traceback line(s))" "$(tail -2 "$log" | tr '\n' ' ')"; fi
}

# A command the lab sheet documents as broken. It must still be broken.
check_known_bad() {
  local secs="$1" label="$2" want="$3"; shift 3
  local log="$LOGS/$(echo "$label" | tr -c 'A-Za-z0-9' '_').log"
  timeout "$secs" bash -c "source '$HERE/rosenv.sh'; source '$WS/install/setup.bash' 2>/dev/null; $*" > "$log" 2>&1
  local rc=$?
  if grep -qE "$want" "$log" || { [ "$want" = "TIMEOUT" ] && [ "$rc" -eq 124 ]; }; then
    ok "$label   [fails as documented]"
  else
    bad "$label   (expected the documented failure, got exit $rc)" "$(tail -2 "$log" | tr '\n' ' ')"
  fi
}

bgpg=()
bg() {   # bg <command> -- a simulator, left running until stop_bg
  local f; f="$LOGS/bg$(( ${#bgpg[@]} + 1 )).pgid"; bgpg+=("$f")
  spawn_pg "$f" /dev/null "source '$HERE/rosenv.sh'; exec $1"
}
stop_bg() { local f; for f in "${bgpg[@]:-}"; do kill_pg "$f"; done; bgpg=(); }
cleanup() { stop_bg; rm -rf "$LOGS"; [ -z "${KEEP:-}" ] && rm -rf "$WS"; }
trap cleanup EXIT

spawn() {   # spawn <pgid-file> <command>
  spawn_pg "$1" "$LOGS/$(basename "$1").log" \
    "source '$HERE/rosenv.sh'; source '$WS/install/setup.bash' 2>/dev/null; exec $2"
}

: > "$REPORT"
note "# EE 414 Week 4 --- hands-on lab check"
note "#"
note "# Every step of EE414_W04_hands_on_lab.html, from an empty directory."
note "#   ROS 2 ${ROS_DISTRO}  |  $(lsb_release -ds 2>/dev/null)"
note "#   captured $(date -u '+%Y-%m-%d %H:%M UTC')"
note "#"
note "# Regenerate:  bash ../../shared/screenshots/verify_w04_handson.sh"
note ""

# --- part 1: get the code --------------------------------------------------
rm -rf "$WS"; mkdir -p "$WS/src"
check 300 "git clone ros2_course_packages" "git clone --depth 1 '$REPO' '$WS/src/ros2_course_packages'"
check 300 "colcon build (two motion packages)" \
      "cd '$WS' && colcon build --packages-select ros2_motion_python ros2_motion_cpp"

n=$(bash -c "source '$HERE/rosenv.sh'; source '$WS/install/setup.bash'; ros2 pkg executables ros2_motion_python" 2>/dev/null | wc -l)
[ "$n" = "3" ] && ok "ros2_motion_python ships 3 executables" \
                || bad "ros2_motion_python executables" "expected 3, got $n"

n=$(bash -c "source '$HERE/rosenv.sh'; source '$WS/install/setup.bash'; ros2 pkg executables ros2_motion_cpp" 2>/dev/null | wc -l)
[ "$n" = "0" ] && ok "ros2_motion_cpp ships 0 executables (empty skeleton)" \
                || bad "ros2_motion_cpp executables" "expected 0 before the student adds circle.cpp, got $n"

# --- part 2: run the 2023 demonstrations -----------------------------------
bg "ros2 run turtlesim turtlesim_node"
sleep 8
check 30 "turtlesim is up" "ros2 topic list | grep -q /turtle1/cmd_vel"

check 90  "cleaner: move 2.0 forward"  "printf '1\n2\n1\nq\n' | ros2 run ros2_motion_python cleaner"
check 90  "cleaner: rotate 90 CCW"     "printf '7\n2\n90\n0\nq\n' | ros2 run ros2_motion_python cleaner"
check 90  "cleaner: go to goal 1,1"    "printf '7\n4\n1\n1\n0\nq\n' | ros2 run ros2_motion_python cleaner"
check 120 "cleaner: spiral"            "printf '7\n5\n0.2\n2.0\nq\n' | ros2 run ros2_motion_python cleaner"
check_known_bad 150 "cleaner: rotate 200 CCW" "TIMEOUT" \
      "printf '7\n2\n200\n0\nq\n' | ros2 run ros2_motion_python cleaner"
check_known_bad 110 "mover: 15 units then stop" "publisher's context is invalid" \
      "ros2 run ros2_motion_python mover"

# --- part 3: the package the student creates -------------------------------
check 60 "ros2 pkg create my_turtle_circle" \
      "cd '$WS/src' && ros2 pkg create my_turtle_circle --build-type ament_python --license Apache-2.0 --dependencies rclpy geometry_msgs"

cp "$SRC/my_turtle_circle/circle.py" "$WS/src/my_turtle_circle/my_turtle_circle/circle.py" 2>/dev/null \
  && ok "circle.py installed ($(wc -l < "$SRC/my_turtle_circle/circle.py") lines)" \
  || bad "circle.py installed" "missing $SRC/my_turtle_circle/circle.py"

sed -i "s|        'console_scripts': \[|        'console_scripts': [\n            'circle = my_turtle_circle.circle:main',|" \
    "$WS/src/my_turtle_circle/setup.py"
grep -q "my_turtle_circle.circle:main" "$WS/src/my_turtle_circle/setup.py" \
  && ok "setup.py entry point added" || bad "setup.py entry point" "sed did not match"

check 300 "colcon build my_turtle_circle" "cd '$WS' && colcon build --packages-select my_turtle_circle"

# --- part 4: does it actually drive a circle? ------------------------------
# Radius is v/w = 2.0/1.0 = 2.0 turtlesim units. Measured, not asserted: sample
# /turtle1/pose for a little over one revolution (2*pi/w = 6.28 s) and take half
# the span in each axis.
measure_circle() {   # measure_circle <label> <ros2 run command>
  local label="$1" cmd="$2"
  bash -c "source '$HERE/rosenv.sh'; ros2 service call /reset std_srvs/srv/Empty '{}'" >/dev/null 2>&1
  local pg="$LOGS/$(echo "$label" | tr -c 'A-Za-z0-9' '_').pgid"
  spawn "$pg" "$cmd"
  sleep 1
  timeout 8 bash -c "source '$HERE/rosenv.sh'; ros2 topic echo /turtle1/pose --csv" > "$LOGS/poses.csv" 2>/dev/null
  sigint_pg "$pg" 6
  sleep 1
  local r
  r=$(python3 - "$LOGS/poses.csv" <<'PY'
import sys
xs = []; ys = []
for line in open(sys.argv[1]):
    p = line.strip().split(',')
    if len(p) >= 5:
        try: xs.append(float(p[0])); ys.append(float(p[1]))
        except ValueError: pass
if len(xs) < 50: print("nan nan"); raise SystemExit
print("%.3f %.3f" % ((max(xs) - min(xs)) / 2, (max(ys) - min(ys)) / 2))
PY
)
  local rx ry; read -r rx ry <<< "$r"
  if python3 -c "import sys; sys.exit(0 if abs($rx-2.0)<0.05 and abs($ry-2.0)<0.05 else 1)" 2>/dev/null; then
    ok "$label traces r = $rx by $ry  (v/w = 2.0)"
  else
    bad "$label circle radius" "measured $rx by $ry, expected 2.000 by 2.000"
  fi
  # ... and the turtle must be stopped afterwards.
  local v
  v=$(bash -c "source '$HERE/rosenv.sh'; ros2 topic echo /turtle1/pose --once" 2>/dev/null \
      | grep -E 'linear_velocity|angular_velocity' | tr -d ' \n')
  [ "$v" = "linear_velocity:0.0angular_velocity:0.0" ] \
    && ok "$label   [Ctrl-C] leaves the turtle stopped" \
    || bad "$label   [Ctrl-C] stop" "pose still reports $v"
  grep -qE 'Traceback|RCLError' "$LOGS/$(basename "$pg").log" \
    && bad "$label   [Ctrl-C] clean exit" "$(tail -2 "$LOGS/$(basename "$pg").log" | tr '\n' ' ')" \
    || ok "$label   [Ctrl-C] no traceback"
}

measure_circle "circle (python)" "ros2 run my_turtle_circle circle"

# --- part 5: the same node in C++ ------------------------------------------
CPP="$WS/src/ros2_course_packages/src/ros2_motion_cpp"
mkdir -p "$CPP/src"
cp "$SRC/ros2_motion_cpp/circle.cpp" "$CPP/src/circle.cpp"
python3 - "$CPP/CMakeLists.txt" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
add = ("add_executable(circle_cpp src/circle.cpp)\n"
       "ament_target_dependencies(circle_cpp rclcpp geometry_msgs)\n\n"
       "install(TARGETS\n  circle_cpp\n  DESTINATION lib/${PROJECT_NAME})\n\n")
if "circle_cpp" not in s:
    s = s.replace("if(BUILD_TESTING)", add + "if(BUILD_TESTING)")
    open(p, 'w').write(s)
PY
grep -q circle_cpp "$CPP/CMakeLists.txt" && ok "CMakeLists.txt gains circle_cpp" \
                                         || bad "CMakeLists.txt" "add_executable not inserted"
check 300 "colcon build ros2_motion_cpp (with circle.cpp)" \
      "cd '$WS' && colcon build --packages-select ros2_motion_cpp"
n=$(bash -c "source '$HERE/rosenv.sh'; source '$WS/install/setup.bash'; ros2 pkg executables ros2_motion_cpp" 2>/dev/null | wc -l)
[ "$n" = "1" ] && ok "ros2_motion_cpp now ships circle_cpp" || bad "circle_cpp executable" "got $n"

measure_circle "circle_cpp" "ros2 run ros2_motion_cpp circle_cpp"

stop_bg

printf '%s\n' "${rows[@]}" >> "$REPORT"
note ""
note "$pass passed, $fail failed."
cat "$REPORT"
exit $(( fail > 0 ))
