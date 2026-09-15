#!/usr/bin/env bash
# Generate week04/ros2_lab/expected_output.txt from an actual run.
#
# Same rule as Week 3: the transcript is produced by running the commands, not
# by typing what they ought to print. The arithmetic sections are exact and
# will reproduce byte for byte; the two closing errors are simulator-dependent
# and will land near, not on, the numbers recorded here. Both facts are stated
# in the file itself so nobody marks a correct lab wrong.
#
#   bash make_expected_output_w04.sh          # arithmetic + turtlesim
#   WITH_GAZEBO=1 bash make_expected_output_w04.sh   # also TurtleBot 3
set -o pipefail       # NOT set -u: ROS 2 setup.bash reads unset variables
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/rosenv.sh"
source "$HERE/assert_clean_graph.sh"
assert_clean_graph || exit 1

WS="$(cd "$HERE/../../../code" && pwd)"
OUT="$(cd "$HERE/../../week04/ros2_lab" && pwd)/expected_output.txt"

started=()
bg() { setsid bash -c "source '$HERE/rosenv.sh'; exec $1" >/dev/null 2>&1 & started+=("$!"); }
cleanup() { for p in "${started[@]:-}"; do kill -- "-$p" 2>/dev/null; done; }
trap cleanup EXIT

run() {   # run() "command" -- echoes the command, then its output
  echo "\$ $1"
  bash -c "source '$HERE/rosenv.sh'; source '$WS/install/setup.bash'; $1" 2>&1
  echo
}

{
  echo "# EE 414 Week 4 --- expected output"
  echo "#"
  echo "# Generated from an actual run, not written by hand."
  echo "#   ROS 2 ${ROS_DISTRO}  |  $(lsb_release -ds 2>/dev/null)"
  echo "#   captured $(date -u '+%Y-%m-%d %H:%M UTC')"
  echo "#"
  echo "# Regenerate:  bash ../../shared/screenshots/make_expected_output_w04.sh"
  echo "#"
  echo "# EXACT vs APPROXIMATE. Everything down to 'THE MODEL' is arithmetic and"
  echo "# reproduces digit for digit. The closing errors at the end come from a"
  echo "# simulator and depend on machine load: a student within about 20% of"
  echo "# those figures has the right answer. What must match is that the error"
  echo "# is non-zero and grows with distance travelled."
  echo

  echo "=== colcon build ==="
  ( cd "$WS" && colcon build --packages-select ee414_course 2>&1 | grep -vi warning )
  echo

  echo "=============================================================="
  echo "THE MODEL --- plain arithmetic, no ROS, no simulator"
  echo "=============================================================="
  echo
  run "ros2 run ee414_course wheels_to_body --table"
  run "ros2 run ee414_course wheels_to_body 0 10"
  run "ros2 run ee414_course body_to_wheels 0.2 1.0"
  run "ros2 run ee414_course body_to_wheels 0.5 3.0"

  echo "=============================================================="
  echo "QUATERNIONS"
  echo "=============================================================="
  echo
  run "ros2 run ee414_course quaternion_demo"

  echo "=============================================================="
  echo "INTEGRATION --- Euler against the exact arc"
  echo "=============================================================="
  echo
  run "ros2 run ee414_course dead_reckoning --compare"

  echo "=============================================================="
  echo "THE ROBOT DESCRIPTION"
  echo "=============================================================="
  echo
  run "check_urdf \$(ros2 pkg prefix --share ee414_course)/urdf/burger_min.urdf"
  run "grep -A7 'systems::DiffDrive' \$(ros2 pkg prefix --share ee414_course)/worlds/diff_drive_demo.sdf"

  echo "=============================================================="
  echo "TURTLESIM --- the nonholonomic constraint, and the square"
  echo "=============================================================="
  echo
  bg "ros2 run turtlesim turtlesim_node"
  sleep 6

  echo "--- pose before commanding pure sideways motion ---"
  run "ros2 topic echo /turtle1/pose --once"

  echo "--- command linear.y for two seconds (expect: nothing moves) ---"
  bash -c "source '$HERE/rosenv.sh'; timeout 2 ros2 topic pub -r 10 /turtle1/cmd_vel \
      geometry_msgs/msg/Twist '{linear: {y: 2.0}}'" >/dev/null 2>&1
  echo

  echo "--- pose after: identical to the last digit ---"
  run "ros2 topic echo /turtle1/pose --once"

  echo "--- the open-loop square (APPROXIMATE: see the header) ---"
  run "ros2 service call /reset std_srvs/srv/Empty '{}'"
  sleep 1
  run "ros2 run ee414_course drive --shape square --distance 2.0"

  if [ -n "${WITH_GAZEBO:-}" ]; then
    echo "=============================================================="
    echo "TURTLEBOT 3 IN GAZEBO --- the same node, the other robot"
    echo "=============================================================="
    echo
    bg "ros2 launch turtlebot3_gazebo empty_world.launch.py"
    sleep 45
    run "ros2 topic type /cmd_vel"
    run "ros2 run ee414_course drive --robot tb3 --shape square --distance 0.5 --speed 0.15 --turn-rate 0.5"
  else
    echo "=============================================================="
    echo "TURTLEBOT 3 IN GAZEBO --- not captured in this run"
    echo "=============================================================="
    echo
    echo "Re-run with WITH_GAZEBO=1 to include it. For reference, the figures"
    echo "recorded while preparing the cue sheet were:"
    echo
    echo "  \$ ros2 topic type /cmd_vel"
    echo "  geometry_msgs/msg/TwistStamped"
    echo
    echo "  \$ ros2 run ee414_course drive --robot tb3 --shape square \\"
    echo "        --distance 0.5 --speed 0.15 --turn-rate 0.5"
    echo "  CLOSING ERROR: 0.0213 m from where it started, 0.6 deg off heading"
    echo
  fi
} > "$OUT" 2>&1

echo "wrote $OUT"
wc -l "$OUT"
