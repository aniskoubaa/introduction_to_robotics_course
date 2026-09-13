# Week 4 Lecture A — a runnable demonstration layer

**Date:** 2026-09-12
**Scope:** `code/src/ee414_w04_demo/`, `week04/ros2_lab/`, `shared/screenshots/make_expected_output_w04.sh`

## What was asked for

Teach Week 4A from the machine rather than from the slides alone: an HTML page of commands to
run, with small programs that show the concepts by executing — turtlesim, TurtleBot 3, a simple
URDF — so the lecture is a demonstration and the deck is the reference.

## What was built

A colcon package, `ee414_w04_demo`, and a runbook keyed to the deck's 40 slides.

| Artifact | Purpose |
|---|---|
| `week04/ros2_lab/EE414_W04_demo_cue_sheet.html` | The runbook. 43 commands, copy buttons, real outputs, keyed to slide numbers. Self-contained, offline. |
| `ee414_w04_demo/wheels_to_body.py` | Forward kinematics. No ROS. |
| `ee414_w04_demo/body_to_wheels.py` | Inverse kinematics with a round-trip assertion and saturation reporting. No ROS. |
| `ee414_w04_demo/quaternion_demo.py` | Four parts: heading↔quaternion, the unit-norm constraint, measured drift over 200,000 compositions, gimbal lock. No ROS. |
| `ee414_w04_demo/dead_reckoning.py` | `--compare`: Euler vs exact arc, offline. Default: live, integrating `/cmd_vel` against simulator truth. |
| `ee414_w04_demo/pose_watch.py` | `/turtle1/pose` and `/odom` side by side — float theta against quaternion. |
| `ee414_w04_demo/drive.py` | Open-loop primitives; reports the closing error and corrects nothing. |
| `ee414_w04_demo/twist_compat.py` | Resolves the `/cmd_vel` message type from the graph at run time. |
| `urdf/burger_min.urdf`, `launch/view_model.launch.py`, `rviz/model.rviz` | The twelve-line differential drive, openable in RViz2. |
| `worlds/diff_drive_demo.sdf` | The `DiffDrive` plugin, with `wheel_separation` and `wheel_radius` as the point. |
| `shared/screenshots/make_expected_output_w04.sh` | Generates `expected_output.txt` from a real run. Reuses the existing `rosenv.sh`. |

## Decisions worth recording

**The spine of the lecture runs without ROS.** Forward and inverse kinematics, the quaternion
argument and the Euler-vs-arc comparison are plain Python. The model is two lines of algebra and
students should meet it as such before it is wrapped in a node — and the session then survives
Gazebo failing to start, which is the realistic classroom risk.

**`L` is demonstrated, not asserted.** Slide 25 claims the wheel separation is never written in a
URDF. `ros2 run tf2_ros tf2_echo wheel_left_link wheel_right_link` returns
`Translation: [0.000, -0.160, 0.000]` — the constant measured out of the transform tree rather
than read from the file. That is the slide's claim, proved in one command.

**Week 8 is not pre-empted.** The URDF here has no inertia, no collision and no sensors, and both
the file and the cue sheet say so. It exists only to locate `r` and `L`.

## Three environment traps, all silent, all hit during preparation

1. **`/cmd_vel` carries `TwistStamped` on Jazzy's TurtleBot 3 bridge, not `Twist`.** A publisher
   of the wrong type produces no error at all — the types do not match, no connection is made,
   the publisher succeeds and the robot does not move. Cost the first attempt at the Gazebo
   square, which reported a closing error of 0.0000 m because nothing ever moved. Handled by
   `twist_compat.py`, and taught deliberately at slide 34 because students will meet it alone.
2. **Anaconda shadows the system Python**, so `import rclpy` fails. `ros2 run` is unaffected —
   only `python3 script.py`, which is what a student types. Already known from Week 3.
3. **A terminal opened by the VS Code snap cannot start a GUI.** turtlesim, RViz2 and Gazebo die
   in the dynamic loader. Already handled by `shared/screenshots/rosenv.sh`.

Traps 2 and 3 were already documented in the shared harness; trap 1 is new and is now in
`code/README.md`.

## One correction made during the work

The first `drive.py` paced its publish loop with `rclpy.spin_once(timeout_sec=period)`. That
returns as soon as a callback is ready, and the pose arrives at 62 Hz, so the loop ran far faster
than the intended 20 Hz and every motion finished short — a commanded square closed 110° off
heading. Pacing on `time.monotonic()` brought it to the honest 2–3%. **The bug mattered
pedagogically, not just technically:** an inflated error would have taught the wrong lesson about
where open-loop error comes from. The comment in `send_for()` records why the obvious formulation
is wrong.

## An honest caveat for Week 5

In the *live* comparison at 20 Hz, Euler and the exact arc agree to the millimetre — one step
turns 0.02 rad, far too little for the integration method to matter. The centimetres of drift are
the robot: acceleration limits, slip, mass. Choosing a better integrator would remove none of it.
The cue sheet says this at slide 36 rather than leaving the impression that integration choice is
the dominant error source, because Week 5's closed loop is the thing that actually fixes it.

## Verification

Every command in the cue sheet was executed on this machine: ROS 2 Jazzy, Ubuntu 24.04.4,
Gazebo Harmonic. The outputs shown are from those runs.

- Euler error halves exactly with the timestep (`3.437e-01 → 1.723e-01 → … → 3.534e-03`); the arc
  integrator holds `1e-16` at every timestep.
- Commanding `linear.y` on turtlesim for two seconds leaves the pose identical to the last digit.
- `tf2_echo` between the wheel links returns `0.160`.
- The open-loop square closes to ~0.21 m on turtlesim (8 m perimeter) and ~0.02 m on TurtleBot 3
  (2 m perimeter). Consecutive turtle runs gave 0.209 m and 0.221 m; that spread is recorded in
  both the cue sheet and the transcript header so nobody marks a correct lab wrong.
- The cue sheet was rendered headless and checked visually; HTML structure validates with no
  unclosed tags and no broken anchors.

## Not done

- Screenshots specific to Week 4. The machine has no window manager tooling (`xdotool`,
  `wmctrl`), so a clean capture needs windows arranged by hand. `week04/README.md` still lists
  these as missing.
- Lecture B's checkpoint lab sheet and the starter (`TODO`-bearing) versions of the nodes. The
  `drive` node here is the worked answer to what Lecture B asks students to build, so it should
  stay out of their hands until they have written their own.
