# Week 1 — Introduction to Robotics and the ROS 2 Ecosystem

| | |
|---|---|
| **Lecture A (1.5 h)** | Course overview: what the course is for, how it works, assessment, policies, setup |
| **Lecture B (1.5 h)** | What is a robot: sense–plan–act, anatomy, the autonomy pipeline, why robot software needs a framework |
| **CLO served** | CLO 1 (both) · CLO 4 introduced in A (AI policy, attribution) |
| **Assessment this week** | — |
| **Tooling rung** | T0 — **no computer required in either session.** Installation is homework. |
| **Reading** | ROS 2 documentation, "Concepts" page (skim); Corke Ch. 1 |

## Status

| Artifact | Path | Status |
|---|---|---|
| Lecture A deck | `slides/EE414_W01A_course_overview.tex` / `.pdf` | ✅ 36 slides, builds clean |
| Lecture B deck | `slides/EE414_W01B_what_is_a_robot.tex` / `.pdf` | ✅ 30 slides, builds clean |
| Shared preamble | `../shared/ee414-beamer-preamble.tex` | ✅ |
| Exercise set + key | `exercises/EE414_W01_exercises.pdf` / `_solutions.pdf` | ❌ not authored |
| Setup guide (M1) | `../../setup/README.md` + `check_ros2_setup.py` | ❌ **critical path** |

## Lectures

| File | Duration | Contents |
|---|---|---|
| `slides/EE414_W01A_course_overview.tex` | 1.5 h · 36 slides | **Who is teaching this**; **four video slots**; what the course is for; the theory-course/this-course contrast; where you end up by Week 11; three reasons robotics is hard; the four CLOs; the weekly A/B shape; the 11+4 calendar; the pipeline-to-weeks map; logistics; the pinned stack; books; **what this course does not cover**; assessment and the exam blueprint; assignments and project; policies; AI-tool policy; setup and `ROS_DOMAIN_ID`; the week's checklist |
| `slides/EE414_W01B_what_is_a_robot.tex` | 1.5 h · 30 slides | Which of these is a robot; sense–plan–act definition; the loop; automation vs autonomy; robot families; why mobile robots; anatomy; the sensor table; the differential drive; the five-block pipeline; "go to the door" traced; three hard truths; the naive `while` loop and its five failures; the computation graph as the answer; ROS 2 honestly; the ecosystem; a first node; `ros2 topic echo` |

Build: `pdflatex <file>.tex` twice. `logo.png` must sit beside the `.tex`.

**Known cosmetic issue:** W01B reports one 0.51 pt overfull `\hbox` (0.18 mm) on the
"go to the door" frame. It does not resize with the column widths, so it is not the table.
Below the visual threshold; left alone rather than chased.

## ⚠️ Before delivering — two things to fill in

### 1. The four video clips

The deck has four `\videoslide` slots opening section 1, ~2.5 minutes total, before any
technical claim. **The URLs live here, never on the slide** — a dead link on a projected slide
is worse than no slide. Download the clips to `slides/video/` if the room's network is
unreliable.

| # | Slot | Length | What to find | URL / file |
|---|---|---|---|---|
| 1 | Warehouse robots, at scale | 45 s | An AMR fleet moving stock in a live warehouse (Amazon Robotics, Locus, Geek+) | ❌ |
| 2 | Where people should not go | 45 s | A legged or wheeled robot inspecting an industrial plant (ANYbotics, Spot at a refinery) | ❌ |
| 3 | A robot changing its mind | 30 s | A mobile robot re-planning around a person who steps into its path — **a Nav2 demo, so it is literally Week 11** | ❌ |
| 4 | Built here | 45 s | RIOTU Lab robots and drones — your own footage | ❌ |

**Each clip is followed by exactly one sentence**, already on the slide, naming what they just
saw in the course's vocabulary. A clip with no naming sentence is entertainment. Do not add a
fifth clip; four is already the limit of what an opening will carry.

### 2. The instructor slide

Slide 2 states: Professor of Computer Science at Alfaisal University; Director of the RIOTU Lab;
research in mobile robots, drones, deep learning and IoT; author of best-selling online ROS
courses and of the Springer *Robot Operating System* series.

**Verify the affiliation and title lines before first delivery** — they were written from the
legacy PSU-era decks and the current wording has not been confirmed.

## Teaching notes

**Deliver A and B in the same week, in order.** A sets the contract; B is the first real
content. If only one session runs in Week 1, run A — B can compress into Week 2A, but a cohort
that never got the assessment rules will be arguing about them in Week 6.

**W01A, the four video slots.** Play them, then stop. The temptation is to narrate over the
clip; do not. The naming sentence after each one is the teaching, and it lands only in silence
after the clip ends. Total elapsed time should be under four minutes including the sentences.

**W01A, the out-of-scope slide.** Deliver it plainly and without apology. Students who arrived
expecting drones, vision or arms need to know in Week 1, and the slide ends on what they get
instead — one robot that maps a room it has never seen and drives across it. That trade is a
good one and should sound like one.

**W01A, "Two courses you could take."** This is the slide that sets expectations for the
semester, and it is the one to deliver slowly. The cohort arriving from EE 306 expects a
mathematics course. Some of them will be disappointed, and it is better that they find out in
Week 1 than in Week 4 when the first ROS 2 assignment lands.

**W01A, the exam blueprint slide.** State plainly that **40% of every written exam is code on
paper**. Every year, some students assume a software course means the exam is a tutorial recap.
Saying it in Week 1, and again in Week 5, is what prevents that conversation in January.

**W01A, the AI-tool policy.** Do not rush it. The two conditions — disclose, and defend — are
the whole policy, and the "in the field" note is the argument for them: an assistant will
confidently produce ROS 1 code, or code for a distribution three versions old, and it looks
right. Debugging that is a skill this course teaches.

**W01B slide 3, "Which of these is a robot?"** Run it as an activity, not a slide. Ask for
hands, take two disagreements, and let the argument run for three or four minutes before
advancing. The definition on the next slide only lands if the students have already discovered
that they disagree about the elevator and the LLM. If time is short, take just the CNC machine
and the robot vacuum — that pair alone produces the argument.

**W01B, the three hard truths.** These are the load-bearing slides of the lecture. Everything
in Weeks 9–11 exists because of truth 1, and the entire ROS 2 section exists because of truth
3. Deliver the truths, then let the "how do you write one program that does all five, at five
different rates?" question hang for a moment before moving on. The answer should feel earned,
not announced.

**W01B, the naive `while` loop.** Do not present it as a mistake. It is what everyone writes
first, it is correct, and it is readable — and it fails for five *structural* reasons that no
amount of careful coding inside it can fix. Students who are told "that's wrong" learn nothing;
students who are shown why the obvious thing breaks will remember the graph.

**W01B, "A first look at a node."** Read it for shape only. Do not explain `super().__init__`,
QoS, or the executor — Week 2 does all of it. The single point is: *no `while` loop; you
declare what happens on each tick and the framework calls you.*

**Register.** Both decks are written for non-native English speakers: short sentences, no
idiom, every term defined at first use. Keep that register when adapting.

## Before Week 2 — what students must have done

1. Cloned the repository and read `setup/README.md`.
2. Installed the pinned distribution by the route that fits their machine.
3. Run the setup check script — every row `PASS` — and brought the output.
4. Set their assigned `ROS_DOMAIN_ID`.

**Assign the domain IDs in Week 1.** Without them, the Week 2 session is a room in which
everyone's nodes see everyone else's, and nobody understands why. This costs ten minutes to
prevent and half a session to diagnose.

## To be produced for this week

| Item | Status |
|---|---|
| Setup guide + `check_ros2_setup.py`, tested on native / WSL2 / Docker | ❌ **blocks Week 2** |
| Exercise set (no computer): the robot/not-a-robot argument written up, pipeline tracing, the five failures of the naive loop | ❌ |
| `ROS_DOMAIN_ID` assignment list | ❌ |
| Figures for `slides/figures/`, each with the prompt that produced it | ❌ |

## Consistency checks

These decks state figures that must match the approved specification. If any change, update
both decks:

- Assessment weights (W01A) — participation 5, assignments 15, quizzes 5, MT1 15, MT2 15,
  project 20, final 25.
- Exam blueprint (W01A) — recall ≤10%, explain 20%, analyze 30%, read code 20%, write code 20%.
- The four CLOs and their Bloom levels (W01A).
- The 11+4 calendar and every "Week N" cross-reference in W01B (the pipeline map, the sensor
  fusion note, the ecosystem table).
- No bonus marks (W01A).
- Project proposal due Week 5; teams form Week 4.

**The distribution name appears in neither deck as literal text** — both use `\rosver` from the
shared preamble, which is defined once and mirrors `setup/README.md`. Keep it that way.
