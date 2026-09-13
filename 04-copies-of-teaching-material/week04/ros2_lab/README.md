# Week 4 — demo runbook and lab material

`EE414_W04_demo_cue_sheet.html` is the **live-demo runbook for Lecture A** — open it in a
browser. Every slide that has something to run, one command per line with its own copy button,
a plain-English explanation of each line, and the exact output to expect. It is a single
self-contained file: no images, no sibling folders, works offline.

Each concept also carries a **collapsed code snapshot** — a blue `Code ·` row that opens the
handful of lines in the source that the demonstration is about. Seven of them are preceded by a
green `Simple ·` row holding the same idea from the beginner scripts, so the room reads the
forty-line version first and the production version second. They are closed by default, so
the room reads the command and its output first, and the source is there for the question from
the third row. They are *generated from the files on disk* by
`../../shared/screenshots/snippets.py`, so the handout cannot drift from the code that just ran.

Everything it runs lives in `../../../code/src/ee414_w04_demo/`, plus a handful of commands
from `~/ros2_ws/src/ee414_course/` — see [Two packages](#two-packages) below.

## Two packages

| | `ee414_w04_demo` | `ee414_course` |
|---|---|---|
| Where | `code/src/` in this repo | `~/ros2_ws/src/` |
| For | the **lecture** — make a slide's claim visible | the **students** — the shape they will write themselves |
| Lineage | written for this deck | [ros2_course_packages](https://github.com/aniskoubaa/ros2_course_packages), corrected and extended |

They overlap deliberately. Both workspaces can be sourced in one terminal; the
package names do not collide. The cue sheet uses whichever makes the point
better and says which it is using. Three places where the student package wins:

- **Slide 13** — `ros2 run ee414_course angle_wrap` replays the wrap bug from the
  2023 `clean.py`: a `rotate(40°)` that stops after **12 degrees**. Far stronger
  than the `python3 -c` one-liner.
- **Slide 17** — `ros2 run ee414_course nonholonomic` walks all six Twist fields
  with before/after poses, instead of testing `linear.y` by hand.
- **Slide 38** — `ros2 run ee414_course go_to_goal` is the closed-loop contrast.
  There was no equivalent before; open loop now has something to be the opposite of.

## What is in the package

| Command | Needs | Slide | What it demonstrates |
|---|---|---|---|
| `wheels_to_body --table` | nothing | 20, 23 | Forward kinematics as arithmetic. Four wheel-speed cases, four path shapes. Stopping the left wheel gives `R = 0.0800`, exactly `L/2`. |
| `body_to_wheels V W` | nothing | 21, 22 | Inverse kinematics, with a round-trip check. Ask for too much and it prints the saturation and the scaled command that would fit. |
| `quaternion_demo` | nothing | 10, 11 | Four parts: a flat robot's quaternion is its heading; the unit-norm constraint; **drift measured over 200,000 compositions** and repaired in one line; gimbal lock watched as `1/cos(pitch)` runs to infinity. |
| `dead_reckoning --compare` | nothing | 29 | Euler against the exact arc on a quarter circle whose answer trigonometry knows. **Euler halves with the timestep and never reaches zero; the arc is exact at `1e-16` every time.** |
| `pose_watch` | a simulator | 9, 12 | Subscribes to `/turtle1/pose` **and** `/odom` at once, so the float-theta and the quaternion arrive side by side in one terminal. |
| `drive --shape ...` | a simulator | 31, 35, 38 | Open-loop primitives: straight, rotate, arc, square, spiral. Every duration is `distance ÷ speed`. Reports the closing error and corrects nothing. |
| `dead_reckoning --robot tb3` | TurtleBot 3 | 36 | Integrates `/cmd_vel` both ways and holds both estimates against the simulator's truth. |
| `view_model.launch.py` | — | 25 | RViz2 + joint sliders on the minimal URDF. |
| `urdf/burger_min.urdf` | — | 26 | The twelve-line differential drive. `r` is written down; **`L` is not** — it is the gap between two joint origins. |
| `worlds/diff_drive_demo.sdf` | Gazebo | 27 | The `DiffDrive` plugin: the one place that reads both constants at run time. |

The first four need **no simulator at all** and are the spine of the lecture. If Gazebo will not
start five minutes before class, the session still works.

## The demonstration that earns its time

Slide 17, and it takes thirty seconds:

```bash
ros2 topic echo /turtle1/pose --once                  # write the three numbers down
ros2 topic pub -r 10 /turtle1/cmd_vel geometry_msgs/msg/Twist '{linear: {y: 2.0}}'
ros2 topic echo /turtle1/pose --once                  # identical to the last digit
```

A valid command, published cleanly, that moves the robot not at all. No error is raised because
nothing is wrong with the *message* — the field exists, the motion does not. That is
`ẋ sin θ − ẏ cos θ = 0` being obeyed, and it is the difference between a constraint students
memorise and one they have watched.

## Three traps, all silent

All three were hit while preparing this material, on the teaching machine.

1. **`/cmd_vel` carries `TwistStamped`, not `Twist`**, on Jazzy's TurtleBot 3 bridge. Publish the
   wrong type and ROS 2 raises nothing: the types do not match, no connection is made, the
   publisher reports success, the robot sits still. `ros2 topic type /cmd_vel` before you debug
   anything else. The nodes here resolve the type at start-up (`twist_compat.py`) and say which
   one they found.
2. **Anaconda shadows the system Python.** `import rclpy` then fails with
   `No module named 'rclpy._rclpy_pybind11'`. `conda deactivate`. Note `ros2 run` is unaffected —
   only `python3 script.py` breaks, which is exactly what a student types.
3. **A terminal opened by a snap application cannot start a GUI.** turtlesim, RViz2 and Gazebo die
   with `undefined symbol: __libc_pthread_init`. The culprit is `LOCPATH` (and `GTK_PATH`,
   `GTK_EXE_PREFIX`) pointing into `/snap/code/<rev>/`.

Traps 2 and 3 are handled by `../../shared/screenshots/rosenv.sh`, which is why the capture
harness works. **Trap 3 is additionally fixed for interactive shells** by a block at the end of
`~/.bashrc` on the teaching machine: it strips those variables when they point into `/snap`, so
any ordinary terminal can start turtlesim, RViz2 and Gazebo. It is a no-op on a clean machine,
and it does not apply to non-interactive `bash -c` — use `rosenv.sh` there.

## Beginner versions, for the explanation

`code/src/ee414_course/ee414_course/beginner_student_freindly/` holds a short
version of each of the seven student scripts — about forty lines, no argparse,
no shared helpers, one idea each. Put these on the projector while explaining;
point at the full version afterwards. They have their own README, including a
**known limitation about Ctrl-C during a drive** that is worth reading before
the lecture. `beginner_check.txt` is their pass/fail table:

```bash
bash ../../shared/screenshots/verify_beginner_scripts.sh
```

## Every command, checked

`command_check.txt` is a pass/fail table covering **every command in the cue sheet**, run in
lecture order against real simulators:

```bash
bash ../../shared/screenshots/verify_w04_commands.sh
WITH_GAZEBO=1 bash ../../shared/screenshots/verify_w04_commands.sh   # also TurtleBot 3
```

Long-running commands are interrupted the way a lecturer interrupts them — SIGINT to the process
group, which is what `Ctrl-C` sends — and are required to exit 0 with no traceback. That is a real
requirement, not a formality: before this check existed, `Ctrl-C` on any of these nodes printed
twenty lines of `RCLError: publisher's context is invalid`, **and never delivered the stop
message**, so the robot kept driving. See `graceful.py` in both packages.

## Expected output

`expected_output.txt` is generated from a real run, never typed by hand:

```bash
bash ../../shared/screenshots/make_expected_output_w04.sh
WITH_GAZEBO=1 bash ../../shared/screenshots/make_expected_output_w04.sh   # also TurtleBot 3
```

**Read the header of that file before marking anything.** The arithmetic sections reproduce digit
for digit. The closing errors do not: they come from a simulator and depend on machine load. Four
consecutive turtle squares here gave 0.209, 0.221, 0.232 and 0.252 m. What must be true of a student's answer
is that the error is **non-zero and grows with distance travelled** — not that it matches a
particular number.

## Lecture B

This folder currently serves **Lecture A**. Lecture B's lab sheet — the step-by-step with
checkpoints, and the starter package with one `TODO` per concept — is not yet authored. The
`drive` node here is the *worked* version of what Lecture B asks students to build, so it should
stay out of their hands until they have written their own.

| Item | Status |
|---|---|
| `EE414_W04_demo_cue_sheet.html` — live-demo runbook for Deck A | ✅ |
| `code/src/ee414_w04_demo/` — working nodes, built and run | ✅ |
| `~/ros2_ws/src/ee414_course/` — student scripts, built and run | ✅ 7 programs |
| `expected_output.txt` — from a real run | ✅ |
| `command_check.txt` — every cue-sheet command, pass/fail | ✅ |
| Code snapshots in the cue sheet, generated from source | ✅ 13 full + 7 beginner |
| Beginner versions of the seven student scripts | ✅ 7, checked |
| `Ctrl-C` clean on every node, robot stopped first | ✅ |
| Common-failure list | ✅ in the cue sheet, and above |
| Lecture B step-by-step lab sheet with checkpoints | ❌ |
| Starter versions of the nodes, one `TODO` per concept | ❌ |
| ROS 2 Jazzy screenshots specific to this week | ❌ needs a clean-desktop capture run |
