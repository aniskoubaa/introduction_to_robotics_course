# Week 06 — Sensors, Actuators and LiDAR Perception

| | |
|---|---|
| **Lecture A (1.5 h)** | Robot sensor and actuator taxonomy; LiDAR operating principle, range and angular resolution, noise models |
| **Lecture B (1.5 h) — ROS 2** | Processing `/scan`; reactive obstacle avoidance; wall following |
| **CLO served** | CLO 2, CLO 3 |
| **Assessment this week** | **Midterm Exam I** (Weeks 1–5) |
| **Reading** | see `../../readings/topic03_perception/` |

## Status

| Artifact | Path | Status |
|---|---|---|
| Lecture deck | `slides/EE414_W06_*.tex` / `.pdf` | ❌ not authored |
| Exercise set + key | `exercises/EE414_W06_exercises.pdf` / `_solutions.pdf` | ❌ not authored |
| ROS 2 lab sheet | `ros2_lab/README.md` | ❌ not authored |
| ROS 2 starter package | `../../code/src/` | ❌ not authored |

## Lectures

_Two decks, 1.5 hours each, 30 slides maximum. A deck that runs past 30 slides
is two lectures pretending to be one._

| File | Duration | Contents |
|---|---|---|
| `slides/EE414_W06_....tex` / `.pdf` | 2 h · — slides | — |

Build: `pdflatex <file>.tex` twice. Shared preamble at `../shared/ee414-beamer-preamble.tex`.

## Lecture B — the ROS 2 session

**Goal:** Processing `/scan`; reactive obstacle avoidance; wall following

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
