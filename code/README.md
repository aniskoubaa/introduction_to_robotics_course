# Code — the course ROS 2 workspace

A single colcon workspace. One package per week, each a runnable starting point for that
week's practice hour and the assignment that follows it.

```
code/
├── src/
│   ├── ee414_w02_first_node/          Week 02 — rclpy nodes, CLI, launch
│   ├── ee414_w03_interfaces/          Week 03 — .msg and .srv definitions (ament_cmake)
│   ├── ee414_w03_nodes/               Week 03 — nodes that use them (ament_python)
│   ├── ee414_w04_demo/                Week 04 — Lecture A demos: kinematics, quaternions,
│   │                                             integration, minimal URDF + Gazebo world
│   ├── ee414_w04_open_loop_motion/    Week 04 — /cmd_vel, /odom, motion primitives
│   ├── ee414_w05_go_to_goal/          Week 05 — P/PID controller, waypoints
│   ├── ee414_w06_obstacle_avoidance/  Week 06 — /scan processing, reactive avoidance
│   ├── ee414_w07_tf2_frames/          Week 07 — broadcasters, listeners, static transforms
│   ├── ee414_w08_robot_description/   Week 08 — URDF/Xacro, Gazebo spawn, RViz2 config
│   ├── ee414_w09_state_estimation/    Week 09 — EKF fusion, rosbag2 replay
│   ├── ee414_w10_slam_localization/   Week 10 — slam_toolbox + AMCL configs and maps
│   ├── ee414_w11_navigation/          Week 11 — Nav2 params, behaviour tree, waypoints
│   └── ee414_common/                  shared helpers, launch fragments, Gazebo worlds
└── README.md
```

## Build

```bash
cd code
colcon build --symlink-install
source install/setup.bash
```

`build/`, `install/` and `log/` are generated — excluded by `.gitignore`, never committed.

### If `colcon build` says `No module named 'em'`

The student has Anaconda on their machine. CMake's `FindPython3` honours `CONDA_PREFIX` and
picks the Anaconda interpreter, which has no `empy` — so interface generation fails even though
the system `python3` has it installed. Two fixes, either is fine:

```bash
conda deactivate                     # for the session
unset CONDA_PREFIX                   # if deactivate is not enough
```

This bites in Week 3, the first week with an `ament_cmake` interfaces package, and never
before. Worth saying out loud at the start of W03B rather than debugging it six times.

### If a node publishes and the robot does not move

Check the message type before anything else:

```bash
ros2 topic type /cmd_vel
```

On Jazzy the TurtleBot 3 Gazebo bridge carries `geometry_msgs/msg/TwistStamped`, not the `Twist`
that every older tutorial shows. A publisher of the wrong type is **not an error**: the types do
not match, so no connection is made, the publisher reports success, and the robot sits still with
nothing printed anywhere. `ee414_w04_demo/twist_compat.py` resolves the type from the graph at
start-up and is the pattern to copy.

> **Week 3 is two packages, not one.** Interface generation is a CMake job, so the `.msg` and
> `.srv` files need an `ament_cmake` package of their own; the nodes that import them stay
> `ament_python`. That split is the week's tooling lesson, so the workspace has to show it.

## Package conventions

- **Python (`rclpy`) only.** C++ is mentioned in lecture as what production uses; nothing in
  this course is assessed in it. A fourth-year EE cohort has limited C++ time to spare, and
  the concepts are the point.
- Every package builds clean on the pinned distribution before it is pushed. A package that
  does not build is worse than a missing one — it costs a student their practice hour.
- Every node has a **starter** version (structure present, one `TODO` per concept) and a
  **solution** version. Solutions live in the instructor archive, not here.
- One launch file per package that brings up the full week's demo in one command.

### Ctrl-C must stop the robot, not print a traceback

`rclpy.init()` installs a SIGINT handler that shuts the context down the moment `Ctrl-C` is
pressed. Everything after it fails:

```
rclpy._rclpy_pybind11.RCLError: Failed to publish: publisher's context is invalid
[ros2run]: Process exited with failure 1
```

The traceback is the visible half of the problem. The half that matters is that the node's
`stop()` never reaches the robot, and a differential drive holds the last velocity it was given
— so `Ctrl-C` on a driving robot leaves it driving.

`ee414_w04_demo/graceful.py` is the fix and the pattern to copy: ask `rclpy.init` for no signal
handler, install one that sets a flag, and let the hold loops notice it. The context stays
valid, so the usual `stop()` on the way out is delivered, the summary still prints, and the
process exits 0.

```python
from ee414_w04_demo import graceful

graceful.init(args)                      # instead of rclpy.init(args=args)
while not graceful.interrupted():        # in every loop that holds a velocity
    ...
```

## Standing rule

**Nothing enters this workspace that has not been run.** The expected-output transcript in
the matching `04-copies-of-teaching-material/weekNN/ros2_lab/` is generated from an actual
run, not written by hand. From Week 4 there is a second transcript, `command_check.txt`: every
command in that week's cue sheet, run in lecture order, with `Ctrl-C` sent to the long-running
ones and a clean exit required.
