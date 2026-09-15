#!/usr/bin/env bash
# Kill any simulator or ROS 2 CLI process left over from an interrupted run.
#
# This lives in its own file for one reason, and it is not tidiness.
#
# `ps | grep turtlesim | xargs kill -9` and `pkill -f turtlesim` both match the
# shell that is running them, because that shell's own command line contains
# the word. The shell dies mid-script, the kill list is never applied, and the
# caller sees a bare non-zero exit with no output. In this project that has now
# happened five times, in five different ad-hoc one-liners, and the `[t]` trick
# does not save you: it protects the `grep`, not the `bash -c '...'` above it
# whose argument holds the whole script text.
#
# A separate file cannot have the pattern in its command line. `bash
# kill_sims.sh` is all `ps` sees. That is the whole fix.
#
#   bash kill_sims.sh          # kill them
#   bash kill_sims.sh --list   # just show what would be killed
set -o pipefail

PATTERNS='turtlesim_node|rviz2|gz sim|ruby .*gz sim|ros2 topic pub|ros2 run ee414_course|ros2 run ros2_motion|ros2 run my_turtle_circle'

self=$$
mine=""
p=$self
while [ -n "$p" ] && [ "$p" != "1" ]; do
  mine="$mine $p"
  p=$(ps -o ppid= -p "$p" 2>/dev/null | tr -d ' ')
done

# The pattern is passed in the ENVIRONMENT, not on awk's command line: `awk -v
# pat="turtlesim_node|..."` puts the word into awk's own /proc/<pid>/cmdline,
# and awk then matches itself. Harmless here, since awk has exited by the time
# the kill is sent, but it is the same mistake one level down and it would bite
# a sibling process eventually. `kill_sims` is excluded for the same reason.
victims=$(ps -eo pid=,cmd= | \
  PAT="$PATTERNS" MINE=" $mine " awk '
    $0 ~ ENVIRON["PAT"] && $0 !~ /kill_sims/ {
      if (index(ENVIRON["MINE"], " " $1 " ") == 0) print $1
    }')

if [ "${1:-}" = "--list" ]; then
  [ -n "$victims" ] && ps -o pid=,cmd= -p $(echo "$victims" | tr '\n' ',' | sed 's/,$//') 2>/dev/null
  exit 0
fi

[ -z "$victims" ] && { echo "nothing to kill"; exit 0; }
echo "$victims" | xargs -r kill -INT 2>/dev/null
sleep 2
echo "$victims" | xargs -r kill -9 2>/dev/null
sleep 1
echo "killed: $(echo "$victims" | tr '\n' ' ')"
