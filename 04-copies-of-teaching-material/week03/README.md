# Week 3 — Communication Models in ROS 2

| | |
|---|---|
| **Lecture A (1.5 h)** | Three shapes of interaction (topic / service / action), the three failure modes of choosing wrong, interface definition, parameters |
| **Lecture B (1.5 h)** | Hands-on: an interfaces package, a custom message, a service both halves, the deadlock on purpose, parameters, a first action client |
| **CLO served** | CLO 1 (A) · CLO 3 (B) |
| **Assessment this week** | **Assignment 1 due** (end of week) |
| **Tooling rung** | T2 — first `ament_cmake` package; first build that generates code |
| **Reading** | ROS 2 docs: Services, Parameters, Actions; "About ROS 2 interfaces" |

## Status

| Artifact | Path | Status |
|---|---|---|
| Lecture A deck | `slides/EE414_W03A_communication_models.tex` / `.pdf` | ✅ 25 slides, builds clean |
| Lecture B deck | `slides/EE414_W03B_interfaces_services_params.tex` / `.pdf` | ✅ 25 slides, builds clean |
| Lab sheet | `ros2_lab/README.md` | ✅ |
| Starter packages | `../../code/src/ee414_w03_interfaces/`, `ee414_w03_nodes/` | ❌ **not authored** |
| Expected-output transcript | `ros2_lab/expected_output.txt` | ❌ — standing rule 2 |
| Assignment 1 collection + rubric | `../../07-exams-answer-keys-or-assessment-rubrics/` | ❌ |

## Lectures

| File | Duration | Contents |
|---|---|---|
| `slides/EE414_W03A_communication_models.tex` | 1.5 h · 25 slides | Stream / question / job; the decision table and the two-second test; failure 1 (a topic where you needed an answer); failure 2 (a service for something slow); failure 3 (the callback deadlock); `.msg` anatomy and field types; when *not* to define a custom message; `.srv` and `.action` separators; why interfaces live in their own package; `ros2 interface show`; the async service client; `ros2 service call`; parameters, declare and read; setting them from CLI and launch; the action exchange; `ros2 action send_goal --feedback`; the summary table |
| `slides/EE414_W03B_interfaces_services_params.tex` | 1.5 h · 25 slides | Two packages with different build types; writing `.msg` and `.srv`; the `CMakeLists.txt` lines; build and `interface show`; using a custom type from a node; echoing it; the service server; testing it from the terminal; **the deadlock, caused deliberately**; why it hangs, in one picture; the `add_done_callback` fix; parameters declared and read live; `ros2 param set` on a running node; parameters in launch; the Fibonacci action from the terminal; the action client; what you can now do |

Build: `pdflatex <file>.tex` twice. `logo.png` must sit beside the `.tex`.

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

## To be produced for this week

| Item | Status |
|---|---|
| `code/src/ee414_w03_interfaces/` — with the exact `CMakeLists.txt` and `package.xml` lines students copy | ❌ |
| `code/src/ee414_w03_nodes/` — starter nodes with `TODO`s | ❌ |
| `ros2_lab/expected_output.txt` from a real run | ❌ |
| Assignment 1 marking: rubric applied, samples kept for section 06 | ❌ |
| A prepared "hung node" example, in case a student cannot reproduce the deadlock | ❌ |

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
