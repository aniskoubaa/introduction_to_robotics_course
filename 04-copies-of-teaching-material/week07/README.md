# Week 7 — Rigid-Body Transformations and TF2

| | |
|---|---|
| **Lecture A (1.5 h)** | Why frames exist; rotation matrices; homogeneous transforms; composition and the index-cancelling notation; trees; 3D and quaternions; transforms in time |
| **Lecture B (1.5 h)** | Hands-on TF2: reading an existing tree, publishing static and dynamic frames, `lookup_transform`, transforming data, and the four TF errors |
| **CLO served** | CLO 2 (A) · CLO 3 (B) |
| **Assessment this week** | **Quiz 3** (in A) |
| **Tooling rung** | T4 — first use of `tf2_tools`, `tf2_ros` CLI and the RViz2 TF display |
| **Reading** | Lynch & Park Ch. 3 (rigid-body motions); ROS 2 docs: TF2 tutorials, "tf2 and time" |

## Status

| Artifact | Path | Status |
|---|---|---|
| Lecture A deck | `slides/EE414_W07A_transformations.tex` / `.pdf` | ✅ 21 slides, builds clean |
| Lecture B deck | `slides/EE414_W07B_tf2.tex` / `.pdf` | ✅ 21 slides, builds clean |
| Lab sheet | `ros2_lab/README.md` | ✅ |
| Starter package | `../../code/src/ee414_w07_tf2_frames/` | ❌ **not authored** |
| Expected-output transcript | `ros2_lab/expected_output.txt` | ❌ — standing rule 2 |
| Quiz 3 + key | `../../07-exams-answer-keys-or-assessment-rubrics/` | ❌ |

> ⚠️ **Authored out of order.** Weeks 4–6 are still briefs. These decks refer backwards to
> Week 4 (kinematics), Week 6 (LiDAR, obstacle avoidance) and Week 2 (`Header`, stamps), and
> forwards to Weeks 8, 10 and 11. Check those references when 4–6 are written.

## Lectures

| File | Duration | Contents |
|---|---|---|
| `slides/EE414_W07A_transformations.tex` | 1.5 h · 21 slides | A number with no frame is not information; the four frames of a mobile robot; the two questions (expression and composition); 2D rotation matrix and its three properties; rotating a point vs re-expressing in a rotated frame; why `Rp + t` is abandoned; homogeneous coordinates; **the index-cancelling notation as a type check**; a worked 10 cm example; why frames form a tree; 3D and why ROS stores quaternions; transforms are only valid at an instant; the two extrapolation errors |
| `slides/EE414_W07B_tf2.tex` | 1.5 h · 21 slides | `view_frames` on a live robot; `tf2_echo` on a static and a dynamic link; who publishes what and why localization inserts a frame; `static_transform_publisher` with named flags; `TransformBroadcaster` from a node; the `w = 0.0` and wall-clock traps; `Buffer` and `TransformListener`; **the `lookup_transform(target, source, time)` argument order**; `do_transform_point`; why that checkpoint is the whole week; the four TF errors caused deliberately; handling the benign two; finding a double publisher; the RViz2 TF display and changing the fixed frame |

Build: `pdflatex <file>.tex` twice. `logo.png` must sit beside the `.tex`.

**Known cosmetic issue:** W07B reports one 1.9 pt overfull `\vbox` (0.7 mm) on the
`static_transform_publisher` frame. Below the visual threshold; left alone.

## Teaching notes

**This is the highest-leverage week in the course, and it does not look like it.** Nothing
visible happens: no robot drives, no map appears. What happens is that Weeks 10 and 11 become
possible. Say this out loud in the first two minutes, because a student who thinks this is a
maths detour will disengage, and then be lost for the rest of the semester.

**W07A, open with the unanswerable question.** "The LiDAR reports 2.1 m at 30°. Where is the
obstacle?" Take answers. Let them discover the question is not answerable. The definition of a
frame then arrives as the resolution of something they felt, not as a definition.

**W07A, rotating a point vs re-expressing in a rotated frame.** This is *the* conceptual
hazard of the week — same matrix, opposite direction, differing by a transpose. Spend real time
here. Use a physical demonstration: hold an object still and turn yourself; then stand still and
move the object. Students who never separate these two will apply transforms backwards for the
rest of the course and blame their controller.

**W07A, the index-cancelling notation.** Sell it as a *type check*, not as tidiness.
`T_AB T_CD` has correct dimensions, compiles, runs, and is nonsense — and the subscripts are the
only thing that catches it. Insist on the notation in Quiz 3 and in the exam; it costs nothing
to adopt and it prevents a whole class of error.

**W07A, the 10 cm worked example.** Do not let this feel trivial. Ten centimetres is exactly
the difference between passing through a gap and scraping it in Week 11. The point of the
example is that frame errors are *small numbers that matter*, not dramatic failures.

**W07A, time.** Tie it explicitly back to Week 1's "nothing is instantaneous" and Week 2's
`Header`. This is the third time those two ideas appear, and this is where they pay off. The
two extrapolation messages should be read aloud — they will see them within the hour.

**W07B, do not let anyone multiply a matrix.** State at the start that TF2 does the algebra.
The session is about publishing the right links and asking the right question. Students who
try to hand-roll the arithmetic in `do_transform_point` will get sign errors, and the lesson
they take away will be the wrong one.

**W07B, the `w = 0.0` trap.** Have every student try it deliberately — thirty seconds — and look
at what `tf2_echo` reports. An all-zero quaternion is not a rotation, nothing warns you, and
every lookup through that link is silently garbage. This costs a full day the first time it
happens in a project.

**W07B, the argument order.** `lookup_transform(target, source, time)`. Write it on the board and
leave it there. The reversed call is *perfectly valid* — it returns the inverse, with no error —
so the only symptom is an obstacle on the wrong side of the robot. Connect it explicitly to the
promise made in Lecture A: "almost every *turned the wrong way* bug is a frame bug."

**W07B, checkpoint 4 is the payoff.** Drive the robot and watch a point that is fixed in
`base_scan` move in `odom`. That single observation is why mapping needs a frame that is not the
sensor's. Do not rush past it — ask the room what would happen to a map built in `base_scan`.

**W07B, the fourth TF error.** Two publishers of one link produces no error at all: the robot
twitches and the map smears. Connect it to Lecture A's "one parent per frame" — the tree rule is
what makes this fault *detectable*, and that is the point of the constraint.

**Register.** Both decks are written for non-native English speakers: short sentences, no idiom,
every term defined at first use.

## Room and equipment

- Computer-equipped classroom. Gazebo and RViz2 both running — this is a heavier session for
  lab machines than Weeks 2 and 3.
- **`tf2_tools` must be installed** for `view_frames`; it is a separate package on some
  installations, and `view_frames` also needs Graphviz. Check before the session.
- A PDF viewer on the lab machines, for `frames.pdf`.

## To be produced for this week

| Item | Status |
|---|---|
| `code/src/ee414_w07_tf2_frames/` — broadcaster and listener starters with `TODO`s | ❌ |
| `ros2_lab/expected_output.txt` from a real run | ❌ |
| A saved RViz2 config with the TF display already added | ❌ |
| Quiz 3: one composition by hand, one notation check, one "which transform do I ask for?" | ❌ |
| A prepared broken tree (double publisher) for students who cannot reproduce error 4 | ❌ |

## Consistency checks

- Frame names must match the TurtleBot3 URDF used in Week 8: `base_link`, `base_scan`,
  `imu_link`, `odom`, `map`.
- The `base_link` → `base_scan` height quoted in W07B (0.172 m) is the TurtleBot3 Burger value.
  **Verify against the actual model before delivery** and correct both decks if it differs.
- Backward references: Week 1 (nothing is instantaneous), Week 2 (`Header`, stamps, no-master
  start-up order, `topic info --verbose`), Week 3 (a callback never waits), Week 6 (obstacle
  avoidance in `base_link`).
- Forward references: Week 8 (URDF and `robot_state_publisher`), Week 10 (SLAM and AMCL publish
  `map` → `odom`), Week 11 (goals in `map`, gap clearance).
- Quiz 3 in Week 7 — matches the specification's assessment calendar.
- The distribution name appears in neither deck as literal text — `\rosver` only.
