# Week 4A — every command run end to end, and code snapshots in the cue sheet

**2026-09-12 23:20** · follows `2026-09-12-2125-week04-lecture-a-live-demo-package.md`

Two pieces of work, both aimed at the same thing: opening the cue sheet tomorrow
and executing it without stopping to debug.

---

## 1 · Every command run, in lecture order, against real simulators

`shared/screenshots/verify_w04_commands.sh` runs all forty commands in
`EE414_W04_demo_cue_sheet.html` — turtlesim up, then RViz2, then Gazebo — and writes a pass/fail
table to `week04/ros2_lab/command_check.txt`.

The part that found real bugs is how it ends the long-running ones. A `timeout` sends `SIGTERM`,
which is *not* what `Ctrl-C` does. The harness sends `SIGINT` to the whole process group, the way
a terminal does, and requires exit 0 with no traceback.

One distinction the harness has to make: **our** nodes must exit 0 — that is the entire point of
`graceful.py` — but the ROS 2 CLI tools (`ros2 topic pub`, `tf2_echo`) exit non-zero on `SIGINT`
and always have. They are designed to be interrupted and print nothing when they are. So
`check_interrupt` is for ours and `check_interrupt_cli` for theirs; both refuse a traceback, only
the first demands exit 0. Calling the second one out here rather than quietly widening the first
is the difference between a check and a formality.

### Eight defects found and fixed

| # | Symptom | Cause | Fix |
|---|---|---|---|
| 1 | `Ctrl-C` on **any** node: 20 lines of `RCLError: publisher's context is invalid`, exit 1 | `rclpy.init()` installs a SIGINT handler that shuts the context down immediately; everything after it — including `stop()` — then fails | `graceful.py` in both packages: no rclpy signal handler, our own sets a flag, loops notice it, context stays valid |
| 2 | **The robot kept driving after `Ctrl-C`** | consequence of 1: the zero `Twist` was never delivered, and a differential drive holds the last velocity it was given | same |
| 3 | `turtle_mover` reported **90.4 % error** on a drive that was accurate to 1 % | `start_pose` was read before the post-`/reset` pose arrived, so the error was measured from where the turtle had been *before* it was teleported to the middle | drop the stale pose, spin until a fresh one arrives |
| 4 | `go_to_goal` printed "Gave up after 60 s" when interrupted at 3 s | the timeout message was on the only exit path | report the interrupt instead; never a timeout that did not happen |
| 5 | `nonholonomic` interrupted mid-way printed its whole conclusion as if it had finished | same shape | guard the summary |
| 6 | `gz sim` on the demo world opened looking at the horizon: **empty grey plane, no robot** | no `<gui>` in the SDF, so the stock camera sits 6 m back — and a Burger is 14 cm long | Gazebo's own default `gui.config` copied in verbatim with **one** line changed, `camera_pose` |
| 7 | A capture ran while a forgotten `ros2 topic pub` was still driving the turtle: a 2 m square "closed" 2.86 m out, and the *nothing moved* demonstration recorded a turtle that had plainly moved | nothing errors; a stray publisher publishes for ever and says nothing | `assert_clean_graph.sh`, sourced by both harnesses: they refuse to run while anything is publishing velocities. Also trap H in the sheet, because it will happen in a lecture |
| 8 | The sheet claimed Euler and the arc integrator "agree to the millimetre" in the live TurtleBot 3 comparison — **they do not** | the numbers originally recorded came from a robot that was *not* at the origin, so a large shared offset swamped the difference between the methods | re-measured from the origin and rewritten: both start 1.6 cm out (that is the robot); over the half circle Euler holds near 13 mm while the arc falls to 6 mm |

Defect 1 is the one worth remembering. It is not cosmetic: the traceback is the visible half, and
the robot still driving is the half that matters. `code/README.md` now carries the pattern.

Along the way: `~/EE414` is now a symlink to this repository, so the cue sheet's setup line runs
verbatim; and `shared/screenshots/rosenv.sh` sources `~/ros2_ws` too, since from Week 4 the sheets
use both packages in one terminal.

---

## 2 · Collapsed code snapshots, generated from the source

Thirteen `<details class="code">` blocks, one or more per tab, each opening the handful of lines
the demonstration is actually about:

| Tab | Snapshot |
|---|---|
| 1 · Pose | `quat_from_yaw` / `yaw_from_quat`; `normalize_angle` |
| 2 · Velocity | `resolve_twist_type`; setting any of the six Twist fields |
| 3 · The model | forward kinematics; inverse kinematics; what saturation does |
| 4 · r and L | the wheel in URDF; the `DiffDrive` plugin in SDF |
| 5 · Integrating | `step_euler` and `step_exact_arc`, side by side |
| 6 · Odometry | what `pose_watch` does with `/odom`'s quaternion |
| 7 · Open loop | `send_for` — the whole of open loop; then `go_to_goal`'s closed loop, adjacent |

They are **closed by default**: the room reads the command and its output first, and the source is
there for the question from the third row. Blue, so they never read as expected output (green) or
as a deliberate failure (red).

They are generated, not pasted. `shared/screenshots/snippets.py` names a file and a line range;
`insert.py` anchors each block on the command it belongs to and drops it after that cue's steps.
Long docstrings are squashed to their first line — the reasoning belongs in the file, the
projector needs the arithmetic. Re-running `insert.py` on a sheet that already has snapshots
refuses rather than duplicating; regenerate from a copy taken before they were added.

The consequence worth having: **the handout cannot drift from the code it quotes.** Edit
`drive.py`, re-run the two scripts, and the sheet is right again.

---

## Verified

- HTML nesting checked with a parser: no mismatched or unclosed tags.
- No horizontal page overflow at 520, 700 or 900 px (`scrollWidth == clientWidth`).
- Expanded and collapsed states rendered and read back at 1200 px and 520 px.
- `command_check.txt` regenerated from a full `WITH_GAZEBO=1` run: turtlesim, RViz2, the
  standalone demo world and TurtleBot 3 in Gazebo, all brought up in turn.
  **40 passed, 0 failed.**

  The first pass was 36/4. None of the four was adjusted away by loosening the threshold: three
  were `ros2 topic pub` and one was `tf2_echo` exiting non-zero on `SIGINT`, which is the ROS 2
  CLI's own long-standing behaviour and prints nothing on screen. The harness now says which
  commands are ours and which are the CLI's, and `tf2_echo` — a "Ctrl-C when it lands" command —
  moved onto the interrupt path where it belonged.
- The live integrator comparison re-measured on a robot starting at the origin, twice, before the
  sheet's wording was changed.
