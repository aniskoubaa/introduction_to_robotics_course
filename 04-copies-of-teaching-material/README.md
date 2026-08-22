# 04 — Copies of Teaching Material

**Status:** ⚠️ Scaffold only. This is the whole authoring effort.

Per-week folders `week01` … `week15`, plus `shared/`. Each week folder carries its own
`README.md` with the lecture topic, the practice-hour goal, the CLO served, an artifact
status table, teaching notes and consistency checks.

Two decks per week, **30 slides maximum each**. A deck that runs past 30 slides is two
lectures pretending to be one.

| Week | Topic | Lecture A | Lecture B | Exercises |
|---|---|---|---|---|
| 01 | Introduction to Robotics and the ROS 2 Ecosystem | ✅ Course Overview (30 sl.) | ✅ What Is a Robot? (30 sl.) | ❌ |
| 02 | ROS 2 Architecture and the Computation Graph | ✅ Computation Graph (24 sl.) | ✅ Your First Nodes (26 sl.) | ❌ |
| 03 | Communication Models in ROS 2 | ✅ Communication Models (25 sl.) | ✅ Your Own Interfaces (25 sl.) | ❌ |
| 04 | Differential-Drive Kinematics | ❌ | ❌ | ❌ |
| 05 | Feedback Control for Robot Motion | ❌ | ❌ | ❌ |
| 06 | Sensors, Actuators and LiDAR Perception | ❌ | ❌ | ❌ |
| 07 | Rigid-Body Transformations and TF2 | ✅ Transformations (21 sl.) | ✅ TF2 in Practice (21 sl.) | ❌ |
| 08 | Robot Modelling: URDF and Simulation | ❌ | ❌ | ❌ |
| 09 | Probabilistic State Estimation | ❌ | ❌ | ❌ |
| 10 | Localization and Mapping | ❌ | ❌ | ❌ |
| 11 | Motion Planning and Autonomous Navigation | ❌ | ❌ | ❌ |
| 12 | System Integration and Advanced Topic | ❌ | ❌ | — |
| 13 | Robot Ethics, Safety and Professional Practice | ❌ | ❌ | — |
| 14 | Review and Project Demonstrations | ❌ | — | — |
| 15 | Final Examination Week | — | — | — |

## Layout

```
shared/            ee414-beamer-preamble.tex, ee414-exercise-style.tex, figure prompts
weekNN/
├── README.md      teaching notes, status, consistency checks
├── slides/        EE414_WNN_<topic>.tex + .pdf, figures/
├── exercises/     one source holding questions AND answers; two thin wrappers
└── ros2_lab/      lab sheet, expected-output transcript, common-failure list
```

## Standing rules

Operative plan: `../../docs/2026-08-22-2230-deck-redesign-plan.md`.

### Format

**1. Exercise sets are generated from one source.** `EE414_WNN_exercises_body.tex` holds the
questions and the answers. `..._exercises.tex` sets `\solutionsfalse`, `..._solutions.tex`
sets `\solutionstrue`. A question and its answer can never drift apart.

**2. Every ROS 2 command in the material has been run.** Not read, not adapted from a
tutorial — executed on the pinned distribution, with the output pasted from the terminal.

**3. Code always wears the terminal window bar.** Enforced in the preamble, not by convention.
Mathematics and pseudocode use the light box instead.

**4. No slide body exceeds 25 words.** Section dividers and code slides are exempt. A
1.5-hour session runs **40–60 slides**. Slide count is not a quality signal; words per slide
is. Everything cut goes into `\note{}` and compiles to a separate notes PDF.

**5. Code is revealed one line per slide**, the new line highlighted (`\codestep`). **A command
is revealed one token per slide** (`\cmdanatomy`): the whole line stays put, every token but one
fades to near-invisible, and one caption hangs below the live token. Any command whose tokens a
first-year student cannot name gets this treatment — which in practice means the first time each
`ros2` verb appears.

**6. Real screenshots, not typeset listings**, wherever a student will compare against their
own screen. A screenshot is the artifact of having run it — rule 2, discharged. Illustrations
may be generated (`shared/gen_figure.py`) and each keeps its prompt beside it; **but nothing
generated may make a factual claim about a real person, place or piece of work.**

**7. The ROS 2 distribution is named in exactly one place** — `../setup/README.md` — and
reached everywhere else through `\rosver`.

**7a. Every deck builds with THREE `pdflatex` passes.** The section divider and `\fullslide`
position with `remember picture,overlay`, whose page anchors come from the `.aux`. After two
passes a divider is a dark rectangle with no text on it, and the build reports no error —
so this is a rule, not a preference.

**7b. Borrowed artwork carries its source on the slide, in small type, every time it is
shown** (`\figslide`, fourth argument). Not a courtesy. The students are being taught to
attribute; a deck that quietly reuses a book's figures teaches the opposite of what the Week 1
AI-tool policy asks of them.

### Flow

**8. Every week opens with the previous week's solution failing.** The escalating problem
statement is the spine of the course: *go to the goal* → *…without hitting anything* → *…in a
building you have never seen*. Nothing is introduced before the student has watched the
previous thing break.

**9. Every mathematical topic gets one everyday analogy** before the formalism.

**10. Every major concept closes with a numbered procedure** (`\procedure`) — *how to decide*,
not just how it works.

**11. Every B session is demo-first**: see it run, explore it from the CLI, then build it. And
every B session ends with something that **runs** — never a half-typed file.

**12. Why-first for tools; pain-first for mathematics.** Never answer "why X" before the
student has felt the problem X solves. You cannot want quaternions until Euler angles have hurt
you.

> ✅ **Week 2 was rebuilt against these rules on 22 August 2026** — workspaces moved from A to
> B, B restructured demo-first on turtlesim, `\cmdanatomy` introduced, and the four
> communication mechanisms given a figure each. It is the worked example of rules 5, 7b and 11.
> See `week02/README.md`, "What changed in the August 2026 revision".

> ⚠️ **Rules 4–6 and 8–12 postdate the Weeks 1, 3 and 7 decks.** Those eight decks carry a median
> of 57–96 words per slide against 12–20 in the legacy ROS course they are modelled on, and
> W07A introduces rotation before translation. They are **dense, not wrong** — deliverable as
> they stand, and scheduled for retrofit *after* the unwritten weeks are authored natively in
> the new format. See the plan, §6. Week 2 has now been done; the density rule (4) is still
> **not** satisfied even there — its slides are shorter than they were, but the prose slides
> still run past 25 words. That is the remaining work, and it needs `\note{}` first.

## Critical path

Superseded by `../../docs/2026-08-22-2230-deck-redesign-plan.md`. In short:

| Horizon | Work |
|---|---|
| **Tonight** | `setup/` guide + `check_ros2_setup.py`; `ROS_DOMAIN_ID` assignment; three video slots + an out-of-scope slide + an instructor slide inserted into W01A |
| **This week** | `\note{}` + notes-PDF target; the five macros (`\bigq`, `\codestep`, `\triptych`, `\pathmap`, `\procedure`); **rewrite W01B as the format pilot**; screenshot pipeline |
| **Rolling** | Two weeks ahead, natively in the new format, ~18 h per week of material |
| **Deferred** | Retrofit W02, W03, W01 — **except W07A, which is resequenced before Week 7 delivers** |
