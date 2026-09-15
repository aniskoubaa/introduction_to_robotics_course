# Week 4 — demo runbook and lab material

Two HTML documents, for two different rooms.

| File | For | Who reads it |
|---|---|---|
| `EE414_W04_demo_cue_sheet.html` | **Lecture A**, taught from the lectern | the instructor |
| `EE414_W04_hands_on_lab.html` | the **hands-on session**, worked at a keyboard | the students |

The cue sheet demonstrates a package that already works. The lab sheet takes a student who has
never created a ROS 2 package from an empty directory to a robot driving a circle they can
predict the radius of. They share a stylesheet and nothing else.

## The lab sheet

`EE414_W04_hands_on_lab.html` — six parts, about 90 minutes, each ending in a checkpoint the
student must be able to tick before going on.

| Part | What happens |
|---|---|
| Before you start | Three failures that print no useful message: Anaconda, an unsourced terminal, a snap terminal that cannot open a window. |
| 1 · Download and build | `mkdir src`, `git clone`, `colcon build --packages-select`. Why to name the packages rather than build the repository. |
| 2 · Run and observe | `cleaner` (the 2023 `clean.py`) and `mover` (`simple_turtlesim_motion.py`). Open loop against closed loop, in the same menu. Two documented failures, met on purpose. |
| 3 · How it moves | Topic, `Twist`, control loop. Three ideas and nothing else. Ends with a prediction: `R = v / ω = 2.0`. |
| 4 · Create a package | `ros2 pkg create`, and what each of the five generated files is for. Build it while it is still empty. |
| 5 · Write the node | **30 lines of Python**, typed not pasted, then the measurement against the prediction. |
| 6 · The same in C++ | Optional. Fills `ros2_motion_cpp`, which ships in the repository with no source file at all. |
| If it does not work | Fourteen error messages, every one of them produced on purpose on this machine, and what to do about each. |

The two files the students write are kept in `handson/`, so the instructor can paste a working
copy and so the checker can install them. `handson_check.txt` is the pass/fail table:

```bash
bash ../../shared/screenshots/verify_w04_handson.sh
```

It starts from an empty directory, clones the repository, and finishes by measuring the radius
of the circle the student's finished node actually draws. **24 of 24 rows pass**, including the
two rows that assert the 2023 code is still broken in the two ways the sheet warns about.

### Two faults in the 2023 code, both taught rather than hidden

1. **`cleaner`, any rotation above 180 degrees, never terminates.** It measures progress with
   `abs(start.theta - current.theta)`, and `theta` wraps at `±π`, so the measured angle can never
   exceed 180. This is the angle-wrapping bug from the lecture, in the code that taught this
   course for two years. The lab sheet asks the students to run it and press `Ctrl-C`.
2. **`mover` ends in `RCLError: publisher's context is invalid`.** It calls `rclpy.shutdown()`
   inside its timer callback and then publishes one more message. The turtle does stop correctly;
   the error arrives one instruction later. On Jazzy this is fatal, and it was not on the release
   the file was written for.

Neither is repaired in place. The repaired versions are the seven student programs in
`ee414_course`, and the contrast is the teaching.

## The cue sheet

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

Everything it runs lives in `../../../code/src/ee414_course/`.

## One package

Until 13 September 2026 there were two: `ee414_w04_demo` in this repository for the lecture, and
`ee414_course` in `~/ros2_ws` for the students. Two copies of overlapping code in two places
drifted, as two copies of anything do. They are now **one package in one repository**, with
twenty executables in three groups:

| Group | Count | Lineage |
|---|---|---|
| Lecture programs | 6 | written for this deck — make a slide's claim visible |
| Student programs | 7 | [ros2_course_packages](https://github.com/aniskoubaa/ros2_course_packages), corrected and extended |
| Beginner versions | 7 | one short version of each student program, for the projector |

The cue sheet uses whichever makes the point better and says which it is using. Three places
where a student program wins:

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
point at the full version afterwards. `Ctrl-C` stops the turtle in all seven —
a limitation recorded here on 13 September was withdrawn on the 15th when the
harness that measured it turned out not to be signalling anything; their README
tells that story. `beginner_check.txt` is their pass/fail table:

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

`EE414_W04_hands_on_lab.html` is the step-by-step sheet with checkpoints, and it is authored and
checked. What is still missing is a **starter package with one `TODO` per concept** — the lab
sheet gives the finished thirty lines rather than a skeleton, which is the right choice for a
first package and the wrong one for the second. The `drive` node in `ee414_course` is the
*worked* version of what a later session asks students to build, so it should stay out of their
hands until they have written their own.

| Item | Status |
|---|---|
| `EE414_W04_demo_cue_sheet.html` — live-demo runbook for Deck A | ✅ |
| `EE414_W04_hands_on_lab.html` — student lab sheet, 6 parts, checkpoints | ✅ 24/24 checked |
| `code/src/ee414_course/` — one package, built and run | ✅ 20 executables |
| `expected_output.txt` — from a real run | ✅ |
| `command_check.txt` — every cue-sheet command, pass/fail | ✅ |
| Code snapshots in the cue sheet, generated from source | ✅ 13 full + 7 beginner |
| Beginner versions of the seven student scripts | ✅ 7, checked |
| `Ctrl-C` clean on every node, robot stopped first | ✅ |
| Common-failure list | ✅ in the cue sheet, and above |
| Lecture B step-by-step lab sheet with checkpoints | ✅ `EE414_W04_hands_on_lab.html` |
| Starter versions of the nodes, one `TODO` per concept | ❌ |
| ROS 2 Jazzy screenshots specific to this week | ❌ needs a clean-desktop capture run |
