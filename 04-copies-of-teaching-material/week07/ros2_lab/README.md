# Week 7 — Lecture B lab sheet

The deck (`../slides/EE414_W07B_tf2.pdf`) is the walkthrough. This sheet is the command
reference students keep open, plus the checkpoint list.

## Checkpoints

| # | After | Everyone must see | If not |
|---|---|---|---|
| 1 | `view_frames` | A `frames.pdf` containing `odom`, `base_link`, `base_scan` | Gazebo not running, or `tf2_tools`/Graphviz missing |
| 2 | Static publisher | `camera_link` in the tree and in `tf2_echo` | Flags misspelled — check `--frame-id` / `--child-frame-id` |
| 3 | Broadcaster node | `tool_link` at 0.3 m forward | `rotation.w` left at 0.0, or wall-clock stamp |
| 4 | `do_transform_point` | A fixed `base_scan` point **moving** in `odom` as the robot drives | Target/source swapped |
| 5 | The four errors | All four caused and read | See the error table below |

**Checkpoint 4 is the payoff of the week.** Ask the room what would happen to a map built in
`base_scan` before moving on.

## Commands

```bash
ros2 run tf2_tools view_frames                    # draw the tree to frames.pdf
ros2 run tf2_ros tf2_echo base_link base_scan     # one transform, live
ros2 topic info /tf --verbose                     # how many publishers?

ros2 run tf2_ros static_transform_publisher \
    --x 0.10 --y 0.0 --z 0.20 \
    --roll 0 --pitch 0 --yaw 0 \
    --frame-id base_link --child-frame-id camera_link
```

Use the **named flags**. The deprecated positional form orders its arguments differently and is
the source of many backwards-mounted sensors.

## The one line to memorise

```
lookup_transform(target, source, time)   ->   T_target,source
```

Takes data **from** `source` **to** `target`. Same as Lecture A's notation — the inner indices
cancel. The reversed call is perfectly valid and returns the inverse, with **no error**: your
obstacle just appears on the wrong side of the robot.

`rclpy.time.Time()` (time zero) means *the latest transform you have*.

## Two traps in broadcaster code

| Trap | Symptom |
|---|---|
| `transform.rotation.w` left at its default `0.0` | An all-zero quaternion is not a rotation. Every lookup through the link is garbage, and **nothing warns you**. Identity is `w = 1.0`. |
| `time.time()` instead of `self.get_clock().now()` | In simulation the clock is not wall time. The transform is stamped in a different era from every other message and lookups fail. |

Also: `header.frame_id` is the **parent**, `child_frame_id` is the **child**. Swapping them
builds an inside-out tree that still runs.

## The four errors — cause each one, read it, fix it

| Do this | Message | Cause |
|---|---|---|
| Look up immediately at start-up | `"base_scan" passed to lookupTransform does not exist` | Buffer is empty. You asked too early. **Not a bug.** |
| Ask for `now()` instead of `Time()` | `requires extrapolation into the future` | That instant has not arrived yet |
| Sleep 30 s, then ask for an old stamp | `requires extrapolation into the past` | The buffer discarded it; your node was too slow |
| Publish `odom` → `base_link` from a second node | **No error.** The robot twitches. | Two parents for one child — the dangerous one |

The first two are normal at start-up. Handle them:

```python
try:
    tf = self.buffer.lookup_transform('odom', 'base_scan', rclpy.time.Time())
except TransformException:
    return          # normal for the first second; try again next tick
```

**Never crash on a missing transform, and never retry in a loop inside the callback.** Return,
and let the next tick try again — Week 3's rule, still holding.

## RViz2

Add the **TF** display. Set the fixed frame to `odom`, drive with teleop, then set it to
`base_link` and drive again. Same data, different question — and the fastest way both to
understand frames and to spot a sensor mounted backwards.

## To be produced

| Item | Status |
|---|---|
| `code/src/ee414_w07_tf2_frames/` — broadcaster and listener starters | ❌ |
| `expected_output.txt` from a real run on the pinned distribution | ❌ |
| Saved RViz2 config with the TF display added | ❌ |
| A prepared double-publisher launch file, for error 4 | ❌ |
