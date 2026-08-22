# 07 — Exams, Answer Keys and Assessment Rubrics

**Status:** ❌ Not authored.

| Instrument | Week | Covers | Status |
|---|---|---|---|
| Quizzes 1–5 | 2, 4, 7, 9, 11 | The preceding lecture pair | ❌ |
| Assignments 1–4 + rubrics | 3, 5, 8, 10 | ROS 2 implementation | ❌ |
| Midterm Exam I + key | 6 | Weeks 1–5 | ❌ |
| Midterm Exam II + key | 12 | Weeks 6–11 | ❌ |
| Project rubric | — | See `../project/rubric.md` | ❌ |
| Final Exam + key | Exam week | Comprehensive | ❌ |

## Examination design

**Every question maps to exactly one CLO**, so the four outcomes are measured from disjoint
item sets. Record the mapping on the exam source, not afterwards from memory.

A written exam on a software-centric course must still test the software. Proposed blueprint —
confirm before Midterm I and then hold it fixed:

| Section | Demand | Weight |
|---|---|---|
| Recall | Definitions, ROS 2 vocabulary | ≤ 10% |
| Explain | Architecture, why a mechanism exists | 20% |
| Analyze | Kinematics, control, estimation, planning problems worked by hand | 30% |
| Read code | Given a ROS 2 node, state what it does and what it publishes | 20% |
| Write code | Complete a node, a callback, a launch entry, a URDF fragment on paper | 20% |

Standing rule: **the answer key is executed before the exam is printed.** Every code answer
runs on the pinned distribution. A key that has only been read is not a key.

## Assignment rubric shape

Functionality 50 · ROS 2 idiom and package structure 20 · code quality and readability 20 ·
report/demo 10. Late work per the syllabus. Lowest of the four assignments is dropped.

⚠️ Keys are instructor material. Excluded by `.gitignore` if this folder is ever published.
