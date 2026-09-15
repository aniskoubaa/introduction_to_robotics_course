# Week 4 — a hands-on lab sheet, and one package instead of two

2026-09-15 02:52 UTC · ROS 2 Jazzy · Ubuntu 24.04.4 LTS · Python 3.12

Two pieces of work, done together because the second one made the first one
possible to describe without a footnote on every line.

---

## 1. The unification, finished

The 13 September entry left the package merged and building, and every
reference to it outside the package still pointing at the old name. That is
now swept.

| File | What changed |
|---|---|
| `shared/screenshots/snippets.py` | `W04` pointed at `code/src/ee414_w04_demo`, `CRS` at `/home/alfaisalx/ros2_ws/src/ee414_course` — an absolute path into a directory that no longer holds the package. Both are now one constant, `PKG`. The two names survive only because the snippet table reads better with them. |
| `shared/screenshots/verify_w04_commands.sh` | Swept, and one row removed: the sweep had turned two different builds into the same build twice. |
| `shared/screenshots/make_expected_output_w04.sh`, `insert.py` | Swept. |
| `shared/screenshots/rosenv.sh` | **Order reversed.** `~/ros2_ws` is now sourced *before* the repository's `code/` workspace, so if a stale `ee414_course` ever reappears in the personal workspace, the repository's copy is the one that wins. It was the other way round, which is how the two copies drifted in the first place. |
| `week04/ros2_lab/EE414_W04_demo_cue_sheet.html` | Swept, and three pieces of prose rewritten: the masthead said `ee414_course + ee414_course`, the setup part built the same package twice from two directories, and a "Two packages" note explained a distinction that no longer exists. |
| `week04/README.md`, `week04/ros2_lab/README.md`, `shared/screenshots/README.md`, `code/README.md` | Rewritten where they described the two-package arrangement. `code/README.md`'s workspace tree listed nine packages that were never created; it now lists the three that exist and says that planned per-week packages are folders inside `ee414_course`. |

The one remaining occurrence of `ee414_w04_demo` outside `docs/` is a comment
in `setup.py` recording what the entry points used to belong to. That is
deliberate.

**Generated artifacts regenerated:** `week04/ros2_lab/command_check.txt` and
`week04/ros2_lab/expected_output.txt`, both from real runs against the merged
package.

---

## 2. `EE414_W04_hands_on_lab.html`

The students' half of Week 4. The cue sheet demonstrates a package that
already works; the lab sheet takes somebody who has never created a ROS 2
package from an empty directory to a robot driving a circle whose radius they
predicted before they ran anything.

Six parts, each ending in a checkpoint that must be ticked before going on:

1. **Download and build** — `mkdir src`, `git clone --depth 1`,
   `colcon build --packages-select`.
2. **Run and observe** — `cleaner` (the 2023 `clean.py`) and `mover`
   (`simple_turtlesim_motion.py`). Nothing is typed. Open loop and closed loop
   are met in the same menu, thirty seconds apart.
3. **How it moves** — topic, `Twist`, control loop. Three ideas, then a
   prediction: `R = v / ω = 2.0`.
4. **Create a package** — `ros2 pkg create`, and what each generated file is
   for. Build it while it is still empty, so a later failure has one possible
   cause instead of two.
5. **Write the node** — thirty lines of Python, then the measurement against
   the prediction.
6. **The same in C++** — optional, twenty minutes.

Plus a troubleshooting table of fourteen messages, every one of them produced
on purpose on this machine.

### What the repository actually contains

Worth recording, because it is not what the repository's own structure
suggests:

- **`ros2_motion_cpp` has no source files.** It is an `ament_cmake` skeleton
  with `rclcpp` and `geometry_msgs` declared and nothing to compile. It builds
  and ships **zero** executables. There is no C++ turtlesim motion code in
  `ros2_course_packages`, and the C++ that is there — `ros2_essential_cpp` —
  is talker/listener/client/server and does not build without
  `ros2_interfaces_cpp` beside it.
- Part 6 therefore *fills* that skeleton rather than running something from
  it. Thirty-three lines of `rclcpp` and seven lines of CMake, and the empty
  package becomes the C++ twin of the student's Python one. The package being
  empty turns out to be the better lesson: it is the only place in the lab
  where the student sees what `add_executable` and `install(TARGETS ...)` are
  actually for, and that omitting the second gives a build that succeeds and a
  `ros2 run` that finds nothing.

### Two faults in the 2023 code, taught rather than hidden

Both were reproduced deliberately, and both are asserted by the checker, so a
future release that repairs them will fail the run and force the sheet to be
updated.

1. **Any rotation above 180 degrees in `cleaner` never terminates.** Progress
   is measured as `abs(start.theta - current.theta)`; `theta` wraps at `±π`,
   so the measured angle rises to 180 and then falls again. A request for 200
   waits for a number that cannot occur. Measured: `rotate(200°)` still
   spinning at the 150-second cap. `rotate(90°)` finishes correctly at
   `90.0000025°`, which is why the fault survived two years of teaching.
2. **`mover` ends in `RCLError: Failed to publish: publisher's context is
   invalid`.** It calls `rclpy.shutdown()` inside its timer callback and then
   publishes one more message on the next line. The turtle does stop
   correctly; the error arrives one instruction later.

   A second, quieter fault in the same file: its constructor calls
   `create_client(Empty, 'reset')` and `call_async` without waiting for the
   service, then `spin_until_future_complete`. The future never completes.
   `Turtlesim Reset` is never printed and `__init__` never returns — the
   traceback at t = 75 s is still inside the constructor. The node works only
   because the timer callbacks run inside that spin.

### The node the students write

Thirty lines, no comments, no argparse.

```python
def main():
    rclpy.init(signal_handler_options=SignalHandlerOptions.NO)
    node = Circle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.pub.publish(Twist())
        time.sleep(0.3)
    rclpy.shutdown()
```

`SignalHandlerOptions.NO` is in a beginner's first node on purpose. Without
it, `Ctrl-C` shuts the context down before the `except` block can publish, and
the student's first experience of stopping their own robot is the same
`publisher's context is invalid` they were shown in Part 2. The sheet makes
that connection explicit.

`time.sleep(0.3)` gives the stop message time to leave the process before
`rclpy.shutdown()` tears the publisher down. It is defensive rather than
demonstrated: turtlesim's own one-second command timeout stops the turtle
either way here, so the simulator cannot show the difference. It is in the file
because the same node on a TurtleBot 3 would need it, and because the sheet
asks students to form the habit. (An earlier draft of this entry claimed three
interrupted runs without it left the turtle moving. That measurement came from
the broken harness described in section 4 and has been removed.)

### The measurement

`linear.x = 2.0`, `angular.z = 1.0`, so `R = v / ω = 2.0`. Sampled from
`/turtle1/pose` over one revolution:

```
x range 3.528 .. 7.528   span 4.000
y range 5.544 .. 9.544   span 4.000
radius 2.000 by 2.000
```

The C++ node gives the same figure. This is the single best thirty seconds in
the sheet: a number predicted from the lecture, and the robot agreeing to
three decimal places.

### One honest caveat, written into the sheet

**turtlesim zeroes the turtle's velocity about one second after the last
command.** Verified by `SIGKILL`-ing a publishing node: velocity was `0.0` at
the first sample 0.3 s later. So the explicit stop message is not what stops
the turtle here — the simulator is. A TurtleBot 3 holds its last velocity,
which is exactly why the habit is worth forming in a simulator where a mistake
costs nothing. The sheet says so rather than letting the student infer a
guarantee that does not exist.

---

## 3. `verify_w04_handson.sh`

Same promise as the other harnesses: every line in the sheet was executed.
This one is the student. It clones into a scratch workspace, builds, runs the
2023 demonstrations, creates `my_turtle_circle` with `ros2 pkg create`,
installs the two files from `week04/ros2_lab/handson/`, builds again, and
**measures the radius of the circle the finished node draws**.

`week04/ros2_lab/handson_check.txt`: **24 passed, 0 failed**, including the
two rows that assert the 2023 faults are still present.

One small thing worth not repeating: **`ros2 pkg create` takes the package name
before `--dependencies`.** With the name last, `nargs='+'` swallows it and the
command fails with `the following arguments are required: package_name`. It is
in the sheet as a warning because a student will hit it.

---

## 4. `set -m` had silently disabled every interrupt check

Writing the new harness turned up the same addressing bug three times, and then
it turned out to be in the two existing harnesses as well. It had been there
since 13 September, and it had been *introduced* by that day's fix.

```
setsid bash -c '...' &
pgid=$!
kill -INT -"$pgid"
```

`setsid(1)` calls `setsid(2)` directly only when the caller is not already a
process group leader. When it is one, **setsid forks and the parent exits**, so
`$!` names a process that is already dead and `kill -INT -$!` signals a group
that no longer exists. Whether the caller is a group leader depends entirely on
job control:

| | background job is | setsid | `$!` |
|---|---|---|---|
| `set +m` (default in a script) | in the shell's own group | does not fork | correct |
| `set -m` | its own group leader | forks | useless |

Both harnesses were written under `set +m` and worked. `set -m` was added to
both on 13 September — correctly, because without it bash gives background jobs
`SIGINT = SIG_IGN` and the interrupt cannot be delivered at all — and that fix
silently broke the addressing. Afterwards:

- nothing was signalled;
- `wait` on the exited parent returned 0;
- the log was empty, so the traceback count was 0;
- **every interrupt row reported PASS**, and the nodes kept running.

It was caught only because `assert_clean_graph.sh` refused to start
`make_expected_output_w04.sh`, naming two `ros2 topic pub` processes leaked by
a "successful" run of `verify_w04_commands.sh` minutes earlier.

### What changed

`shared/screenshots/procgroup.sh` is new: `spawn_pg`, `sigint_pg`, `kill_pg`.
The group id is written down by the child and never inferred from `$!`. All
three harnesses source it. `check_interrupt` additionally now **fails** a row
whose command had already exited before the interrupt was due, instead of
reporting `[Ctrl-C] PASS` about a process that was never interrupted.

`shared/screenshots/kill_sims.sh` is also new, and it is a separate file for a
reason that is not tidiness. `ps | grep turtlesim | xargs kill -9` and `pkill -f
turtlesim` both match the shell running them, because that shell's own command
line contains the word; the shell dies mid-script and the caller sees a bare
non-zero exit with no output. That has now happened five times in this project,
in five different one-liners, and the `[t]urtlesim` trick does not help — it
protects the `grep`, not the `bash -c '...'` above it whose argument holds the
whole script text. A file called `kill_sims.sh` cannot have the pattern in its
command line.

### A retraction

The 13 September entry recorded a limitation in the beginner scripts: that
`simple_square` and `simple_go_to_goal`, interrupted mid-motion, left the turtle
coasting, measured 3 of 3 and 2 of 3 times.

**That limitation does not exist.** It was the broken harness measuring itself.
The scripts were never interrupted, so they were still driving when the pose was
read. With the addressing fixed, `beginner_check.txt` is **8 of 8**, including
the assertion that the turtle is stopped after every interrupt. The
`finally: stop(pub)` block in each script does exactly what it says.

Withdrawn in `beginner_student_freindly/README.md`, in
`week04/ros2_lab/README.md`, and by a note at the head of the 13 September
entry's section, which is otherwise left as written.

---

## Files

| Path | Status |
|---|---|
| `week04/ros2_lab/EE414_W04_hands_on_lab.html` | new · 6 parts · 1713 lines |
| `week04/ros2_lab/handson/my_turtle_circle/circle.py` | new · 30 lines |
| `week04/ros2_lab/handson/ros2_motion_cpp/circle.cpp` | new · 33 lines |
| `week04/ros2_lab/handson/ros2_motion_cpp/CMakeLists.fragment.txt` | new · 7 lines |
| `week04/ros2_lab/handson/README.md` | new |
| `week04/ros2_lab/handson_check.txt` | new · 24/24 |
| `shared/screenshots/verify_w04_handson.sh` | new |
| `shared/screenshots/snippets.py`, `insert.py`, `rosenv.sh`, `verify_w04_commands.sh`, `make_expected_output_w04.sh` | unified |
| `week04/ros2_lab/EE414_W04_demo_cue_sheet.html` | unified · three passages rewritten |
| `week04/README.md`, `week04/ros2_lab/README.md`, `shared/screenshots/README.md`, `code/README.md` | rewritten where they described two packages |

The lab sheet's HTML is checked against the reference files in `handson/`:
strip the `<b>` emphasis from the two code cards and the text is byte-identical
to the files on disk. The handout cannot drift from the code it asks for.

## Still open

- The `<gui>` block in `worlds/diff_drive_demo.sdf` — about 220 lines of
  Gazebo's stock `gui.config`, keep or revert. Unanswered since 12 September.
- A **starter** package with one `TODO` per concept. The lab sheet gives the
  finished thirty lines, which is right for a first package and wrong for the
  second.
- ROS 2 Jazzy screenshots specific to this week. Both Week 4 HTML documents are
  deliberately image-free and self-contained, so this is a slides problem, not
  a handout one.
