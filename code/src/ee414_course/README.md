# ee414_course

Simple, runnable scripts for **EE 414 — Introduction to Robotics**. Week 4:
differential-drive kinematics.

Built on the teaching scripts in
[ros2_course_packages](https://github.com/aniskoubaa/ros2_course_packages) —
same style, same class-per-node shape, with the bugs fixed and the Week 4
material added. See [What changed](#what-changed-from-ros2_course_packages).

## Build

```bash
cd ~/ros2_ws
colcon build --packages-select ee414_course
source install/setup.bash
```

## The scripts

Run them in this order. The first two need **no simulator at all** — the model
is arithmetic, and it is worth seeing it as arithmetic first.

| # | Command | Simulator? | Slide | What it shows |
|---|---|---|---|---|
| 1 | `ros2 run ee414_course kinematics` | no | 20–23 | Forward and inverse kinematics. Four wheel-speed cases, four path shapes. Stop one wheel and the turn radius is exactly `L/2`. |
| 2 | `ros2 run ee414_course angle_wrap` | no | 13 | Why you must never subtract two headings. **Watches the original `rotate()` bug happen.** |
| 3 | `ros2 run ee414_course pose_monitor` | yes | 9, 12 | `theta` as a float from turtlesim, a quaternion from `/odom`, side by side. |
| 4 | `ros2 run ee414_course nonholonomic` | yes | 17 | Commands all six Twist fields. Four do nothing, identically, with no error. |
| 5 | `ros2 run ee414_course turtle_mover` | yes | 29–31 | Open loop at its simplest, with the estimate printed against the truth. |
| 6 | `ros2 run ee414_course move_rotate` | yes | 20, 35 | `move()` and `rotate()`, and the square that does not close. |
| 7 | `ros2 run ee414_course go_to_goal` | yes | 38 | Closed loop, for contrast. It arrives every time. |
| 8 | `ros2 launch ee414_course view_model.launch.py` | — | 25–26 | The minimal URDF in RViz2, with sliders for the wheels. |

Every motion script takes `--robot turtle` (default) or `--robot tb3` and runs
on either without being edited.

```bash
# turtlesim
ros2 run turtlesim turtlesim_node
ros2 run ee414_course move_rotate --shape square --distance 2.0

# TurtleBot 3 — same script, slower and smaller because a Burger tops out at 0.22 m/s
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo empty_world.launch.py
ros2 run ee414_course move_rotate --robot tb3 --shape square \
    --distance 0.5 --speed 0.15 --turn-rate 0.5
```

## The three demonstrations worth the time

**`angle_wrap`** prints the original `rotate()` bug as it happens:

```
 time    heading      buggy measure      correct measure
 0.2s     +176.0          6.0 deg           6.0 deg
 0.4s     -178.0        348.0 deg          12.0 deg   <-- buggy stops here
 ...
 1.4s     -148.0        318.0 deg          42.0 deg   <-- correct stops here
```

A `rotate(40°)` built on the buggy measure stops after **12 degrees**.

**`nonholonomic`** commands sideways motion and reads the pose before and after:

```
  before : x=5.544445  y=5.544445  theta=0.000000
  after  : x=5.544445  y=5.544445  theta=0.000000
  result : NOTHING MOVED. Not approximately -- identically.
```

**`move_rotate --shape square`** shows the wrap bug turning up on its own, on
whichever side crosses the ±π seam:

```
  rotate +90.0 deg at 1.000 rad/s -> hold for 1.571 s
         turned 89.8 deg (the naive subtraction would say 270.2 deg)
```

## What changed from ros2_course_packages

The teaching shape is deliberately unchanged. These are corrections.

**1. The rotation measurement was wrong at the seam.** `clean.py` had:

```python
rotated_related_angle_degree = math.degrees(abs(start_pose.theta - self.pose.theta))
```

Pose topics report `theta` already wrapped into (−π, π]. Cross that seam and
this expression jumps from nearly 0 to nearly 360, so `rotate()` stops far too
early. Now `abs(normalize_angle(now - start))`, in `robot_pose.py`.

**2. `go_to_goal()` had the same bug in its heading error.**

```python
angular_speed = (desired_angle_goal - self.pose.get_theta()) * p_gain_angular
```

With the goal behind the robot this exceeds π and the robot turns the long way
round. Now wrapped, clamped to the robot's real limits, and it turns to face
the goal before driving at it.

**3. `rclpy.shutdown()` was called from inside a timer callback** in
`simple_turtlesim_motion.py`, and the callback then published again. Now the
timer is cancelled and the node exits cleanly.

**4. The speed guards did not match their messages.** `if angular_speed_degree > 30`
printed *"must be lower than 0.5"*. Limits are now per robot, in one place, and
the message names the number being enforced.

**5. `/cmd_vel` type detection.** On ROS 2 Jazzy the TurtleBot 3 Gazebo bridge
carries `geometry_msgs/msg/TwistStamped`, not `Twist`. Publishing the wrong one
produces **no error at all** — the types do not match, so nothing connects, and
the robot sits still. `robot_io.py` asks the graph and sends the right one,
which is why every script here runs on both robots unchanged.

**6. `RobotPose` grew the arithmetic every script was re-implementing** —
`distance_to`, `angle_to`, `heading_error_to`, `angle_turned_since` — so the
angle handling is correct in one place instead of wrong in several.

**7. `Ctrl-C` left the robot driving.** `rclpy.init()` installs a SIGINT handler
that shuts the context down at once, so the node's own `stop()` then raises

```
rclpy._rclpy_pybind11.RCLError: Failed to publish: publisher's context is invalid
```

The traceback is the visible half. The half that matters is that the zero
`Twist` was never sent, and a differential drive holds the last velocity it was
given — so interrupting a driving robot left it driving. `graceful.py` asks
rclpy for no signal handler and installs one that only sets a flag; the hold
loops check it, the context stays valid, `stop()` is delivered, the summary
still prints, and the process exits 0.

```python
from ee414_course import graceful

graceful.init(args)                   # instead of rclpy.init(args=args)
while not graceful.interrupted():     # in every loop that holds a velocity
    ...
```

**8. Interrupted runs told the truth.** `go_to_goal` used to report "Gave up
after 60 s" when it had been stopped after three, and `nonholonomic` printed its
whole conclusion after testing two fields of six. Both now say they were
interrupted.

**9. `turtle_mover` measured from the wrong starting point.** It read the pose
after calling `/reset` but before the reset pose had arrived, so the error was
measured from wherever the turtle had been *before* being teleported to the
middle: a 5 m drive accurate to 1.1% was reported as **90.4% wrong**. It now
discards the stale pose and waits for a fresh one.

## Layout

```
ee414_course/
├── ee414_course/
│   ├── robot_pose.py     RobotPose + normalize_angle + quaternion helpers
│   ├── graceful.py       Ctrl-C that stops the robot instead of a traceback
│   ├── robot_io.py       RobotDriver: one API for turtlesim and TurtleBot 3
│   ├── kinematics.py     forward/inverse/ICC, no ROS
│   ├── angle_wrap.py     the wrap bug, demonstrated, no ROS
│   ├── pose_monitor.py   theta vs quaternion, live
│   ├── nonholonomic.py   the four fields that do nothing
│   ├── turtle_mover.py   simplest open-loop node
│   ├── move_rotate.py    move() / rotate() / square / arc
│   └── go_to_goal.py     closed loop, for contrast
├── urdf/burger_min.urdf  r and L, written down as a robot
├── launch/view_model.launch.py
└── rviz/model.rviz
```

## Licence

Derived from `ros2_course_packages`, © 2023 Anis Koubaa, CC BY-NC-SA 4.0.
This package keeps that licence.
