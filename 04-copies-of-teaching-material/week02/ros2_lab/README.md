# Week 2 — Lecture B lab checklist

The instructor deck (`../slides/EE414_W02B_first_nodes.pdf`) is the walkthrough. This is the
one-page version students keep open beside it, and the checkpoint list the instructor runs the
room against.

## Checkpoints

| # | After | Everyone must see | If not |
|---|---|---|---|
| 0 | Environment check | `ROS_DISTRO` set, **your** `ROS_DOMAIN_ID`, `ros2 topic list` works | Source the underlay. If still empty, the install failed — pair up now, fix after class |
| 1 | First run | `talker` printing `hello 0, 1, 2…` | See the failure table below |
| 2 | Inspection | `ros2 topic echo`, `hz` and `info` all producing output | Wrong terminal not sourced |
| 3 | Both nodes | `listener` printing `got: hello …`, and `rqt_graph` showing talker → /chatter → listener | Topic name, domain ID, or QoS |
| 4 | Launch | `ros2 launch` starting both, `Ctrl-C` stopping both | The `launch/` folder was not installed — check `setup.py` |

**Do not advance past a checkpoint until the room is with you.** A student stuck at
checkpoint 1 gets nothing from the remaining fifty minutes and will not say so unprompted.

## Sequence

1. Environment check — `printenv ROS_DISTRO`, `printenv ROS_DOMAIN_ID`, `ros2 topic list`
2. `mkdir -p ~/ee414_ws/src` · `colcon build` · `source install/setup.bash`
3. `ros2 pkg create --build-type ament_python --dependencies rclpy std_msgs ee414_w02_first_node`
4. Write `talker.py` — publisher, timer, `main`
5. Add the entry point in `setup.py`
6. `colcon build --symlink-install` · source · `ros2 run … talker`  → **Checkpoint 1**
7. Second terminal: `node list`, `topic list`, `topic echo`, `topic hz`, `topic info --verbose`, `topic pub` → **Checkpoint 2**
8. Write `listener.py`, add its entry point, rebuild, run in a third terminal → **Checkpoint 3**
9. `rqt_graph`
10. Kill the talker. Watch the listener survive.
11. Write `launch/chatter_launch.py`, install the folder, `ros2 launch` → **Checkpoint 4**
12. The five deliberate failures

## The five deliberate failures

Cause each one, read the symptom **before** giving the cause, then fix it.

| Do this | Symptom | The lesson |
|---|---|---|
| New terminal, do not source | `Package not found` | Sourcing is per shell, and does not persist |
| Misspell the entry point | `No executable found` | The entry point is a mapping, not magic |
| Change the listener's `ROS_DOMAIN_ID` | Both run. Silence. | Discovery is partitioned |
| Rename the topic in one node only | Both run. Silence. | The topic name is the whole contract |
| Listener `BEST_EFFORT`, publisher `RELIABLE` | Both run. Silence. | QoS must be compatible |

**Three of the five look identical from outside: two healthy nodes, no data.** That is the point
of the exercise.

## The diagnostic order

```
ros2 node list                       # are both alive?
ros2 topic list                      # does the topic exist?
ros2 topic info /chatter --verbose   # counts, types, QoS profiles
printenv ROS_DOMAIN_ID               # ... in BOTH terminals
```

| What you see | What it means |
|---|---|
| Publisher count 1, subscriber 0 | The subscriber is on another topic or another domain |
| Both counts 1, no data | QoS mismatch — read the two profiles |
| Topic missing entirely | The publisher is not running, or its terminal is not sourced |

Same four commands in Week 11, on a robot with forty topics. Learn the order now.

## To be produced

| Item | Status |
|---|---|
| `code/src/ee414_w02_first_node/` starter package (structure present, one `TODO` per concept) | ❌ |
| `expected_output.txt` — transcript from a real run on the pinned distribution | ❌ |
| Fallback for failed installs: prepared Docker image, or a pairing plan | ❌ |
