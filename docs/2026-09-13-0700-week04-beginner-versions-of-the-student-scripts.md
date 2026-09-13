# Week 4 — beginner versions of the seven student scripts

**2026-09-13 07:00 UTC.** Requested during preparation for the Week 4A
lecture: a short version of each `ee414_course` script, "only a few lines of
code with basic instruction for education purpose", to put on the projector
while explaining, with the full documented version read afterwards.

## What was built

`ee414_course/beginner_student_freindly/`, seven scripts, one per idea, 36–90
lines each against 91–205 for the full versions.

| Beginner | Full | The one idea |
|---|---|---|
| `simple_kinematics.py` | `kinematics.py` | forward and inverse, four lines of algebra |
| `simple_angle_wrap.py` | `angle_wrap.py` | never subtract two headings directly |
| `simple_pose_reader.py` | `pose_monitor.py` | node, subscription, callback |
| `simple_nonholonomic.py` | `nonholonomic.py` | `linear.y` is legal and does nothing |
| `simple_move.py` | `turtle_mover.py` | open loop: `seconds = distance / speed` |
| `simple_square.py` | `move_rotate.py` | four timed sides do not close |
| `simple_go_to_goal.py` | `go_to_goal.py` | closed loop: look, then decide |

Each is registered in `setup.py`, so they run with `ros2 run ee414_course
simple_*` like everything else.

Deliberately absent: argparse (constants at the top instead, so changing one
mid-lecture is a one-line edit the room can follow), TurtleBot 3 support,
message-type resolution, and any import from a sibling module. Each file reads
top to bottom on its own. Deliberately present: `stop(pub)`, which publishes an
empty `Twist` five times, because a topic does not retry.

## Everything was run

`verify_beginner_scripts.sh` (new, in `shared/screenshots/`) runs all seven and
writes `week04/ros2_lab/beginner_check.txt`. Result: **7 of 7 scripts pass**,
plus one failing assertion described below.

## Defects found and fixed

| # | Where | Fault | Fix |
|---|---|---|---|
| 1 | `simple_pose_reader` | printed all 62 pose messages a second — an unreadable wall on a projector | print one in twenty |
| 2 | `simple_go_to_goal` | `angular.z` unclamped: a heading error of pi asked for 12.6 rad/s and the turtle spun violently | `clamp(..., MAX_W)`, which also teaches saturation |
| 3 | `simple_go_to_goal` | stop published once, then `rclpy.shutdown()` immediately — the message could be dropped | shared `stop(pub)` helper, five messages |
| 4 | all five ROS scripts | `rclpy.init()`'s own SIGINT handler kills the context before a stop can be published | `SignalHandlerOptions.NO` plus an explicit `signal.signal(SIGINT, default_int_handler)` |

## A defect in the verification harness itself

The first interrupt test reported two scripts hanging and three passing. All
five results were wrong.

`verify_w04_commands.sh` starts long-running commands as background jobs from a
non-interactive shell. POSIX requires bash to set **`SIGINT` to `SIG_IGN`** for
such jobs, and that disposition is inherited all the way down to Python. So the
harness was signalling a process tree that could not be signalled, and reporting
whatever the fallback `kill -9` produced. Confirmed directly:

```
background, job control OFF : SIGINT disposition: 1          (SIG_IGN)
background, job control ON  : <built-in function default_int_handler>
```

`set -m` has been added to both harnesses. This matters beyond cosmetics: with
it off, a node that relies on Python's default Ctrl-C handling is marked broken,
and a node that installs its own handler — which `graceful.py` does — passes for
the wrong reason. The existing `command_check.txt` results were real, but the
check was weaker than it claimed. **`command_check.txt` should be regenerated
with the fixed harness** (`WITH_GAZEBO=1 bash verify_w04_commands.sh`); it had
not been re-run when this entry was written.

The three "passing" scripts in that first run had simply finished on their own
before the interrupt arrived. A test that cannot fail is not a test, and a
long-running command that completes early makes an interrupt check vacuous —
worth remembering for the next harness.

## Known limitation, not fixed

`simple_square` and `simple_go_to_goal`, interrupted **part way through a
motion**, can leave the turtle coasting at its last commanded velocity.
Measured after the fixes above: 3 of 3 interrupted `simple_square` runs left
`linear_velocity: 1.0`; 2 of 3 `simple_go_to_goal` runs left `angular_velocity:
-2.0`. The `finally: stop(pub)` block is present and correct, and an
instrumented run showed it never executing — under `ros2 run` the interrupt is
not reaching the node in time.

This is the same class of fault `graceful.py` was written to fix. The full
versions do not have it: they poll an interrupt flag rather than relying on the
exception arriving, and all of them pass the interrupt check. Resolving it for
the beginner scripts means either importing `graceful` — which costs the
standalone readability that is their whole purpose — or finding why `ros2 run`
swallows the signal. Neither was done.

For tomorrow: let the scripts finish (15 s for the square, 3 s for the move), or
use `ros2 service call /reset std_srvs/srv/Empty '{}'`, which stops and
re-centres the turtle and is already in the cue sheet. The limitation is written
into `beginner_student_freindly/README.md` so it is not rediscovered by
surprise.

## Also in this commit

`code/src/ee414_course/` is now a copy of the `~/ros2_ws` package. It had never
been in the repository, so nothing in `ee414_course` — the seven student scripts
the cue sheet uses on slides 13, 17 and 38 — was under version control.
