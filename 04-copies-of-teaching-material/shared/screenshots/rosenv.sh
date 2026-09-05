# Environment for the screenshot capture harness.
#
# Sourced by every capture script and by every terminal the harness opens, so
# what is photographed is exactly what a student's terminal would print.
#
# Three things are stripped, each because it silently breaks a capture:
#
#   LOCPATH / GTK_*   When Claude Code or VS Code runs from a snap, the shell
#                     inherits paths into /snap/core20. Anything GUI launched
#                     with those inherited dies with
#                     `undefined symbol: __libc_pthread_init`.
#   /snap in LD_LIBRARY_PATH   Same failure, different route.
#   anaconda3         CMake's FindPython3 honours CONDA_PREFIX, so an interface
#                     package fails to build with `No module named 'em'` even
#                     though the system python3 has empy installed.
#
# None of these affect a clean Ubuntu 24.04 install. They are here so the
# harness runs on the instructor's machine, which has all three.

unset LOCPATH GTK_PATH GTK_EXE_PREFIX GTK_IM_MODULE_FILE GIO_MODULE_DIR GSETTINGS_SCHEMA_DIR
unset PYTHONPATH PYTHONHOME CONDA_PREFIX CONDA_DEFAULT_ENV
export XDG_DATA_DIRS=/usr/local/share:/usr/share
export PATH=$(echo "$PATH" | tr ':' '\n' | grep -v anaconda3 | paste -sd:)
export LD_LIBRARY_PATH=$(echo "$LD_LIBRARY_PATH" | tr ':' '\n' | grep -v '^/snap/' | paste -sd:)

source /opt/ros/jazzy/setup.bash

# The course workspace, so captures can show the week's own packages.
WS="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../code" 2>/dev/null && pwd)"
[ -n "$WS" ] && [ -f "$WS/install/setup.bash" ] && source "$WS/install/setup.bash"

# A domain of its own, so a capture never picks up a student's or a colleague's
# nodes on the same network.
export ROS_DOMAIN_ID=77
export TURTLEBOT3_MODEL=burger
export DISPLAY=${DISPLAY:-:1}
