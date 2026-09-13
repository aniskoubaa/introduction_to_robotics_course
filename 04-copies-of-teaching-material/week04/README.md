# Week 04 — Differential-Drive Kinematics

| | |
|---|---|
| **Lecture A (1.5 h)** | Pose and velocity in the plane; the differential-drive model; wheel odometry and its error sources |
| **Lecture B (1.5 h) — ROS 2** | Open-loop motion: `/cmd_vel` and `/odom`; straight-line and rotation primitives in Gazebo |
| **CLO served** | CLO 2, CLO 3 |
| **Assessment this week** | Quiz 2 |
| **Reading** | see `../../readings/topic02_kinematics_and_control/` |

## Status

| Artifact | Path | Status |
|---|---|---|
| Lecture deck | `slides/EE414_W04A_differential_drive.tex` / `.pdf` | ✅ 40 slides |
| Lecture deck | `slides/EE414_W04B_open_loop_motion.tex` / `.pdf` | ✅ 35 slides |
| Exercise set + key | `exercises/EE414_W04_exercises.pdf` / `_solutions.pdf` | ❌ not authored |
| Demo runbook (Lecture A) | `ros2_lab/EE414_W04_demo_cue_sheet.html` | ✅ 40 commands, all run · 13 code snapshots |
| ROS 2 demo package | `../../code/src/ee414_w04_demo/` | ✅ 6 programs · URDF · SDF world · launch |
| Expected-output transcript | `ros2_lab/expected_output.txt` | ✅ generated from a real run |
| Command check (every line, pass/fail) | `ros2_lab/command_check.txt` | ✅ full run incl. Gazebo |
| ROS 2 lab sheet (Lecture B) | `ros2_lab/README.md` | ⚠️ Lecture A covered; B's checkpoint sheet not authored |
| ROS 2 starter package (Lecture B) | `../../code/src/` | ❌ not authored |

## Lectures

_Lecture B is 35 pages — 29 authored frames plus 6 section dividers, the same shape
as Week 3. Lecture A is 40: five frames were added after first authoring — the
quaternion rationale and its drawn companion, and the three-slide bridge from the
kinematic constants to the robot description._

| File | Duration | Contents |
|---|---|---|
| `slides/EE414_W04A_differential_drive.tex` / `.pdf` | 1.5 h · 40 slides | Pose in the plane · why a quaternion, and what gimbal lock looks like · velocity in the body frame · the differential-drive model, forward and inverse · the ICC and the arc · where `r` and `L` live: a minimal URDF and the Gazebo diff-drive plugin · integrating to a position · wheel odometry and its six error sources · open loop defined |
| `slides/EE414_W04B_open_loop_motion.tex` / `.pdf` | 1.5 h · 35 slides | The two topics · motion from the terminal · the four `Twist` primitives · an rclpy motion node on a timer · `move_straight`, `rotate_in_place`, the square, the spiral · measuring the error from `/turtle1/pose` · the same node on TurtleBot 3 with `/cmd_vel` and `/odom` |

Build: `pdflatex <file>.tex` **three times** (the section dividers position from the `.aux`). Shared preamble at `../shared/ee414-beamer-preamble.tex`.

## Lecture B — the ROS 2 session

**Goal:** Open-loop motion: `/cmd_vel` and `/odom`; straight-line and rotation primitives in Gazebo

Every B session ends with something that **runs**. Students leave the room having seen
their own node print, move, or draw in RViz2 — never with a half-typed file.

| Item | Status |
|---|---|
| Lab sheet (step-by-step, 1.5 hours, checkpoint at each step) | ❌ |
| Starter package under `code/src/` | ❌ starter versions; the worked nodes exist |
| Expected-output transcript (for the key) | ✅ `ros2_lab/expected_output.txt` |
| Common-failure list (what breaks, and the fix) | ✅ `ros2_lab/README.md` |

## Teaching Lecture A from the machine

`ros2_lab/EE414_W04_demo_cue_sheet.html` is the runbook: open it in a browser and teach from it
beside the slides. 40 commands, each with a copy button, an explanation and its real output, and
a collapsed **code snapshot** on each concept that opens the lines of source it is about.

Every one of those commands has been run end to end on the teaching machine, in lecture order,
against real simulators — `ros2_lab/command_check.txt` is the table. `Ctrl-C` is safe on every
node: it stops the robot first, prints the summary, and exits cleanly.

The spine of the lecture — forward and inverse kinematics, the quaternion argument, and Euler
against the exact arc — runs as **plain arithmetic with no ROS and no simulator**. That is
deliberate: the model is two lines of algebra, and students should see it as such before it is
wrapped in a node. It also means the session survives Gazebo refusing to start.

Three demonstrations are worth protecting if time runs short:

1. **Slide 17, thirty seconds.** Command `linear.y` on the turtle and read the pose before and
   after. Identical to the last digit. The nonholonomic constraint stops being a formula.
2. **Slide 25, one command.** `tf2_echo wheel_left_link wheel_right_link` answers `0.160` — `L`
   measured from the transform tree, because it is nowhere in the URDF as a number.
3. **Slide 29, one command.** `dead_reckoning --compare`: Euler's error halves with the timestep
   and never vanishes; the exact arc sits at `1e-16` at every timestep.

One honest caveat to carry into Week 5: in the *live* comparison at 20 Hz the two integrators
agree to the millimetre, because one step turns 0.02 rad. The centimetres of drift are the robot
— acceleration, slip, mass — not the integration method. Saying so is what makes slide 35's list
credible.

## Teaching order, and where it came from

The sequence is the one used in the 2020 *ROS for Beginners: Basics, Motion and OpenCV*
course, kept because it works: **the turtle draws the motion before any equation is
integrated**, and the four `Twist` patterns (straight / rotate / arc / spiral) are met as a
table before any of them is coded. Turtlesim comes first for one concrete reason —
`turtlesim/msg/Pose` hands you `theta` as a float, so a student writes a rotation before
meeting a quaternion.

Two deliberate departures from the legacy module:

1. **Everything in Week 4 is open loop.** The legacy `move_straight` measured distance from the
   pose callback and stopped when it was reached — that is a closed loop, and Week 5 owns it.
   Here the pose is subscribed to in order to *measure* the closing error and never to correct
   it, so that Week 5 has a concrete failure to fix.
2. **The session ends on TurtleBot 3 in Gazebo**, as the week specification requires: the
   identical node, `/cmd_vel` and `/odom`, and the same square that closes on the turtle and
   does not close on the robot. The two closing errors, side by side, are the deliverable.

### Reused figures

`slides/figures/legacy/` holds four turtlesim captures lifted from the 2020 deck
(`anis_slides_legacy/ros-for-beginners-I-2020-slides.key.pdf`, pages 202, 223, 234, 237).
The turtlesim window is unchanged under ROS 2, and nothing version-specific is visible in any
of them. Each carries its attribution on the slide via `\figslide`.

`slides/figures/shots/` holds two real ROS 2 Jazzy captures reused from Week 3
(`a03_pose_echo.png`, `a15_tb3_gazebo.png`).

**Still missing:** ROS 2 Jazzy captures specific to this week — the square's trail in
turtlesim, the same square in Gazebo, and the two printed closing errors. They need a capture
run on the Linux box, in the manner of `../shared/screenshots/shoot_w03.py`.

## Teaching notes

_To be written after first delivery._

## Consistency checks

Figures stated in this week's material must match the approved specification:

- Assessment weights — participation 5, assignments 15, quizzes 5, MT1 15, MT2 15, project 20, final 25.
- The four CLOs — EXPLAIN · ANALYZE · DEVELOP · EVALUATE.
- ROS 2 distribution pinned in `../../setup/README.md`. Do not name a version anywhere else.
