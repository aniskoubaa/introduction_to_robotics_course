# Week 3 — Communication Models in ROS 2

| | |
|---|---|
| **Lecture A (1.5 h)** | Three shapes of interaction (topic / service / action), the three failure modes of choosing wrong, interface definition, parameters |
| **Lecture B (1.5 h)** | Hands-on: two packages with different build types, a custom message and service, a service both halves, the deadlock on purpose, parameters, a first action client |
| **CLO served** | CLO 1 (A) · CLO 3 (B) |
| **Assessment this week** | **Assignment 1 due** (end of week) |
| **Tooling rung** | T2 — first `ament_cmake` package; first build that generates code |
| **Reading** | ROS 2 docs: Services, Parameters, Actions; "About ROS 2 interfaces" |

## Status

| Artifact | Path | Status |
|---|---|---|
| Lecture A deck | `slides/EE414_W03A_communication_models.tex` / `.pdf` | ✅ 35 slides, builds clean |
| Lecture B deck | `slides/EE414_W03B_packages_and_interfaces.tex` / `.pdf` | ✅ 33 slides, builds clean |
| Screenshots | `slides/figures/shots/` | ✅ 30, all captured from a live run |
| Capture harness | `../shared/screenshots/` | ✅ the set is regenerable |
| Lab sheet | `ros2_lab/README.md` | ✅ |
| Starter packages | `../../code/src/ee414_w03_interfaces/`, `ee414_w03_nodes/` | ✅ both build clean |
| Expected-output transcript | `ros2_lab/expected_output.txt` | ✅ generated from a real run |
| Live-demo runbook | `ros2_lab/EE414_W03_demo_cue_sheet.html` | ✅ both decks, self-contained |
| Assignment 1 collection + rubric | `../../07-exams-answer-keys-or-assessment-rubrics/` | ❌ |

### Three errors the screenshots found

Executing the decks rather than typesetting them turned up three things that were wrong. This
is the standing rule earning its keep, so they are recorded rather than quietly fixed.

| Was | Is |
|---|---|
| `ros2 pkg create --build-type ament_python --dependencies rclpy std_msgs ee414_w03_nodes` | **Fails.** `--dependencies` takes a list and swallows the package name; the error then complains that no package name was given. The name must come first. W03B now teaches the correct form *and* shows the failure. |
| `interface show` on `WheelState` prints four lines | It prints **eight** — `show` expands `Header` down to `sec`, `nanosec` and `frame_id`. The typeset listing had been written from the `.msg` file, not from the command. |
| `spin_until_future_complete` inside a callback "freezes, prints nothing, does not crash" | On the pinned distribution it **raises** `RuntimeError: Executor is already spinning`. The genuine silent deadlock needs `client.call()`. W03B now shows both, which is better teaching than either alone: one failure names itself, the other does not. |

## Lectures

| File | Duration | Contents |
|---|---|---|
| `slides/EE414_W03A_communication_models.tex` | 1.5 h · 35 slides | Stream / question / job; the decision table and the two-second test; failure 1 (a topic where you needed an answer); failure 2 (a service for something slow); failure 3 (the callback deadlock); `.msg` anatomy and field types; when *not* to define a custom message; `.srv` and `.action` separators; why interfaces live in their own package; `ros2 interface show`; the async service client; `ros2 service call`; parameters, declare and read; setting them from CLI and launch; the action exchange; `ros2 action send_goal --feedback`; the summary table. One **Definition:** slide opens each of the four paradigm sections (topic, service, action, parameter), all four built from `\paradigmdef` so they carry the same four rows in the same order |
| `slides/EE414_W03B_packages_and_interfaces.tex` | 1.5 h · 33 slides | **ament vs. colcon** --- which tool owns which decision; two packages with different build types; writing `.msg` and `.srv`; the `CMakeLists.txt` lines; build and `interface show`; using a custom type from a node; echoing it; the service server; testing it from the terminal; **the deadlock, caused deliberately**; why it hangs, in one picture; the `add_done_callback` fix; parameters declared and read live; `ros2 param set` on a running node; parameters in launch; the Fibonacci action from the terminal; the action client; what you can now do |

Build: `pdflatex <file>.tex` **three times** — the section-outline slides need the `.toc`.

### Fitting the lecture into 35 slides

Both decks sit inside the 30–35 slide budget: A is 35, B is 32. A reached 51 first and was
compressed by **merging, never by dropping a concept**. Three patterns did the work:

- **Paired terminal captures became one two-up slide.** `service list` + `service call`,
  `param list` + `param set`, `interface show` on a service + on an action, `topic hz` +
  `topic info`. Each pair was always one idea shown twice; side by side it is a comparison,
  which is what the separator-counting and QoS slides actually need.
- **Tables that only interpreted a capture moved into that capture's caption.** The slide that
  mapped `node info` headings to the four mechanisms is now the caption under `node info`.
- **The three failure modes became three rows of one table.** As separate slides they were met
  one after another; as rows they are compared.

Two typeset blocks went in the process, both because a capture beside them said the same
thing: the hand-written `.srv`/`.action` pair (the real `Spawn` and `RotateAbsolute` captures
teach separator-counting better) and the QoS settings table (the `topic info --verbose` capture
already prints Reliability, Durability and History — the table was the screenshot retyped).

### The ament / colcon slide, and the Week 2 line it contradicted

Deck B opens its first section with **Two Tools: `ament` and `colcon`** (slide 4), added
5 September 2026. It was a real gap. Week 2B defines *workspace* and *package* but never says
what either **tool** is --- `colcon` appears there only as "colcon produces the other three
folders". That was survivable while every package was `ament_python` and the choice made
itself. In Week 3 the student has to *choose* a build type, and that choice cannot be made
without knowing which tool owns which decision.

The slide is one analogy, one three-row table, one keyline:

> A workspace is a building site. **ament** is the standard each package is built to;
> **colcon** is the foreman --- reads the plans, decides who works first, and never picks up
> a tool.
>
> **colcon decides *when* each package is built. ament decides *how*.**

It carries the two flavours as well (`ament_python` → setuptools for the nodes, `ament_cmake`
→ CMake for the interfaces, because message generation is a CMake job), which is what makes
the *next* slide's two different `--build-type` values read as a decision rather than as
magic. Build order from `package.xml` is deliberately not here --- it already lands two slides
later, on "Building and Verifying the Package", where students can see colcon do it.

**This exposed a factual error in Week 2B.** Its `\cmdanatomy` on `--build-type` said the
alternative `ament_cmake` "is C++ --- not used in this course". Both halves were wrong:
`ament_cmake` is CMake, not C++ (the interfaces package contains no C++ at all), and Week 3
requires it. `week02/slides/EE414_W02B_first_nodes.tex` now reads "The alternative is
`ament_cmake` --- CMake, which you need in Week 3 for message generation", which also plants
the reference a week early. W02B rebuilt: 43 pages, 0 errors, unchanged otherwise.

## Why deck B is named for packages, not just interfaces

The file was `EE414_W03B_interfaces_services_params.tex` until 5 September 2026, and the name
undersold it. Two of the six sections are gone before a single `.msg` field is written: the
deck opens by creating **two packages with two different build types** (`ament_cmake` for the
interfaces, `ament_python` for the nodes), configuring `rosidl_generate_interfaces` in
`CMakeLists.txt`, and building the pair with `colcon`. That is the part students get wrong,
and it was invisible in the filename. It is now `EE414_W03B_packages_and_interfaces.tex`,
titled *Your Own Packages and Interfaces*.

The **workspace** is deliberately not in the name. It is Week 2B's topic --- `week02/slides/
EE414_W02B_first_nodes.tex`, section "Where your own code lives", which creates `ee414_ws/`
and explains `src` / `build` / `install` / `log`. Week 3B reuses that workspace and says so on
its Session Structure slide ("Your Week 2 workspace, one new interfaces package, one new nodes
package"). Naming it twice would suggest the workspace is rebuilt here, and it is not.

Services, parameters and actions stay out of the filename for the same reason every other deck
has a short slug --- `first_nodes`, `computation_graph`, `tf2`. A filename that lists every
topic is a filename that goes stale on the next edit. The full scope lives in the subtitle:
*Creating Packages, Defining Interfaces, Implementing Services, Parameters and Actions*.

## Why deck A does not use this week's packages

Deck A teaches on `turtlesim`, `LaserScan` and invented examples (`PowerStatus.msg`,
`IsCharged.srv`) — never on `WheelState`, `ResetOdom` or the `ee414_w03_*` packages. Those are
session B's deliverables, and a lecture that displays them has already answered B's
checkpoints. This was not true before: A showed both, so students arrived at the lab having
seen its results.

A carries **one** typed command (`--ros-args -p`, which no capture shows). Everything else a
student is meant to run appears as a real capture. Three hand-typed transcripts were removed
because executing them showed they were wrong — the `LaserScan` listing omitted
`time_increment`, `scan_time` and `intensities`; the `ros2 service list` listing showed one
service where the real command prints seven; the Fibonacci transcript printed feedback as
`[0, 1, 1, 2]` where the CLI prints a YAML list. In each case a correct capture of the same
command was already two slides away. Deck B's typed blocks are *commands to type* with no
asserted output, each followed by the capture of its result — that pattern is fine and stays.

Deliberate repetition that remains: A explains the deadlock and B causes it; A introduces
`declare_parameter` and launch-file parameters and B applies both to their own node. That is
the lecture/lab split, not duplication.

Deck A is ordered **Interaction Models → Interface Definitions → Topics → Services → Actions →
Parameters → Application to a Mobile Robot**, and deck B **Custom Interface Packages →
Publishing on a Topic → Service Server and Client → Executor Deadlock → Parameters → Action
Clients**. Topics used to have no section of its own in either deck — the outline named
services, actions and parameters, so the one mechanism students had already met was the one
the contents page never mentioned. The paradigm sections follow the order the deck's own
summary table uses (stream, question, job, setting), not the order they were written in.
`logo.png` must sit beside the `.tex`.

## The turtlesim thread

W03A no longer describes the four mechanisms and then names examples. It runs **one node** and
interrogates it. `turtlesim` is the only node in the ecosystem small enough to hold in your
head that nevertheless exposes all four:

| Shape | On `turtlesim` |
|---|---|
| topic | `/turtle1/pose` out, `/turtle1/cmd_vel` in |
| service | `/spawn`, `/turtle1/set_pen`, `/clear`, `/kill` |
| action | `/turtle1/rotate_absolute` — a real action, with feedback |
| parameter | `background_r/g/b` — and the window repaints when you change one |

`ros2 node info /turtlesim` prints all four under four headings on one screen. That single
capture is the spine of the lecture; everything after it is a closer look at one heading.

The last block of A repeats the same four on the TurtleBot 3 in Gazebo, so nobody leaves
believing the mechanisms were a property of the toy.

**Two live sessions are needed to teach A as written:**

```bash
ros2 run turtlesim turtlesim_node
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Both are on the slides as screenshots, so the lecture survives if a demo will not start — but
run them live if you can. The `/spawn` and `background_r` moments land far harder when the
window is on the projector rather than in an image.

**Known cosmetic issues:** W03B reports three overfull `\vbox` warnings of 1.5 pt, 0.5 pt and
0.3 pt (all under 0.5 mm). Below the visual threshold; left alone.

## Teaching notes

**The spine of this week is a question, not a list.** *Is this a stream, a question, or a job?*
Every slide in A serves that question. Students who leave able to answer it for a new situation
have got the week; students who memorised three definitions have not.

**W03A, the three failures.** These are the reason the lecture exists. Deliver them as
consequences, not as warnings — "here is what your robot does on demo day" lands where "prefer
actions for long tasks" does not. Failure 3 (the deadlock) is deliberately *not* solved in A;
they cause it themselves in B, forty minutes later.

**W03A, "when not to define a custom message."** Push hard here. The instinct of every student
is to invent their own type, and every custom type is a wall between their robot and the
ecosystem. The concrete version: *publish your own `MyLaserScan` and RViz2 cannot draw it and
`slam_toolbox` cannot consume it.* They meet that consequence for real in Week 10.

**W03A, actions.** Keep this light. They need the shape — goal, feedback, result, cancel — and
one command. Full action *servers* are not required until the project. The honest framing is:
"today's `fibonacci` is Nav2's interface with the robot removed."

**W03B, the deliberate deadlock is the centrepiece.** Do not skip it for time, and do not warn
them out of it. Have the whole room write the hanging version, watch their own node freeze, and
sit with it for a moment before the explanation. A hang with no error message is the hardest
thing a beginner can meet in ROS 2, and meeting it under supervision — once — is worth an hour
of them meeting it alone at midnight in Week 11.

**W03B, "test one half from the terminal first."** This is the transferable habit of the whole
session: build the server, prove it with `ros2 service call`, *then* write the client. It halves
the search space for every bug they will have this semester. Say it explicitly.

**W03B, the CMakeLists lines.** Tell them to copy from the lab sheet and say plainly that
nobody memorises this. Time spent on CMake syntax is time not spent on the concept, and the
concept is *definitions are generated code*.

**W03B, parameters.** Make sure they read the parameter *inside the timer callback*, not once in
`__init__` — otherwise `ros2 param set` appears not to work and they conclude parameters are
broken. Then have them change a value while the node runs. That moment is what makes Week 5
tuning possible.

**Register.** Both decks are written for non-native English speakers: short sentences, no idiom,
every term defined at first use.

## Room and equipment

- Computer-equipped classroom, as Week 2.
- **`action_tutorials_py` must be installed** for the Fibonacci demo. Check before the session;
  it is a separate package on some installations.
- Warn students at the end of B to **launch Gazebo once before Week 4**. Week 4B is the first
  simulation session and finding out then that Gazebo does not start costs the whole hour.

### Two more the cue sheet found

Writing the runbook meant running every Deck A command again, one at a time, and pasting what
came back. Two claims did not survive that.

| Was | Is |
|---|---|
| `ros2 service list -t \| grep -v parameter` lists **seven** services | It lists **eight**. `/turtlesim/get_type_description` is not a parameter service, so the `grep` does not remove it. The count appeared only in the cue sheet, never on a slide, so no deck changed. |
| `ros2 topic info` reports `Publisher count: 1` whether or not anything is being sent | With nothing publishing it reports **0**; while `topic pub` runs it reports **1**. The teaching point survives — the number counts *connections*, not traffic, so a connected-but-silent publisher still counts — but it has to be shown with both states, which is what the runbook now does. |

## To be produced for this week

| Item | Status |
|---|---|
| `code/src/ee414_w03_interfaces/` — with the exact `CMakeLists.txt` and `package.xml` lines students copy | ✅ |
| `code/src/ee414_w03_nodes/` — `wheel_publisher`, `odom_node`, `reset_client`, `driver` | ✅ solution versions; **starter versions with `TODO`s still to cut** |
| `ros2_lab/expected_output.txt` from a real run | ✅ |
| A prepared "hung node" example, in case a student cannot reproduce the deadlock | ✅ `reset_client --ros-args -p mode:=hang` |
| Assignment 1 marking: rubric applied, samples kept for section 06 | ❌ |

## Consistency checks

- Assignment 1 due this week; Assignment 2 in Week 5 — matches the specification calendar.
- Forward references stated in these decks: tuning gains → Week 5, costmaps and
  `navigate_to_pose` → Week 11, simulation clock → Week 8, `slam_toolbox` consuming standard
  types → Week 10, Gazebo → Week 4B. If the calendar moves, these move.
- The async-callback rule stated here ("a callback never waits") is relied on again in Weeks 6,
  9 and 11.
- The distribution name appears in neither deck as literal text — `\rosver` only.
- **`#` may not start a line inside a code box.** Both decks respect this; the `.msg` field
  comments in W03A use `<-` arrows rather than `#`.
