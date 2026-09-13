#!/usr/bin/env bash
# Run all seven beginner scripts in ee414_course/beginner_student_freindly.
#
# Same contract as verify_w04_commands.sh, and for the same reason: a script
# that goes on the projector must have been run on this machine first. The two
# arithmetic scripts must finish and exit 0; the five that need turtlesim are
# interrupted with a real Ctrl-C part way through and must also exit 0, with no
# traceback and the turtle stopped.
#
#   bash verify_beginner_scripts.sh
set -o pipefail       # NOT set -u: ROS 2 setup.bash reads unset variables

# See the long note in verify_w04_commands.sh. Without job control, bash gives
# every background job SIGINT = SIG_IGN, and the interrupt checks below would
# be signalling a process tree that cannot be signalled.
set -m

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/rosenv.sh"
source "$HERE/assert_clean_graph.sh"
assert_clean_graph || exit 1
export PYTHONUNBUFFERED=1

REPORT="$(cd "$HERE/../../week04/ros2_lab" && pwd)/beginner_check.txt"
LOGS="$(mktemp -d)"
pass=0; fail=0; rows=()

verdict() {   # verdict <rc> <label> <log> <interrupted>
  local rc="$1" label="$2" log="$3" interrupted="$4" suffix=""
  [ "$interrupted" = "1" ] && suffix="   [Ctrl-C]"
  local traces
  traces=$(grep -cE 'Traceback|RCLError|ExternalShutdown' "$log")
  if [ "$rc" = "0" ] && [ "$traces" = "0" ]; then
    rows+=("  PASS   ${label}${suffix}"); pass=$((pass + 1))
  else
    rows+=("  FAIL   ${label}${suffix}   (exit $rc, $traces tracebacks)")
    fail=$((fail + 1)); echo "--- $label ---"; tail -15 "$log"
  fi
}

check() {   # check <timeout> <label> <command...>
  local secs="$1" label="$2"; shift 2
  local log="$LOGS/$(echo "$label" | tr -c 'A-Za-z0-9' '_').log"
  timeout "$secs" bash -c "source '$HERE/rosenv.sh'; $*" > "$log" 2>&1
  verdict "$?" "$label" "$log" 0
}

check_interrupt() {   # check_interrupt <seconds before Ctrl-C> <label> <command...>
  local secs="$1" label="$2"; shift 2
  local log="$LOGS/$(echo "$label" | tr -c 'A-Za-z0-9' '_').log"
  setsid bash -c "source '$HERE/rosenv.sh'; exec $*" > "$log" 2>&1 &
  local pgid=$! i
  sleep "$secs"
  kill -INT -"$pgid" 2>/dev/null
  for i in $(seq 1 40); do kill -0 -"$pgid" 2>/dev/null || break; sleep 0.25; done
  kill -0 -"$pgid" 2>/dev/null && kill -9 -"$pgid" 2>/dev/null
  wait "$pgid" 2>/dev/null
  verdict "$?" "$label" "$log" 1
}

started=()
bg() { setsid bash -c "source '$HERE/rosenv.sh'; exec $1" >/dev/null 2>&1 & started+=("$!"); }
cleanup() { for p in "${started[@]:-}"; do kill -9 -- "-$p" 2>/dev/null; done; }
trap cleanup EXIT

echo "no simulator needed"
check 20 "simple_kinematics"    "ros2 run ee414_course simple_kinematics"
check 20 "simple_angle_wrap"    "ros2 run ee414_course simple_angle_wrap"

echo "starting turtlesim"
bg "ros2 run turtlesim turtlesim_node"
sleep 6

check_interrupt 4  "simple_pose_reader"   "ros2 run ee414_course simple_pose_reader"
check_interrupt 2  "simple_nonholonomic"  "ros2 run ee414_course simple_nonholonomic"
check_interrupt 2  "simple_move"          "ros2 run ee414_course simple_move"
check_interrupt 5  "simple_square"        "ros2 run ee414_course simple_square"
check_interrupt 3  "simple_go_to_goal"    "ros2 run ee414_course simple_go_to_goal"

# Ctrl-C during a drive must leave the robot stopped, not coasting.
sleep 2
vels=$(bash -c "source '$HERE/rosenv.sh'; timeout 5 ros2 topic echo /turtle1/pose --once" 2>/dev/null \
       | grep -E 'linear_velocity|angular_velocity')
moving=$(printf '%s\n' "$vels" | grep -vc ': 0\.0$')
if [ -n "$vels" ] && [ "$moving" = "0" ]; then
  rows+=("  PASS   the turtle is stopped after every Ctrl-C"); pass=$((pass + 1))
else
  rows+=("  FAIL   the turtle is STILL MOVING after Ctrl-C")
  fail=$((fail + 1)); echo "--- turtle velocities ---"; printf '%s\n' "$vels"
fi

{
  echo "# EE 414 Week 4 --- beginner script check"
  echo "#"
  echo "# ee414_course/beginner_student_freindly, every script run on this machine."
  echo "#   ROS 2 ${ROS_DISTRO}  |  $(lsb_release -ds 2>/dev/null)"
  echo "#   captured $(date -u '+%Y-%m-%d %H:%M UTC')"
  echo "#"
  echo "# Regenerate:  bash ../../shared/screenshots/verify_beginner_scripts.sh"
  echo "#"
  echo "# [Ctrl-C] means the script was interrupted part way through with a real"
  echo "# SIGINT to its process group. Exit 0 and no traceback is the requirement."
  echo
  printf '%s\n' "${rows[@]}"
  echo
  echo "$pass passed, $fail failed."
} > "$REPORT"

cat "$REPORT"
