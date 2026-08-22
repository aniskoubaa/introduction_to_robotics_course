# Week 07 — Rigid-Body Transformations and TF2

| | |
|---|---|
| **Lecture A (1.5 h)** | Rotation matrices, homogeneous transforms, frame composition; why a robot needs a transform tree |
| **Lecture B (1.5 h) — ROS 2** | TF2: broadcasting, listening, static transforms; reading and debugging the tree in RViz2 |
| **CLO served** | CLO 2, CLO 3 |
| **Assessment this week** | Quiz 3 |
| **Reading** | see `../../readings/topic04_modelling_and_simulation/` |

## Status

| Artifact | Path | Status |
|---|---|---|
| Lecture deck | `slides/EE414_W07_*.tex` / `.pdf` | ❌ not authored |
| Exercise set + key | `exercises/EE414_W07_exercises.pdf` / `_solutions.pdf` | ❌ not authored |
| ROS 2 lab sheet | `ros2_lab/README.md` | ❌ not authored |
| ROS 2 starter package | `../../code/src/` | ❌ not authored |

## Lectures

_Two decks, 1.5 hours each, 30 slides maximum. A deck that runs past 30 slides
is two lectures pretending to be one._

| File | Duration | Contents |
|---|---|---|
| `slides/EE414_W07_....tex` / `.pdf` | 2 h · — slides | — |

Build: `pdflatex <file>.tex` twice. Shared preamble at `../shared/ee414-beamer-preamble.tex`.

## Lecture B — the ROS 2 session

**Goal:** TF2: broadcasting, listening, static transforms; reading and debugging the tree in RViz2

Every B session ends with something that **runs**. Students leave the room having seen
their own node print, move, or draw in RViz2 — never with a half-typed file.

| Item | Status |
|---|---|
| Lab sheet (step-by-step, 1.5 hours, checkpoint at each step) | ❌ |
| Starter package under `code/src/` | ❌ |
| Expected-output transcript (for the key) | ❌ |
| Common-failure list (what breaks, and the fix) | ❌ |

## Teaching notes

_To be written after first delivery._

## Consistency checks

Figures stated in this week's material must match the approved specification:

- Assessment weights — participation 5, assignments 15, quizzes 5, MT1 15, MT2 15, project 20, final 25.
- The four CLOs — EXPLAIN · ANALYZE · DEVELOP · EVALUATE.
- ROS 2 distribution pinned in `../../setup/README.md`. Do not name a version anywhere else.
