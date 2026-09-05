#!/usr/bin/env bash
# Generate week03/ros2_lab/expected_output.txt from an actual run.
#
# code/README.md standing rule: "The expected-output transcript in the matching
# ros2_lab/ is generated from an actual run, not written by hand." This is that
# generator. Marking a student's lab against a transcript somebody typed from
# memory is how a class ends up being told its correct output is wrong.
#
#   bash make_expected_output.sh
set -o pipefail       # NOT set -u: ROS 2 setup.bash reads unset variables
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/rosenv.sh"

WS="$(cd "$HERE/../../../code" && pwd)"
OUT="$(cd "$HERE/../../week03/ros2_lab" && pwd)/expected_output.txt"

started=()
bg() { setsid bash -c "source '$HERE/rosenv.sh'; exec $1" >/dev/null 2>&1 & started+=("$!"); }
cleanup() { for p in "${started[@]:-}"; do kill -- "-$p" 2>/dev/null; done; }
trap cleanup EXIT

{
  echo "# EE 414 Week 3 --- expected output"
  echo "#"
  echo "# Generated from an actual run, not written by hand."
  echo "#   ROS 2 ${ROS_DISTRO}  |  $(lsb_release -ds 2>/dev/null)"
  echo "#   captured $(date -u '+%Y-%m-%d %H:%M UTC')"
  echo "#"
  echo "# Regenerate:  bash ../../shared/screenshots/make_expected_output.sh"
  echo

  echo "=== colcon build --symlink-install ==="
  ( cd "$WS" && rm -rf build install log && colcon build --symlink-install 2>&1 \
      | grep -vi warning )
  source "$WS/install/setup.bash"
  echo

  echo "=== Checkpoint 1 --- ros2 interface show ==="
  echo "\$ ros2 interface show ee414_w03_interfaces/msg/WheelState"
  ros2 interface show ee414_w03_interfaces/msg/WheelState
  echo
  echo "\$ ros2 interface show ee414_w03_interfaces/srv/ResetOdom"
  ros2 interface show ee414_w03_interfaces/srv/ResetOdom
  echo

  bg "ros2 run ee414_w03_nodes wheel_publisher"
  bg "ros2 run ee414_w03_nodes odom_node"
  sleep 5

  echo "=== Checkpoint 2 --- your own type on the wire ==="
  echo "\$ ros2 topic echo /wheel_state --once"
  timeout 15 ros2 topic echo /wheel_state --once
  echo "# stamp will differ; every other field must match."
  echo

  echo "=== Checkpoint 3 --- the service, from the terminal ==="
  echo "\$ ros2 service call /reset_odom ee414_w03_interfaces/srv/ResetOdom \"{zero_heading: true}\""
  timeout 20 ros2 service call /reset_odom ee414_w03_interfaces/srv/ResetOdom "{zero_heading: true}"
  echo

  echo "=== Checkpoint 4a --- mode:=spin, the loud failure ==="
  echo "\$ ros2 run ee414_w03_nodes reset_client --ros-args -p mode:=spin"
  timeout 12 ros2 run ee414_w03_nodes reset_client --ros-args -p mode:=spin 2>&1 | tail -6
  echo

  echo "=== Checkpoint 4b --- mode:=hang, the silent one ==="
  echo "\$ ros2 run ee414_w03_nodes reset_client --ros-args -p mode:=hang"
  hl=$(mktemp); bg "ros2 run ee414_w03_nodes reset_client --ros-args -p mode:=hang > $hl 2>&1"
  sleep 10; cat "$hl"; rm -f "$hl"
  echo "# and then nothing, for as long as you leave it. That is the deadlock."
  echo

  echo "=== The fix --- mode:=fix ==="
  echo "\$ ros2 run ee414_w03_nodes reset_client --ros-args -p mode:=fix"
  fl=$(mktemp); bg "ros2 run ee414_w03_nodes reset_client --ros-args -p mode:=fix > $fl 2>&1"
  sleep 8; tail -4 "$fl"; rm -f "$fl"
  echo "# one reply per published message, forever."
  echo

  echo "=== Checkpoint 5 --- a parameter, changed while it runs ==="
  bg "ros2 run ee414_w03_nodes driver"
  sleep 5
  echo "\$ ros2 param get /driver max_speed"
  timeout 10 ros2 param get /driver max_speed
  echo "\$ ros2 param set /driver max_speed 0.05"
  timeout 10 ros2 param set /driver max_speed 0.05
  echo "\$ ros2 param get /driver max_speed"
  timeout 10 ros2 param get /driver max_speed
  echo

  echo "=== Checkpoint 6 --- an action, with feedback ==="
  bg "ros2 run action_tutorials_py fibonacci_action_server"
  sleep 5
  echo "\$ ros2 action send_goal /fibonacci action_tutorials_interfaces/action/Fibonacci \"{order: 3}\" --feedback"
  timeout 25 ros2 action send_goal /fibonacci \
      action_tutorials_interfaces/action/Fibonacci "{order: 3}" --feedback 2>&1
  echo "# the goal ID differs every run; the sequence does not."
} > "$OUT"

echo "wrote $OUT  ($(wc -l < "$OUT") lines)"
