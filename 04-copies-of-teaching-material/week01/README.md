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
| Lecture A deck | `slides/EE414_W01A_course_overview.tex` / `.pdf` | ✅ 35 slides, builds clean |
| Lecture B deck | `slides/EE414_W01B_what_is_a_robot.tex` / `.pdf` | ✅ 35 slides, builds clean |
| Shared preamble | `../shared/ee414-beamer-preamble.tex` | ✅ |
| Exercise set + key | `exercises/EE414_W01_exercises.pdf` / `_solutions.pdf` | ❌ not authored |
| Setup guide (M1) | `../../setup/README.md` + `check_ros2_setup.py` | ✅ written; **not yet run on a clean machine** |

## Lectures

| File | Duration | Contents |
|---|---|---|
| `slides/EE414_W01A_course_overview.tex` | 1.5 h · 36 slides | **Who is teaching this**; **four video slots**; what the course is for; the theory-course/this-course contrast; where you end up by Week 11; three reasons robotics is hard; the four CLOs; the weekly A/B shape; the 11+4 calendar; the pipeline-to-weeks map; logistics; the pinned stack; books; **what this course does not cover**; assessment and the exam blueprint; assignments and project; policies; AI-tool policy; setup and `ROS_DOMAIN_ID`; the week's checklist |
| `slides/EE414_W01B_what_is_a_robot.tex` | 1.5 h · 30 slides | Which of these is a robot; sense–plan–act definition; the loop; automation vs autonomy; robot families; why mobile robots; anatomy; the sensor table; the differential drive; the five-block pipeline; "go to the door" traced; three hard truths; the naive `while` loop and its five failures; the computation graph as the answer; ROS 2 honestly; the ecosystem; a first node; `ros2 topic echo` |

Build: `pdflatex <file>.tex` **three times**. `logo.png` must sit beside the `.tex`.

**Known cosmetic issue:** W01B reports one 0.51 pt overfull `\hbox` (0.18 mm) on the
"go to the door" frame. It does not resize with the column widths, so it is not the table.
Below the visual threshold; left alone rather than chased.

## ⚠️ Before delivering — two things to fill in

### 1. The opening images — one still to add

A PDF shows video as a still, so section 1 opens with **three images**, each carrying one
sentence that names what the student is looking at in the course's own vocabulary.

| # | Slide | Figure | Status |
|---|---|---|---|
| 1 | Warehouse robots, at scale | `figures/w01a_warehouse.png` | ✅ generated |
| 2 | Where people should not go | `figures/w01a_inspection.png` | ✅ generated |
| 3 | A robot changing its mind | `figures/w01a_replanning.png` | ✅ generated |
| 4 | **Built here** | `figures/w01a_riotu.jpg` | ❌ **needs a real photo from you** |

> ⚠️ **Slot 4 is commented out in the `.tex` on purpose.** It is a claim about your own lab's
> work, and an AI-generated image presented as RIOTU research would be a fabrication shown to
> students. Drop a real photograph into `figures/w01a_riotu.jpg` and uncomment the block at the
> end of section 1.

**Optional:** if the room's network is reliable you can also play a clip from a browser between
slides. Keep the URLs here, never on a slide — a dead link projected in front of a class is
worse than no link.

| # | Clip to find | URL |
|---|---|---|
| 1 | An AMR fleet moving stock in a live warehouse | ❌ |
| 2 | A robot inspecting an industrial plant | ❌ |
| 3 | A Nav2 robot re-planning around a person — **literally Week 11** | ❌ |
| 4 | RIOTU Lab robots and drones | ❌ |

#### Regenerating a figure

Figures 1–3 were generated with Gemini 3 Pro Image. Each keeps its prompt beside it, so the
whole set can be restyled consistently:

```bash
cd ../shared
python3 gen_figure.py ../week01/slides/figures/w01a_warehouse.png \
                      ../week01/slides/figures/w01a_warehouse.prompt.txt
```

`gen_figure.py` appends the house style (palette, no text, no logos, no identifiable people,
16:9) to every prompt, which is what keeps fifteen weeks of illustrations looking like one
course. Needs `GEMINI_API_KEY`.

### 2. The instructor slide — two instructors, one of them incomplete

The course is taught by **Prof. Anis Koubaa and Dr. Asem Ibrahim Alalwan**, and both names now
appear on every deck's title page and in every footline.

> ⚠️ **Slide 2 carries a `VERIFY BEFORE DELIVERY` line and the "Practical information" slide
> carries `email: VERIFY`.** Dr. Asem Ibrahim Alalwan's title, department, email and one line of
> subject expertise were **not** supplied and have deliberately not been invented — writing a
> colleague's credentials from guesswork and projecting them to a class is not a defensible
> thing to do. Fill both in, or cut the placeholder bullets, before first delivery.

Anis Koubaa's lines were written from the legacy PSU-era decks: Professor of Computer Science
at Alfaisal University; Director of the RIOTU Lab; research in mobile robots, drones, deep
learning and IoT; author of best-selling online ROS courses and of the Springer *Robot
Operating System* series. **Confirm the current wording** before first delivery.

## What changed in the August 2026 revision (W01B)

Five concepts were re-sequenced so the concrete case comes before the structure. Nothing was
cut; five slides were added. The pattern, which is the reusable part:

> **1.** a situation they can picture · **2.** a question they attempt · **3.** the number that
> proves their answer fails · **4.** the name of the thing that fixes it

Beat 3 was what the deck was missing everywhere — it asserted that robotics is hard instead of
quantifying it.

| Was | Now |
|---|---|
| Five pipeline boxes, then "go to the door" traced through them | **"You are the robot. Go to the door."** → five questions the room answers → the same five boxes, as their answer → the traced version with real numbers |
| Truth 1 opened on `x = 4.2 ± 0.3` | Opens on **walk ten steps with your eyes shut**, then 2 % wheel slip over 50 m = 1 m of error |
| Truth 2 showed a delay chain and never added it up | **175 ms → 4 cm of travel after deciding to stop**, and ×10 for a warehouse AMR |
| The naive loop, then five reasons it fails | **A stopwatch on the loop first**: 320 ms → 3 Hz → 7 cm blind between control decisions, half the robot's length |
| $v, \omega$ introduced in a display equation between bullets | **A wheelchair is a differential drive** — hands on rims, three motions — then the symbols |

The pipeline diagram now carries **week numbers** (Perception W6, Estimation W9, Localization
W10, Planning W11, Control W4–5). It and W01A's "Where you end up" are the same object, and the
labels are what turn it from a taxonomy into the map the semester hangs off.

**Numbers used, and where they must stay consistent:** 0.22 m/s is the course's driving speed
and also `max_speed` in W02A. The controller is designed for **20 Hz** — the value in Truth 3's
rate table — and the naive loop drops it to 3 Hz. `plan()` is 200 ms in both the code listing
and the stopwatch table. If any of these change, they change in all of those places.

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

**W01B, "You are the robot. Go to the door."** Do not answer it. Let the room shout, write
their answers on the board in the order they arrive, and only then advance. The five questions
on the next slide should read as *their* list tidied up, not as yours revealed. If the room is
silent, prompt with the narrowest possible question — *the LiDAR just gave you 360 numbers; is
that where you are?* — and the rest follows.

**W01B, "Do this now, with your eyes shut."** Actually make them stand up and do it. Ten
seconds of a room walking into each other buys you the entire probabilistic half of the course,
because from then on "the robot does not know where it is" is something they have felt rather
than something you claimed.

**W01B, "Put a stopwatch on it."** Compute it in front of them; do not present the total. Ask
for the sum, then ask what 3 Hz means at 0.22 m/s, and let somebody in the room produce the
7 cm. A number the class derived is worth five they were shown.

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
| Setup guide + `check_ros2_setup.py` | ✅ written · ❌ **still untested on a clean machine** |
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
