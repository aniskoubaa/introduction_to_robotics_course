# Week 2 — ROS 2 Architecture and the Computation Graph

| | |
|---|---|
| **Lecture A (1.5 h)** | The computation graph: nodes, the four communication mechanisms, message types, discovery, QoS |
| **Lecture B (1.5 h)** | Hands-on: take turtlesim apart from the CLI, then build a workspace, a publisher, a subscriber, a launch file — and five deliberate failures |
| **CLO served** | CLO 1 (A) · CLO 3 (B) |
| **Assessment this week** | **Quiz 1** (in A) · **Assignment 1 posted** (in B, due Week 3) |
| **Tooling rung** | T1 — **first session requiring a working installation.** No install, no session. |
| **Reading** | ROS 2 docs: Concepts → Nodes, Topics, Discovery, QoS settings |

## Status

| Artifact | Path | Status |
|---|---|---|
| Lecture A deck | `slides/EE414_W02A_computation_graph.tex` / `.pdf` | ✅ 36 slides, builds clean |
| Lecture B deck | `slides/EE414_W02B_first_nodes.tex` / `.pdf` | ✅ 42 slides, builds clean |
| Legacy figures | `slides/figures/w02_*.png` | ✅ 6, each credited on its slide |
| Lab checklist | `ros2_lab/README.md` | ✅ |
| Starter package | `../../code/src/ee414_w02_first_node/` | ❌ **not authored** |
| Expected-output transcript | `ros2_lab/expected_output.txt` | ❌ — standing rule 2 |
| Quiz 1 + key | `../../07-exams-answer-keys-or-assessment-rubrics/` | ❌ |
| Assignment 1 + rubric | `../../07-exams-answer-keys-or-assessment-rubrics/` | ❌ |
| Setup guide (M1) | `../../setup/README.md` + `check_ros2_setup.py` | ✅ written; **not yet run on a clean machine** |

## Lectures

| File | Duration | Contents |
|---|---|---|
| `slides/EE414_W02A_computation_graph.tex` | 1.5 h · 36 slides | Recap of Week 1's five failures mapped to their answers; **the whole lecture in one figure**; the node as one process doing one job; topics as anonymous many-to-many; a real TurtleBot3 graph; **the four mechanisms one figure at a time** (topic / service / action / parameter) before the comparison table; **four questions that choose between them**; messages as typed contracts; the five message types of the semester; `Header`, stamps and frames; **the `roscore` that no longer exists**; **the ROS 1 commands you will hit online, and their ROS 2 equivalents**; discovery without a master; `ROS_DOMAIN_ID`; QoS — reliability, durability, history; choosing a profile; the incompatible-QoS silent failure; **`ros2 topic info --verbose` one token per slide**; the silent-topic diagnostic order |
| `slides/EE414_W02B_first_nodes.tex` | 1.5 h · 42 slides | Environment check; **turtlesim — a robot you did not write**; `ros2 run` one token per slide; teleop; `node list` / `topic list` / `node info` / `interface show` / `topic echo` / `topic pub`; **what you learned with no source code**; workspace anatomy; `colcon build`; underlay and overlay; `ros2 pkg create` one token per slide; generated layout; `talker.py`; `main` and `spin`; entry points in `setup.py`; build and run; inspecting your own node the same way; `listener.py`; `rqt_graph`; what the pair proves; launch files; `ros2 launch`; five deliberate failures; the diagnostic order |

Build: `pdflatex <file>.tex` **three times**. Two passes is not enough — the section divider
positions with `remember picture,overlay` and its page anchors come from the `.aux`, so on pass
two the divider renders as a dark rectangle with no text on it. `logo.png` must sit beside the
`.tex`; `figures/` beside it too.

**Known cosmetic issue:** W02B reports one 1.79 pt overfull `\vbox` (0.6 mm). Below the visual
threshold, left alone.

## What changed in the August 2026 revision

Both decks were rebuilt in the style of the instructor's own ROS course
(`../../../anis_slides_legacy/`). Four changes, none of them cosmetic:

**1. Workspaces moved out of A and into B.** A was carrying nine concepts in ninety minutes,
which the deck review flagged as the densest lecture in the course. Workspaces, `colcon`,
sourcing and underlay/overlay are things you *type*, and they now live in the session where
they are typed. A is now vocabulary only.

**2. B is demo-first.** It opens with `turtlesim` — a robot simulator the students did not
write — and they take its graph apart with six commands before creating a package of their own.
Building the talker first made the CLI look like ceremony, because the only graph being
inspected was one they already understood. Inspecting somebody else's running system makes
those commands the *only* way to find out what is going on, which is what they are for in
Week 11 on a Nav2 stack nobody in the room wrote.

**3. Command anatomy (`\cmdanatomy`).** A command is shown once, large, with every token but
one faded almost to nothing and a single caption on a leader line below it. Repeat, moving the
highlight along, and `ros2 run turtlesim turtlesim_node` becomes four slides that each teach
one thing. A beginner cannot tell which of those words is ROS, which is the package and which
is the program — they are all lowercase, all underscored, all unfamiliar. Fading the other
three is what makes the question answerable.

**4. Real figures for the four mechanisms.** Topic, service and action now get a picture each
before the comparison table, and the `roscore` terminal appears as history — the process ROS 2
deleted — rather than as prose.

| Figure | Source | Used on |
|---|---|---|
| `w02_graph.png` | *ROS Robot Programming*, Pyo/Cho/Jung/Lim (ROBOTIS, 2017) | A — "The whole lecture, in one picture" |
| `w02_pubsub.png` | same | A — "One: a topic" |
| `w02_service.png` | same | A — "Two: a service" |
| `w02_action.png` | same | A — "Three: an action" |
| `w02_roscore.png` | Instructor's own ROS 1 course (2020), ROS Noetic | A — "This process does not exist any more" |
| `w02_ros1_cli.png` | same, `rosnode list` + `rostopic list` panes recomposed | A — "Half of what you will find online looks like this" |

> **Attribution is on the slide, every time, in small type.** Not a courtesy: the students are
> being taught to attribute, and a deck that quietly reuses a book's artwork teaches the
> opposite of what the Week 1 AI-tool policy asks of them.

**The course is ROS 2 only, but it says so out loud.** Two slides in A are deliberately ROS 1:
`roscore` as the process that was deleted, and a `rosnode list` / `rostopic list` capture beside
a seven-row translation table. Neither teaches a ROS 1 command as something to use. They exist
because students will search for help and the top result will be ROS 1 with no year on it —
better they meet the old commands here, labelled, than at midnight in an answer from 2016. The
one-second test on that slide (*starts with `ros` and no space after it → ROS 1*) is the part
worth making them repeat back.

> ⚠️ **The four book figures say ROS, not ROS 2, and one shows a ROS Master.** That is correct
> for what they illustrate — the *shapes* of the four mechanisms, which did not change — but say
> so when the parameter-server box appears in `w02_graph.png`. In ROS 2 parameters live in the
> node, not in a central server. It is a thirty-second correction and students will spot it.

## Teaching notes

**A is vocabulary; B is where it becomes real.** Do not let A drift long. Every minute
overspent in A is a minute the room does not have when a third of them hit an installation
problem in B.

**W02A, "Where we left off."** Open by mapping Week 1's five failures onto their answers.
Students who missed Week 1 need it; students who were there get the payoff of a promise kept.
Ninety seconds, no more.

**W02A, the four mechanisms.** Resist teaching services and actions properly here. One figure
and one table row each is correct for Week 2 — topics carry everything until Week 11. Students
who ask "when would I use an action?" get the Nav2 answer: *when the job takes forty seconds and
you might want to cancel it.* The "four questions, in order" slide that follows is the one to
make them write down; it is what stops somebody building a `drive_to_goal` **service** in Week 6
and losing an afternoon to a node that has gone deaf.

**W02A, the command-anatomy slides.** Five slides, one command. Do not rush them and do not
apologise for them. Advance, say the one caption, stop. The temptation is to say all five things
on the first slide and click through the rest — that throws away the entire effect, which is
that only one thing is legible at a time.

**W02A, underlay and overlay — moved.** It is now in **W02B**, immediately before the students
create their workspace. If you are working from an older printout, do not deliver it twice.

**W02A, QoS.** This is the load-bearing section and the one most likely to be cut for time.
**Do not cut it.** The incompatible-QoS failure — two healthy nodes, no errors, no data — costs
a student a full day the first time, and it appears in Week 6 (LiDAR is best-effort) and Week 10
(maps are transient-local). Make them write down `ros2 topic info --verbose`.

**W02A, underlay and overlay.** Deliver the "open a clean terminal" advice as real engineering
advice, not a joke. Sourcing two workspaces into one shell produces the worst class of bug in
robotics: *the code you are editing is not the code that runs.*

**W02B opens on turtlesim, and that is deliberate.** The first thirty minutes produce no code
at all. That will feel slow if you are behind schedule, and cutting it is the wrong economy: the
six CLI commands are the transferable skill of the whole week, and they only land while the
students are looking at a system they *cannot* read the source of. End the section on
"Twenty minutes, no source code" and let it sit.

**W02B, `ros2 topic pub` driving the turtle.** Have them close teleop first, or two publishers
fight over `/cmd_vel` and the turtle stutters — which is, admittedly, its own good lesson if you
have the time to name it.

**W02B is a walkthrough, not a demonstration.** Type it live, at their speed, with your terminal
font large. **Stop at every checkpoint.** A student who falls behind at Checkpoint 1 gets nothing
from the remaining fifty minutes, and will not say so unprompted.

**W02B, the entry point in `setup.py`.** This one line will generate more confusion than the rest
of the session combined, because a typo builds cleanly and fails only at run time. Say the
mapping out loud — *name you type = module path : function* — and make them read theirs back.
**Then point back at the morning:** the third token of `ros2 run turtlesim turtlesim_node` is a
name somebody declared in a line exactly like theirs. That is the moment the two halves of the
session join up.

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
| Setup guide + `check_ros2_setup.py` | ✅ written · ❌ **still untested on a clean machine** |
| `code/src/ee414_w02_first_node/` — starter package with `TODO`s, plus the solution in the instructor archive | ❌ |
| `ros2_lab/expected_output.txt` — a real transcript from a real run | ❌ |
| Quiz 1 (10 min): nodes, the four mechanisms, one QoS question | ❌ |
| Assignment 1 + rubric: parameterised publisher, computing subscriber, launch file | ❌ |
| Fallback plan for students whose install failed — pair them, or a prepared Docker image | ❌ |

## Consistency checks

- The five failures in W02A's opening table must match W01B's "five reasons that loop fails".
- The six CLI commands taught on turtlesim in W02B section 1 must be the same six used again on
  the student's own talker later in the deck. If one is added or dropped, change both places —
  the repetition *is* the teaching.
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
