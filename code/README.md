# Code — the course ROS 2 workspace

A single colcon workspace. One package per week, each a runnable starting point for that
week's practice hour and the assignment that follows it.

```
code/
├── src/
│   ├── ee414_w02_first_node/          Week 02 — rclpy nodes, CLI, launch
│   ├── ee414_w03_interfaces/          Week 03 — .msg and .srv definitions (ament_cmake)
│   ├── ee414_w03_nodes/               Week 03 — nodes that use them (ament_python)
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

## Standing rule

**Nothing enters this workspace that has not been run.** The expected-output transcript in
the matching `04-copies-of-teaching-material/weekNN/ros2_lab/` is generated from an actual
run, not written by hand.
