#!/usr/bin/env bash
# Run every command in the Week 4A cue sheet and report which ones work.
#
# The sheet's standing promise is that each line was actually executed on this
# machine. This is the script that keeps the promise honest: it drives every
# simulator the sheet needs, runs all forty commands in lecture order, and
# writes a pass/fail table to week04/ros2_lab/command_check.txt.
#
# Long-running commands (a simulator, a watcher) are interrupted the way the
# lecturer interrupts them -- SIGINT to the whole process group, which is what
# Ctrl-C does in a terminal -- and are expected to exit 0 with no traceback.
#
#   bash verify_w04_commands.sh              # everything except Gazebo
#   WITH_GAZEBO=1 bash verify_w04_commands.sh
set -o pipefail       # NOT set -u: ROS 2 setup.bash reads unset variables

# Job control ON, and this one is not optional. With it off -- the default in a
# script -- bash sets SIGINT to SIG_IGN for every background job, and that
# disposition is inherited all the way down to python. The interrupt checks
# below would then be signalling a process tree that cannot be signalled, and
# they would report whatever the fallback kill -9 produced. A node that relies
# on Python's default Ctrl-C handling would be marked broken; one that installs
# its own handler (graceful.py does) would pass for the wrong reason. `set -m`
# gives background jobs the same SIGINT disposition a terminal gives them.
set -m

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/rosenv.sh"
source "$HERE/procgroup.sh"
source "$HERE/assert_clean_graph.sh"
assert_clean_graph || exit 1
export PYTHONUNBUFFERED=1

WS="$(cd "$HERE/../../../code" && pwd)"
LAB="$(cd "$HERE/../../week04/ros2_lab" && pwd)"
REPORT="$LAB/command_check.txt"
LOGS="$(mktemp -d)"

pass=0; fail=0; rows=()

note() { printf '%s\n' "$*" >> "$REPORT"; }

# ---------------------------------------------------------------------------
# One command, run to completion. $1 is a timeout in seconds, $2 the label.
# ---------------------------------------------------------------------------
check() {
  local secs="$1" label="$2"; shift 2
  local log="$LOGS/$(echo "$label" | tr -c 'A-Za-z0-9' '_').log"
  timeout "$secs" bash -c "source '$HERE/rosenv.sh'; $*" > "$log" 2>&1
  local rc=$?
  verdict "$rc" "$label" "$log" 0
}

# ---------------------------------------------------------------------------
# A command with no natural end: start it in its own process group, SIGINT the
# group after $1 seconds, the way Ctrl-C does in a terminal.
#
# Our own nodes must exit 0 -- that is the whole point of graceful.py. The ROS 2
# CLI tools (`ros2 topic pub`, `tf2_echo`) exit non-zero on SIGINT and always
# have; they are designed to be interrupted and print nothing when they are.
# So use check_interrupt for ours, check_interrupt_cli for theirs: both refuse a
# traceback, only the first demands exit 0.
# ---------------------------------------------------------------------------
# NOT `INTERRUPT_ANY_EXIT=1 check_interrupt ...`: a variable assignment prefixed
# to a *function* call leaks into the shell afterwards in bash, which would make
# every later check lenient.
check_interrupt_cli() {
  INTERRUPT_ANY_EXIT=1
  check_interrupt "$@"
  unset INTERRUPT_ANY_EXIT
}

# The group id comes from the child, never from $!. See procgroup.sh: with
# `set -m` above, setsid forks and $! is a parent that has already exited, so
# the old `kill -INT -$!` signalled nothing and every row here passed without
# testing anything. The leaked `ros2 topic pub` processes it left behind were
# what gave it away.
check_interrupt() {
  local secs="$1" label="$2"; shift 2
  local slug; slug=$(echo "$label" | tr -c 'A-Za-z0-9' '_')
  local log="$LOGS/$slug.log" pgf="$LOGS/$slug.pgid"
  spawn_pg "$pgf" "$log" "source '$HERE/rosenv.sh'; $*" || {
    rows+=("  FAIL   $label   (could not start)"); fail=$((fail + 1)); return; }
  sleep "$secs"
  if ! kill -0 -"$(cat "$pgf")" 2>/dev/null; then
    rows+=("  FAIL   $label   [Ctrl-C]   (exited before the interrupt; nothing was tested)")
    fail=$((fail + 1)); return
  fi
  local rc=0
  sigint_pg "$pgf" 10 || rc=1
  [ -n "${INTERRUPT_ANY_EXIT:-}" ] && rc=0
  verdict "$rc" "$label" "$log" 1
}

verdict() {
  local rc="$1" label="$2" log="$3" interrupted="$4"
  local suffix=""
  [ "$interrupted" = "1" ] && suffix="   [Ctrl-C]"
  local traces
  traces=$(grep -cE 'Traceback|RCLError|Process exited with failure' "$log")
  if [ "$rc" -eq 0 ] && [ "$traces" -eq 0 ]; then
    rows+=("  PASS   ${label}${suffix}"); pass=$((pass + 1))
  else
    rows+=("  FAIL   $label   (exit $rc, $traces traceback line(s))")
    rows+=("         $(tail -3 "$log" | tr '\n' ' ')")
    fail=$((fail + 1))
  fi
}

bgpg=()
bg() {   # bg <command> -- a simulator, left running until stop_bg
  local pgf="$LOGS/bg$(( ${#bgpg[@]} + 1 )).pgid"; bgpg+=("$pgf")
  spawn_pg "$pgf" /dev/null "source '$HERE/rosenv.sh'; exec $1"
}
stop_bg() { local f; for f in "${bgpg[@]:-}"; do kill_pg "$f"; done; bgpg=(); }
trap stop_bg EXIT

: > "$REPORT"
note "# EE 414 Week 4A --- cue sheet command check"
note "#"
note "# Every command in EE414_W04_demo_cue_sheet.html, run in lecture order."
note "#   ROS 2 ${ROS_DISTRO}  |  $(lsb_release -ds 2>/dev/null)"
note "#   captured $(date -u '+%Y-%m-%d %H:%M UTC')"
note "#"
note "# Regenerate:  bash ../../shared/screenshots/verify_w04_commands.sh"
note "#   add WITH_GAZEBO=1 to include the TurtleBot 3 rows."
note ""

# --- setup -----------------------------------------------------------------
check 300 "colcon build ee414_course" "cd '$WS' && colcon build --packages-select ee414_course"

# --- no simulator ----------------------------------------------------------
check 60 "quaternion_demo --part 1" "ros2 run ee414_course quaternion_demo --part 1"
check 60 "quaternion_demo --part 2" "ros2 run ee414_course quaternion_demo --part 2"
check 60 "quaternion_demo --part 3" "ros2 run ee414_course quaternion_demo --part 3"
check 60 "quaternion_demo --part 4" "ros2 run ee414_course quaternion_demo --part 4"
check 60 "the one-liner wrap"       "python3 -c \"import math; a=math.radians(176); b=math.radians(-176); print('naive ', math.degrees(b-a)); print('wrapped', math.degrees(math.atan2(math.sin(b-a), math.cos(b-a))))\""
check 60 "interface show Twist"     "ros2 interface show geometry_msgs/msg/Twist"
check 60 "wheels_to_body --table"   "ros2 run ee414_course wheels_to_body --table"
check 60 "wheels_to_body 0 10"      "ros2 run ee414_course wheels_to_body 0 10"
check 60 "body_to_wheels 0.2 1.0"   "ros2 run ee414_course body_to_wheels 0.2 1.0"
check 60 "body_to_wheels 0.5 3.0"   "ros2 run ee414_course body_to_wheels 0.5 3.0"
check 60 "grep the URDF"            "grep -E '<joint name|<origin xyz|<cylinder radius' \$(ros2 pkg prefix --share ee414_course)/urdf/burger_min.urdf"
check 60 "check_urdf"               "check_urdf \$(ros2 pkg prefix --share ee414_course)/urdf/burger_min.urdf"
check 60 "grep the SDF plugin"      "grep -A7 'systems::DiffDrive' \$(ros2 pkg prefix --share ee414_course)/worlds/diff_drive_demo.sdf"
check 120 "dead_reckoning --compare" "ros2 run ee414_course dead_reckoning --compare"

# --- turtlesim -------------------------------------------------------------
bg "ros2 run turtlesim turtlesim_node"
sleep 8
check 30 "pose --once"              "ros2 topic echo /turtle1/pose --once"
check_interrupt 5 "pose_watch"      "ros2 run ee414_course pose_watch"
check_interrupt_cli 5 "cmd_vel pub (drive)" "ros2 topic pub -r 10 /turtle1/cmd_vel geometry_msgs/msg/Twist '{linear: {x: 1.0}, angular: {z: 0.6}}'"
check 30 "service call /reset"      "ros2 service call /reset std_srvs/srv/Empty '{}'"
check_interrupt_cli 4 "cmd_vel pub (sideways)" "ros2 topic pub -r 10 /turtle1/cmd_vel geometry_msgs/msg/Twist '{linear: {y: 2.0}}'"
check 30 "angle_wrap"               "ros2 run ee414_course angle_wrap"
check 120 "nonholonomic"            "ros2 run ee414_course nonholonomic"
check 30 "reset"                    "ros2 service call /reset std_srvs/srv/Empty '{}'"
check 120 "drive --shape square"    "ros2 run ee414_course drive --shape square --distance 2.0"
check 30 "reset"                    "ros2 service call /reset std_srvs/srv/Empty '{}'"
check 120 "drive --shape spiral"    "ros2 run ee414_course drive --shape spiral --speed 2.0 --turn-rate 1.2"
check 30 "reset"                    "ros2 service call /reset std_srvs/srv/Empty '{}'"
check 120 "move_rotate --shape square" "ros2 run ee414_course move_rotate --shape square --distance 2.0"
check 30 "reset"                    "ros2 service call /reset std_srvs/srv/Empty '{}'"
check 120 "go_to_goal 9,9"          "ros2 run ee414_course go_to_goal --x 9.0 --y 9.0"
check 180 "go_to_goal 1.5,2"        "ros2 run ee414_course go_to_goal --x 1.5 --y 2.0"
stop_bg

# --- the model in RViz -----------------------------------------------------
bg "ros2 launch ee414_course view_model.launch.py"
sleep 18
check_interrupt_cli 8 "tf2_echo wheel to wheel" "ros2 run tf2_ros tf2_echo wheel_left_link wheel_right_link"
stop_bg
sleep 3

# --- Gazebo ----------------------------------------------------------------
if [ -n "${WITH_GAZEBO:-}" ]; then
  bg "gz sim -r \$(ros2 pkg prefix --share ee414_course)/worlds/diff_drive_demo.sdf"
  sleep 35
  check 25 "the demo world publishes /odom" "gz topic -e -t /odom -n 1"
  stop_bg
  sleep 5

  bg "ros2 launch turtlebot3_gazebo empty_world.launch.py"
  sleep 50
  check 30  "odom --once"           "ros2 topic echo /odom --once"
  check 20  "topic type /cmd_vel"   "ros2 topic type /cmd_vel"
  check_interrupt_cli 5 "cmd_vel pub, WRONG type" "ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.1}}'"
  check 180 "drive tb3 square"      "ros2 run ee414_course drive --robot tb3 --shape square --distance 0.5 --speed 0.15 --turn-rate 0.5"
  check 120 "drive tb3 arc 180"     "ros2 run ee414_course drive --robot tb3 --shape arc --angle 180 --speed 0.15 --turn-rate 0.4"
  check_interrupt 8 "dead_reckoning --robot tb3" "ros2 run ee414_course dead_reckoning --robot tb3"
  stop_bg
else
  rows+=("  SKIP   TurtleBot 3 rows (re-run with WITH_GAZEBO=1)")
fi

printf '%s\n' "${rows[@]}" >> "$REPORT"
note ""
note "$pass passed, $fail failed."
rm -rf "$LOGS"
cat "$REPORT"
exit $(( fail > 0 ))
