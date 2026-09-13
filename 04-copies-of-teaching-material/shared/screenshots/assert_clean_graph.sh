# Refuse to capture anything while something else is already driving the robot.
#
# Sourced by the capture and verification harnesses. It exists because a
# `ros2 topic pub -r 10 /turtle1/cmd_vel ...` left running in a forgotten
# terminal drove the turtle into the wall *during* a capture. The transcript
# came out with a 2.86 m closing error on a 2 m square, and a "nothing moved"
# demonstration in which the turtle had plainly moved. Nothing errored. The
# numbers were simply wrong, which is the worst way for a harness to fail.
#
# Publishers only: `ros2 run turtlesim turtlesim_node` is fine to leave up, and
# the ros2 daemon is not a robot. The search is in Python rather than
# `pgrep -f`, which matches the shell doing the searching -- see the module.

assert_clean_graph() {
    local here strays
    here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    strays=$(python3 "$here/find_stray_publishers.py")
    if [ -n "$strays" ]; then
        echo "REFUSING TO RUN: something is already publishing velocities." >&2
        echo "$strays" >&2
        echo >&2
        echo "Stop it (Ctrl-C in its terminal, or kill the pid above) and re-run." >&2
        return 1
    fi
    return 0
}
