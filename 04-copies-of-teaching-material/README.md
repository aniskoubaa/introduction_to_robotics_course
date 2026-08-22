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
| 03 | Communication Models in ROS 2 | ❌ | ❌ | ❌ |
| 04 | Differential-Drive Kinematics | ❌ | ❌ | ❌ |
| 05 | Feedback Control for Robot Motion | ❌ | ❌ | ❌ |
| 06 | Sensors, Actuators and LiDAR Perception | ❌ | ❌ | ❌ |
| 07 | Rigid-Body Transformations and TF2 | ❌ | ❌ | ❌ |
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

**1. Exercise sets are generated from one source.** `EE414_WNN_exercises_body.tex` holds the
questions and the answers. `..._exercises.tex` sets `\solutionsfalse`, `..._solutions.tex`
sets `\solutionstrue`. A question and its answer can never drift apart.

**2. Every ROS 2 command in the material has been run.** Not read, not adapted from a
tutorial — executed on the pinned distribution, with the output pasted from the terminal.
ROS 2 tutorials rot between distributions faster than any other material in this course.

**3. Code always wears the terminal window bar.** Every Python listing, terminal session and
traceback renders as a macOS terminal window. It tells a student at a glance that they are
looking at something that runs on a machine rather than at prose about it. Enforced in the
preamble, not by convention. Mathematics and pseudocode use the light box instead.

**4. Every B session ends with something that runs.** A student must leave the room having
seen their own node print, move, or draw in RViz2. Never a half-typed file.

**6. Thirty slides is the ceiling for a 1.5-hour session.** Not a target — a ceiling. The
count includes section-opener slides, because the students sit through those too.

**5. The ROS 2 distribution is named in exactly one place** — `../setup/README.md`. Every
other document refers to it. A distribution upgrade must be a one-line change.

## Critical path

| ID | Artifact | Due |
|---|---|---|
| M1 | `setup/` guide + `check_ros2_setup.py`, tested on Windows/WSL2, macOS/Docker and native Ubuntu | **Before Week 1** |
| M2 | Week 1–3 decks and labs — the ROS 2 on-ramp, where the course is won or lost | Before Week 1 |
| M3 | Shared beamer preamble ✅ / exercise style ❌ | Before Week 1 |
| M4 | `code/` starter workspace with one package per week | Rolling, 2 weeks ahead |
| M5 | Expected-output transcripts for every lab (the automated key) | With each lab |
| M6 | Gazebo world files and the TurtleBot3 simulation setup | Before Week 4 |
| M7 | Project brief, milestones and rubric | Before Week 5 |
| M8 | Ethics case studies for Week 13 | Before Week 13 |
