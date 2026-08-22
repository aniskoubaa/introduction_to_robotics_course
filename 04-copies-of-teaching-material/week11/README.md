# Week 11 — Motion Planning and Autonomous Navigation

| | |
|---|---|
| **Lecture A (1.5 h)** | Configuration space; Dijkstra and A\*; global vs. local planners; costmaps and recovery behaviours |
| **Lecture B (1.5 h) — ROS 2** | The **Nav2** stack: behaviour tree, planner and controller servers; autonomous point-to-point navigation |
| **CLO served** | CLO 2, CLO 3 |
| **Assessment this week** | Quiz 5 |
| **Reading** | see `../../readings/topic06_planning_and_navigation/` |

## Status

| Artifact | Path | Status |
|---|---|---|
| Lecture deck | `slides/EE414_W11_*.tex` / `.pdf` | ❌ not authored |
| Exercise set + key | `exercises/EE414_W11_exercises.pdf` / `_solutions.pdf` | ❌ not authored |
| ROS 2 lab sheet | `ros2_lab/README.md` | ❌ not authored |
| ROS 2 starter package | `../../code/src/` | ❌ not authored |

## Lectures

_Two decks, 1.5 hours each, 30 slides maximum. A deck that runs past 30 slides
is two lectures pretending to be one._

| File | Duration | Contents |
|---|---|---|
| `slides/EE414_W11_....tex` / `.pdf` | 2 h · — slides | — |

Build: `pdflatex <file>.tex` twice. Shared preamble at `../shared/ee414-beamer-preamble.tex`.

## Lecture B — the ROS 2 session

**Goal:** The **Nav2** stack: behaviour tree, planner and controller servers; autonomous point-to-point navigation

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
