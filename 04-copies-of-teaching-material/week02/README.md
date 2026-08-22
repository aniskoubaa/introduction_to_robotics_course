# Week 2 — ROS 2 Architecture and the Computation Graph

| | |
|---|---|
| **Lecture A (1.5 h)** | The computation graph: nodes, the four communication mechanisms, message types, discovery, QoS, workspaces and packages |
| **Lecture B (1.5 h)** | Hands-on: a workspace, a publisher, a subscriber, a launch file — and five deliberate failures |
| **CLO served** | CLO 1 (A) · CLO 3 (B) |
| **Assessment this week** | **Quiz 1** (in A) · **Assignment 1 posted** (in B, due Week 3) |
| **Tooling rung** | T1 — **first session requiring a working installation.** No install, no session. |
| **Reading** | ROS 2 docs: Concepts → Nodes, Topics, Discovery, QoS settings |

## Status

| Artifact | Path | Status |
|---|---|---|
| Lecture A deck | `slides/EE414_W02A_computation_graph.tex` / `.pdf` | ✅ 24 slides, builds clean |
| Lecture B deck | `slides/EE414_W02B_first_nodes.tex` / `.pdf` | ✅ 26 slides, builds clean |
| Lab checklist | `ros2_lab/README.md` | ✅ |
| Starter package | `../../code/src/ee414_w02_first_node/` | ❌ **not authored** |
| Expected-output transcript | `ros2_lab/expected_output.txt` | ❌ — standing rule 2 |
| Quiz 1 + key | `../../07-exams-answer-keys-or-assessment-rubrics/` | ❌ |
| Assignment 1 + rubric | `../../07-exams-answer-keys-or-assessment-rubrics/` | ❌ |
| Setup guide (M1) | `../../setup/README.md` + `check_ros2_setup.py` | ❌ **blocks this week** |

## Lectures

| File | Duration | Contents |
|---|---|---|
| `slides/EE414_W02A_computation_graph.tex` | 1.5 h · 24 slides | Recap of Week 1's five failures mapped to their answers; the node as one process doing one job; the four mechanisms (topic / service / action / parameter); topics as anonymous many-to-many; a real TurtleBot3 graph; messages as typed contracts; the five message types of the semester; `Header`, stamps and frames; discovery without a master; ROS 1 vs ROS 2; `ROS_DOMAIN_ID`; QoS — reliability, durability, history; choosing a profile; the incompatible-QoS silent failure; workspace anatomy; build-then-source; underlay and overlay |
| `slides/EE414_W02B_first_nodes.tex` | 1.5 h · 26 slides | Environment check; workspace; `ros2 pkg create`; generated layout; `talker.py`; `main` and `spin`; entry points in `setup.py`; build and run; `node list` / `topic list` / `echo` / `hz` / `info` / `pub`; `listener.py`; `rqt_graph`; what the pair proves; launch files; `ros2 launch`; five deliberate failures; the diagnostic order |

Build: `pdflatex <file>.tex` twice. `logo.png` must sit beside the `.tex`.

**Known cosmetic issue:** W02A reports one 0.24 pt overfull `\vbox` on the QoS-mismatch frame.
0.08 mm — below the visual threshold, left alone.

## Teaching notes

**A is vocabulary; B is where it becomes real.** Do not let A drift long. Every minute
overspent in A is a minute the room does not have when a third of them hit an installation
problem in B.

**W02A, "Where we left off."** Open by mapping Week 1's five failures onto their answers.
Students who missed Week 1 need it; students who were there get the payoff of a promise kept.
Ninety seconds, no more.

**W02A, the four mechanisms.** Resist teaching services and actions properly here. They get one
row each in a table, and that is correct for Week 2 — topics carry everything until Week 11.
Students who ask "when would I use an action?" get the Nav2 answer: *when the job takes forty
seconds and you might want to cancel it.*

**W02A, QoS.** This is the load-bearing section and the one most likely to be cut for time.
**Do not cut it.** The incompatible-QoS failure — two healthy nodes, no errors, no data — costs
a student a full day the first time, and it appears in Week 6 (LiDAR is best-effort) and Week 10
(maps are transient-local). Make them write down `ros2 topic info --verbose`.

**W02A, underlay and overlay.** Deliver the "open a clean terminal" advice as real engineering
advice, not a joke. Sourcing two workspaces into one shell produces the worst class of bug in
robotics: *the code you are editing is not the code that runs.*

**W02B is a walkthrough, not a demonstration.** Type it live, at their speed, with your terminal
font large. **Stop at every checkpoint.** A student who falls behind at Checkpoint 1 gets nothing
from the remaining fifty minutes, and will not say so unprompted.

**W02B, the entry point in `setup.py`.** This one line will generate more confusion than the rest
of the session combined, because a typo builds cleanly and fails only at run time. Say the
mapping out loud — *name you type = module path : function* — and make them read theirs back.

**W02B, "What you just proved to yourself."** This slide is the point of the whole session: four
of Lecture A's claims, verified by the student in twenty minutes rather than asserted by the
instructor. Have them actually kill the talker and watch the listener survive. It takes ten
seconds and it is the moment the architecture stops being abstract.

**W02B, the five failures.** Cause them deliberately, in order, and make the room read the
symptom **before** you give the cause. Three of the five look identical from outside — two
healthy nodes and silence — and that is exactly the lesson. The diagnostic order on the next
slide is the same four commands they will use in Week 11 on a robot with forty topics.

**Register.** Both decks are written for non-native English speakers: short sentences, no idiom,
every term defined at first use.

## Room and equipment

- **A computer-equipped classroom, or every student on a laptop.** This is the first session
  where the room requirement in the specification actually binds.
- Large terminal font on the projector. 14 pt is unreadable from row 6.
- **Assign `ROS_DOMAIN_ID` values before this session** if it was not done in Week 1. Without
  them, thirty students' nodes see each other and the graph exercise becomes noise.

## To be produced for this week

| Item | Status |
|---|---|
| Setup guide + `check_ros2_setup.py` | ❌ **blocks the session** |
| `code/src/ee414_w02_first_node/` — starter package with `TODO`s, plus the solution in the instructor archive | ❌ |
| `ros2_lab/expected_output.txt` — a real transcript from a real run | ❌ |
| Quiz 1 (10 min): nodes, the four mechanisms, one QoS question | ❌ |
| Assignment 1 + rubric: parameterised publisher, computing subscriber, launch file | ❌ |
| Fallback plan for students whose install failed — pair them, or a prepared Docker image | ❌ |

## Consistency checks

- The five failures in W02A's opening table must match W01B's "five reasons that loop fails".
- Assignment 1 due Week 3; Quiz 1 in Week 2 — matches the specification's assessment calendar.
- Forward references stated in these decks: actions → Week 11, `Header`/frames → Week 7,
  estimation → Week 9, best-effort LiDAR → Week 6, transient-local maps → Week 10, launch
  parameters → Weeks 8 and 11. If the calendar moves, these move.
- The distribution name appears in neither deck as literal text — `\rosver` only.

## The `#` constraint (preamble)

A `#` **may not be the first non-space character of a line** inside `pycode`, `shell` or `spec`.
Beamer's `[fragile]` scanner reads it as a macro parameter and the build dies with
`! Illegal parameter number in definition of \next`. Leading whitespace does not help. Inline
comments are fine. For a header comment — a `.msg` type name, a file path — put it in the prose
above the box, as W02A does with `geometry_msgs/msg/Twist`. The rule is documented in
`../shared/ee414-beamer-preamble.tex`.
