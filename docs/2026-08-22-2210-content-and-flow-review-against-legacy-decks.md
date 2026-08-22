# Content and logical-flow review — EE 414 against the legacy ROS course

**Date:** 22 August 2026
**Companion to:** `2026-08-22-2153-slide-design-review-against-legacy-decks.md` (density and format)
**This document:** what is taught, in what order, and why the legacy ordering works better.

---

## 1. The engine the legacy course runs on, and mine does not

Three consecutive slides in the navigation deck (133–135):

> **PROBLEM STATEMENT: GO-TO-GOAL**
> **PROBLEM STATEMENT: GO-TO-GOAL + OBSTACLE AVOIDANCE**
> **PROBLEM STATEMENT: FIND A PATH + OBSTACLE AVOIDANCE**

Same question, three times, each adding one difficulty the previous solution cannot handle. Every
tool that follows arrives as **the answer to a problem the student has already watched fail.**
Feedback control answers the first. Bug algorithms answer the second. Map-based navigation
answers the third.

EE 414 motivates differently: I show the five-block pipeline (perception → estimation →
localization → planning → control) in Week 1 and then fill one block per week. That is a
**declarative** structure — here is the architecture, here are its parts. It is accurate,
tidy, and it never creates *need*. A student reaching Week 10 has no felt reason why SLAM
exists, because nothing they built has yet failed for want of a map.

**This is the deepest difference between the two courses, and it is a flow problem, not a
content problem.** The topics are nearly the same. The legacy course earns each one.

### Recommendation

Adopt an escalating problem statement as the spine, and open **every** week with the version of
it that this week's tool answers:

| Week | The problem, escalated | The tool it forces |
|---|---|---|
| 4 | Make the robot go **there** | Kinematics, `/cmd_vel` |
| 5 | Make it go there **accurately** | Feedback control |
| 6 | Make it go there **without hitting anything** | LiDAR, reactive avoidance |
| 6B/11A | It got stuck in a **U-shaped corridor** | Bug algorithms — reactive has limits |
| 9 | It thinks it is somewhere it is not | State estimation |
| 10 | It needs to know where **"there"** is | Mapping and localization |
| 11 | Find a path through a building it has a map of | Global + local planning |

Each week's opening slide is the previous week's solution *breaking*.

---

## 2. Known-to-unknown ordering: three places I inverted it

### 2.1 Transformations — translation before rotation

Legacy order (nav deck, pages 9–100):

```
coordinate frame -> location in WORLD frame -> location in ROBOT frame
   -> THE SAME LOCATION IN BOTH FRAMES (7 slides)
   -> transformation types -> TRANSLATION ONLY (5 slides + 7-slide derivation)
   -> translation + rotation -> transformation matrix
   -> 3D frames -> right-hand rule -> roll/pitch/yaw -> general rotation matrix
   -> worked 3D example -> representation methods -> Euler -> Euler theorem
   -> quaternion -> conversions both ways -> WHY QUATERNION? -> benefits
```

My W07A order:

```
why frames -> frames on a robot -> the two questions -> ROTATION MATRIX
   -> properties -> point vs frame -> Rp+t abandoned -> homogeneous coordinates
   -> notation -> worked example -> tree -> 3D and quaternions (one table) -> time
```

Four specific inversions:

**(a) I open with rotation. He opens with translation.** Translation is arithmetic a student
already owns — add 10 cm. Rotation requires trigonometry and the frame-versus-point distinction.
He establishes the *shape* of the whole idea (change of frame) on the easy operation, then
substitutes the hard one into a structure that is already familiar. I introduce the hardest
object on the first content slide.

**(b) I never show one point with two different coordinate pairs.** He spends seven slides
(15–21) on *location in the world frame*, *location in the robot frame*, then both together —
before any matrix appears. That is the concrete anchor for the entire week. My deck asserts "a
number without a frame is meaningless" and then never shows the two numbers side by side. **The
claim is made and never demonstrated.**

**(c) 3D is one table row in my deck.** He gives right-hand rule (with an exercise), roll-pitch-yaw,
the general rotation matrix, and a worked 3D example. My students meet a quaternion inside
`/odom` in Week 9 and inside `/amcl_pose` in Week 10. One table row does not prepare them.

**(d) "Why quaternions" is one table cell in mine; a full section after the mechanics in his.**
He shows Euler angles, shows the conversions, lets the student feel gimbal lock — *then* asks
`WHY QUATERNION?` in 100-point type. I state the answer before the student has the problem.

> **The principle I got wrong:** my house style is why-first, and that is right for *tools* —
> why ROS 2, why a middleware, why actions. It is wrong for *mathematics*. You cannot want
> quaternions until Euler angles have hurt you. **Why-first for tools; pain-first for maths.**

### 2.2 TF2 — no physical robot before the abstract tree

His TF sequence opens: `WHAT IS TF?` → **`HOW A ROBOT LOOKS LIKE?`** (a photograph, links and
joints) → `URDF: ROBOT DESCRIPTION LANGUAGE` → `WHY TF?` → `BENEFITS OF TF` → the tools.

Mine opens with `view_frames` on a running robot and a tree of names: `map`, `odom`,
`base_link`, `base_scan`. Correct, and abstract from the first second. **The frames are attached
to a physical object, and I never show the object.**

He also anchors frames to messages the students already use: `ODOM POSITION MESSAGE FORMAT`,
`AMCL_POSE POSITION MESSAGE FORMAT`, `CONVERSION OF ORIENTATION`, `TURTLEBOT3 ROTATION`. The
abstraction lands in the `/odom` message they echoed in Week 4. Mine mentions `Header` and
stops.

### 2.3 Control — no everyday analogy

Legacy slide 137 is titled **`SHOWER FEEDBACK`**: desired 35°, measured 45°, controller (you),
actuator (the tap), "turn hotter, not colder". The block diagram on slide 138 is then the same
picture with the labels changed.

My Week 5 brief goes straight to proportional and PID control from EE 306. For a cohort that has
had a control course this is defensible — but the shower diagram costs one slide and makes the
block diagram *readable* rather than recalled.

**Across all eight of my decks there is not one analogy from daily life.** That is a systematic
omission, not an oversight in one place.

---

## 3. The within-lecture pattern

Reading the legacy decks, the same ten-step shape recurs for every major topic:

| # | Step | Example |
|---|---|---|
| 1 | **Problem statement** — what we cannot do yet | `PROBLEM STATEMENT: GO-TO-GOAL` |
| 2 | **Everyday analogy** | `SHOWER FEEDBACK` |
| 3 | **Concept, one idea per slide, animated** | `COORDINATE FRAME: TRANSLATION` ×5 |
| 4 | **Formal derivation, one algebraic step per slide** | *"and substituting Eq. 2.4 we write"* ×7 |
| 5 | **See it work — video or live demo** | `FOLLOWER DEMO`, `TURTLEBOT3 SLAM DEMO` |
| 6 | **Explore the running system from the CLI** | `rostopic echo`, `tf_echo`, `view_frames` |
| 7 | **Practical tips — the numbered procedure** | `Practical Tips to Write Publisher ROS Topics`: Step 1 name → Step 2 type → Step 3 frequency → Step 4 object → Step 5 publish |
| 8 | **Code, one line per slide** | `Create a Publisher Object` → `Publish the ROS Message` |
| 9 | **Run it** | `Running the Talker Node` |
| 10 | **Parameters and tuning — same scene, different values** | `GLOBAL_PLANNER: EXAMPLE OF DIFFERENT PARAMETERS` ×2 |

My decks implement roughly steps 1, 3, 8 and 9, plus two of my own that he does not have
(deliberate failure, and the diagnostic order). **Steps 2, 5, 7 and 10 are absent from every
deck I have written.**

Of those four, **step 7 is the cheapest and most valuable.** A five-line numbered procedure that
tells a student *how to decide* — pick a name, pick a type, pick a rate, create the object, keep
publishing — is the thing they carry into an exam and into the project. I teach the mechanism and
never the procedure.

---

## 4. Content genuinely missing from the EE 414 plan

Ranked by how much each costs the course.

### 4.1 Reactive navigation and the Bug algorithms — **the biggest gap**

He teaches `WHAT IS BUG ALGORITHM?` → `ASSUMPTIONS` (reactive paradigm: sense + act, no global
map, sensors only) → `BUG 0` (head to goal; follow boundary) → `BUG 1`, with the original
Lumelsky & Stepanov (1987) citation.

This sits exactly between reactive obstacle avoidance and map-based navigation, and it does
three jobs at once:

1. Names the **reactive paradigm** as a paradigm, against the deliberative one.
2. Gives a **complete navigation algorithm the student can implement in 90 minutes** — two
   behaviours and a switch.
3. **Makes the map necessary.** Bug 0 fails visibly in a U-shaped obstacle. That failure is the
   reason SLAM exists, and the student watches it happen.

My plan jumps from Week 6 (reactive avoidance) to Week 11 (Nav2) with nothing between. **Nav2
therefore arrives as a configuration exercise rather than as an answer.** Add Bug 0/Bug 1 to
Week 6B or Week 11A.

### 4.2 A* as an animated algorithm

He spends **23 consecutive slides** (245–267) walking A* node by node across a grid, plus a link
to a live visualiser. My Week 11 brief has "Dijkstra and A*" in a bullet inside a lecture that
also covers costmaps, planners, controllers and behaviour trees.

For an EE elective, A* deserves 8–12 slides of its own with the open/closed lists filled in step
by step, and the heuristic changed to show the effect. It is the one algorithm in the course a
student can fully understand end to end.

### 4.3 The "robot setup" checklist

Six slides titled `ROBOT SETUP` enumerate what a robot must provide before the navigation stack
will run at all: a valid TF tree, odometry, a laser source, a base controller accepting
`/cmd_vel`, a map. This is **the integration knowledge that makes a project work**, and it exists
nowhere in my material. It belongs in Week 12 (integration) and should be issued as a one-page
checklist the project teams tick off.

### 4.4 Parameters come from measurement, not guessing

`HOW TO OBTAIN THE MAXIMUM VELOCITY` · `HOW TO OBTAIN THE MAXIMUM ACCELERATION` · `HOW TO OBTAIN
THE MINIMUM VALUES?` — a procedure for measuring a real robot's limits and putting the measured
numbers into the planner configuration.

My Week 3 teaches the parameter *mechanism* (declare, get, set live) and my Week 5 says "tune the
gains". Neither says **where a number comes from**. This is a one-slide procedure with a large
payoff in the project.

### 4.5 Showing the effect of a parameter

`GLOBAL_PLANNER: EXAMPLE OF DIFFERENT PARAMETERS` appears twice — the same scenario, planned
under two configurations, side by side. That is how tuning is taught: not "there are parameters"
but "here is what this one does to the path."

Every tuning topic in my course (Week 5 gains, Week 9 EKF covariances, Week 10 SLAM resolution,
Week 11 costmap inflation) should carry one before/after pair.

### 4.6 The local planner as a concept

`DWA ALGORITHM` → `DYNAMIC WINDOW APPROACH` → `TRAJECTORY SCORING` → parameters. Nav2's DWB
controller is a direct descendant, and a student who has seen candidate trajectories scored can
configure it. My Week 11 brief says "global vs. local planners" and moves on.

### 4.7 Real sensor hardware

`Commercial Laser Scanners` ×4, `RGBD Cameras`, `Laser Range Finder Hokuyo URG-04LX` — actual
part numbers, ranges, resolutions, prices. My Week 6 brief has a generic taxonomy table. Real
parts make the trade-off (range vs. cost vs. update rate) concrete and are what a graduate will
actually be asked to specify.

### 4.8 Deliberately out of scope — but say so

The legacy course also covers **OpenCV and camera perception**, **rosserial/Arduino**, **aerial
robots** and **robotic arms**. EE 414 is 45 contact hours and cannot hold these; the exclusion is
correct. But it should be **stated on a slide in Week 1** — students who expect vision, drones or
arms should know in week one, and should be pointed at where to get them.

---

## 5. Flow problems inside my own decks

Independent of the legacy comparison, re-reading my eight decks against the ten-step pattern:

| Deck | Flow problem |
|---|---|
| **W01B** | Sense–plan–act, taxonomy, anatomy, pipeline, three truths, then middleware. The middleware argument is excellent and arrives 20 slides in, after the student's attention has been spent on a taxonomy they cannot yet use. **Move the naive `while` loop earlier.** |
| **W02A** | Nine concepts (nodes, four mechanisms, messages, headers, discovery, QoS, workspaces, overlay) in one 90-minute session. This is the densest lecture in the course by concept count. **QoS or workspaces should move to W02B or Week 3.** |
| **W02B** | Reaches `ros2 pkg create` on slide 4. No exploration of a running system first. **Insert 10 minutes of turtlesim/TurtleBot3 poking before any authoring.** |
| **W03A** | Three failure modes, then interfaces, then services, then parameters, then actions. Parameters are unrelated to the "three shapes" spine and interrupt it. **Move parameters to the end, or to Week 5 where tuning motivates them.** |
| **W07A** | Ordering inverted as in §2.1. Also: the tree (one parent per frame) arrives *after* homogeneous coordinates, but it is the simpler idea and motivates why composition matters. **Tree before matrices.** |
| **W07B** | Checkpoint 4 is "watch a point move between frames" — correct and abstract. His equivalent is the **turtle follower**: turtle2 chases turtle1 using only TF. A complete behaviour, visibly delightful, same mechanism. **Replace the checkpoint with the follower.** |

---

## 6. Worked example — W07A resequenced

**Current (21 slides):** why frames · frames on a robot · two questions · rotation matrix ·
properties · point-vs-frame · abandon `Rp+t` · homogeneous · notation · worked example · tree ·
3D and quaternions · time · summary.

**Proposed (≈45 slides at the new density):**

| Block | Slides | Content |
|---|---|---|
| **1. The problem** | 3 | "The LiDAR says 2.1 m at 30°. Where is the obstacle?" — unanswerable. Photograph of a TurtleBot3 with the laser visibly *not* at the centre. |
| **2. One point, two answers** | 6 | The obstacle in the world frame. The same obstacle in the robot frame. Both together, two number pairs, one object. **No matrices yet.** |
| **3. Translation alone** | 5 | Shift the origin. Derive $p_A = p_B + t$ one line per slide. Trivially true, and it is the shape of everything that follows. |
| **4. Rotation** | 6 | Rotate the frame. Build $R(\theta)$ column by column. The $90°$ sanity check. |
| **5. Point vs frame** | 3 | The transpose. Physical demonstration: turn the object, then turn yourself. |
| **6. Both together** | 5 | `Rp + t`, then why it does not chain, then homogeneous coordinates as the fix. |
| **7. Notation and the tree** | 5 | $T_{AC}=T_{AB}T_{BC}$, inner indices cancel. One parent per frame. Worked 10 cm example. |
| **8. Into 3D** | 8 | Right-hand rule **+ exercise**. Roll-pitch-yaw. General rotation matrix. A worked 3D example. |
| **9. Euler, and its problem** | 4 | Euler angles. Gimbal lock — **shown**, as a loss of a degree of freedom. |
| **10. `WHY QUATERNIONS?`** | 4 | Full-bleed question. Then the benefits, and the `/odom` message where they will meet one next week. |
| **11. Time** | 3 | A transform is valid at an instant. The two extrapolation errors. |
| **12. Summary + tips** | 2 | Six take-aways, plus a numbered *how to decide which transform to ask for* procedure. |

Same content. Translation before rotation, the concrete anchor before the algebra, 3D given real
weight, and the quaternion question asked after the student has felt the need.

---

## 7. Priority order

| # | Change | Cost | Effect |
|---|---|---|---|
| 1 | Adopt the **escalating problem statement** as the course spine; open every week with the previous week's solution failing | ~2 h | Fixes the deepest structural weakness |
| 2 | Add **Bug 0 / Bug 1** to Week 6 or 11 | ~4 h | Makes maps necessary rather than assumed |
| 3 | Resequence **W07A** per §6 (translation first, concrete anchor, 3D expanded) | ~4 h | Fixes the worst-ordered deck |
| 4 | Add a **numbered "practical tips" procedure** to every major concept | ~3 h total | Highest value per hour of any item here |
| 5 | Add an **everyday analogy** to each maths-heavy topic (shower → control, and equivalents for estimation and costmaps) | ~2 h | Removes a systematic omission |
| 6 | **Demo before code** in every B session: see it work, then build it | ~2 h | Fixes the abstract-first habit |
| 7 | Expand **A\*** to 8–12 animated slides; add **DWA** and **trajectory scoring** | ~5 h | Week 11 becomes teaching, not configuration |
| 8 | Add the **robot-setup checklist** to Week 12 and the project brief | ~1 h | Directly raises project pass rate |
| 9 | Add **before/after parameter pairs** to every tuning topic | ~3 h | Teaches that parameters have meaning |
| 10 | Add **real sensor hardware** to Week 6; state the **out-of-scope** list in Week 1 | ~2 h | Concreteness and honest expectations |

Items 1, 4, 5 and 6 are cheap and apply to every deck. **Do them before rewriting anything at
the new density**, so the rewrite lands the format and the flow in one pass rather than two.

---

## 8. Summary

The density review said my slides read like a specification. This one says something narrower and
more fixable: **the topic list is right and the ordering of tension is wrong.**

The legacy course works because nothing is introduced until the student has watched the previous
thing fail. Mine is organised as an architecture diagram being filled in — every part correct,
every part arriving before it is wanted. Fixing that is mostly resequencing and a handful of new
slides, not new subject matter.

The three concrete additions that would change the most: **Bug algorithms** (so maps become
necessary), **numbered procedures** (so students know how to decide, not just how it works), and
**one everyday analogy per mathematical topic** (so the formalism has something to land on).
