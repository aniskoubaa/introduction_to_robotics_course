# Setup — do this before Week 2

Every practice hour and every assignment assumes a working ROS 2 installation. Budget
**60–90 minutes**. Do not arrive in Week 2 without it.

## Pinned distribution

> **ROS 2 Jazzy Jalisco** on **Ubuntu 24.04 LTS**.
> Gazebo **Harmonic**. Python **3.12**.

⚠️ This is the **only** place in the course where the distribution is named. Every other
document refers here. When the course upgrades, change these three lines and nothing else.

## Pick a route

| Route | For | Effort | Recommended |
|---|---|---|---|
| **A — Native Ubuntu 24.04** | Anyone with a spare machine or a dual boot | Medium | ✅ Best performance, fewest surprises |
| **B — WSL2 on Windows 11** | Most students | Low | ✅ Works, including GUI apps (RViz2, Gazebo) via WSLg |
| **C — Docker + VNC** | macOS, especially Apple Silicon | Medium | Acceptable; Gazebo is slower |
| **D — University lab machines** | Fallback | None | Pre-imaged; no personal state persists |

Apple Silicon users: route C. Gazebo runs but expect reduced frame rates — this affects
comfort, not correctness, and every assignment is sized to run on it.

## To be authored

| Item | Status |
|---|---|
| Step-by-step guide per route, with screenshots | ❌ |
| `check_ros2_setup.py` — verifies distribution, `rclpy`, TF2, Gazebo, TurtleBot3 packages, and prints a pass/fail table | ❌ |
| Common-failure list: sourcing, `ROS_DOMAIN_ID` collisions in a shared lab, WSLg GUI issues, Gazebo GPU fallback | ❌ |
| Recorded 15-minute walkthrough on the LMS | ❌ |

## Verify

```bash
python3 check_ros2_setup.py     # must print PASS on every row
ros2 run demo_nodes_cpp talker  # in one terminal
ros2 run demo_nodes_py listener # in another — you should see the messages
```

## Shared-lab note

Every student on the same network segment sees every other student's nodes unless
`ROS_DOMAIN_ID` differs. Assign each student a domain ID in Week 1 and have them put it in
`~/.bashrc`. Skipping this produces a room in which everyone's robot is driven by everyone.
