# EE 414 — Introduction to Robotics

Teaching material for **EE 414 — Introduction to Robotics** (3 credits), a fourth-year
elective in the BSc Electrical Engineering program at **Alfaisal University**, College of
Engineering. Fall 2026.

The course is built around **autonomous mobile robotics**. **ROS 2** is the framework in
which the concepts get implemented — it is the vehicle, not the subject.

---

## What makes this different from the previous offering

The 2024 specification taught robotics as a sequence of mathematical topics with no software,
no platform and no environment named — while its stated objective promised that students would
be "designing, building and programming robots." This redesign closes that gap.

Three commitments run through every artifact here:

**1. Theory on Monday, running code the same hour.** Each 3-hour week is 2 hours of lecture
plus 1 hour of in-class ROS 2 practice. A concept introduced at the board is realised as a
node that runs in Gazebo before the students leave the room. Kinematics is not finished when
the equation is derived; it is finished when the robot drives.

**2. The industrial toolchain, not a teaching toy.** ROS 2, Gazebo, RViz2, `colcon`, TF2,
`slam_toolbox`, Nav2, `rosbag2`. A graduate who has configured Nav2 and debugged a transform
tree has done what a robotics engineer does on their first week of work. A graduate who has
only solved kinematics on paper has not.

**3. Everything is executed before it is written down.** ROS 2 material rots between
distributions faster than any other material in this course. Every command in every deck and
lab sheet has been run on the pinned distribution, and the output is pasted from the terminal.

Assessment follows the same shape: written examinations still test the software — reading a
given node and writing one on paper are 40% of every exam blueprint.

---

## Course at a glance

| | |
|---|---|
| **Credits** | 3 (3-0-0) · 45 contact hours · classroom 100% |
| **Weekly shape** | 2 h lecture + 1 h in-class ROS 2 practice |
| **Structure** | 11 taught weeks + 4 weeks for examination, project and review |
| **Prerequisite** | EE 306 Control and Feedback Systems Design · Python and Linux assumed |
| **Stack** | ROS 2 Jazzy · Ubuntu 24.04 · Gazebo Harmonic · Python 3.12 |
| **Hardware** | Gazebo throughout; 2–4 TurtleBot3 units are an enhancement, not a dependency |
| **Instructor** | Prof. Anis Koubaa — `akoubaa@alfaisal.edu` |

### The four CLOs

| # | Statement | Bloom |
|---|---|---|
| **CLO 1 — EXPLAIN** | Explain robot system architectures and the ROS 2 computation graph. | Understand |
| **CLO 2 — ANALYZE** | Analyze robot kinematics, motion control and state estimation problems. | Analyze |
| **CLO 3 — DEVELOP** | Develop ROS 2 software for robot perception, localization and navigation. | Create |
| **CLO 4 — EVALUATE** | Evaluate ethical and safety implications of autonomous robots within a team. | Evaluate |

Four outcomes, one verb each, ≤ 15 words — recallable without opening the document. All eight
PLOs remain covered.

### Semester plan

| Week | Topic | Assessment |
|---|---|---|
| 1 | Introduction to Robotics and the ROS 2 Ecosystem | — |
| 2 | ROS 2 Architecture and the Computation Graph | Quiz 1 |
| 3 | Communication Models in ROS 2 | Assignment 1 |
| 4 | Differential-Drive Kinematics | Quiz 2 |
| 5 | Feedback Control for Robot Motion | Assignment 2 · **project proposal** |
| 6 | Sensors, Actuators and LiDAR Perception | **Midterm Exam I** |
| 7 | Rigid-Body Transformations and TF2 | Quiz 3 |
| 8 | Robot Modelling: URDF and Simulation | Assignment 3 |
| 9 | Probabilistic State Estimation | Quiz 4 |
| 10 | Localization and Mapping | Assignment 4 |
| 11 | Motion Planning and Autonomous Navigation | Quiz 5 |
| 12 | System Integration and Advanced Topic | **Midterm Exam II** |
| 13 | Robot Ethics, Safety and Professional Practice | Project design review |
| 14 | Review and Project Demonstrations | **Project demo + report** |
| 15 | — | **Final Examination** |

Weeks 12–15 carry no new required material, so a week lost to a holiday or a university event
is absorbed without dropping a topic. Contact hours still total 45.

### Grading

| Component | Weight |
|---|---|
| Attendance and participation | 5% |
| ROS 2 assignments (4, lowest dropped) | 15% |
| Quizzes (5, lowest dropped) | 5% |
| Midterm Exam I | 15% |
| Midterm Exam II | 15% |
| Course project | 20% |
| Final Exam (comprehensive) | 25% |

---

## Repository map

```
introduction_to_robotics_course/
├── 01-course-specification/   ← the approved spec: CLOs, content, assessment design
├── 02-course-syllabus/            institutional syllabus (blocked on approval)
├── 03-combined-course-report/     TP-154, filed after delivery
├── 04-copies-of-teaching-material/ ← THE MAIN BODY OF WORK. week01…week15 + shared/
├── 05…09                          portfolio sections filled during and after delivery
├── 10-additional-documents/       superseded V2024 spec, Council correspondence
├── setup/                     ← START HERE: ROS 2 install, verified before Week 2
├── code/                          the course colcon workspace, one package per week
├── project/                       brief, milestones, templates, rubric
├── readings/                      papers and chapter references, by topic
├── docs/                          notes, analysis, announcements
└── templates/                     blank institutional forms
```

The numbered folders are the Alfaisal **course portfolio** structure — they exist so the
portfolio assembles itself as the semester runs, rather than being reconstructed in
December. `setup/`, `code/`, `project/` and `readings/` are the parts students actually use.

---

## Status

**Scaffold stage.** The course specification is drafted and **pending EE Department Council
approval** — treat it as a draft. No teaching material has been authored yet.

| Section | Status |
|---|---|
| 01 Course specification | ✅ Drafted, pending approval |
| 02 Syllabus | ❌ Blocked on approval |
| 04 Teaching material | ❌ Scaffold only — weeks 01–15 folders with briefs |
| `setup/`, `code/`, `project/` | ❌ Briefs written, artifacts not authored |
| 03, 05–09 | ❌ Filled during and after delivery |

### Critical path

1. `setup/` guide + `check_ros2_setup.py`, tested on all three routes — **before Week 1**.
2. Weeks 1–3 decks and labs — the ROS 2 on-ramp, where the course is won or lost.
3. Shared LaTeX preambles, so 15 weeks of material look like one course.
4. Confirm the computer-equipped classroom and decide the Week 12 advanced topic.

---

## Design precedent

Adapted from **CS460 — Introduction to Mobile Robots**, Prince Sultan University, reduced to a
lighter technical load for a 3-hour fourth-year EE elective: the ROS 1 material, the
manipulation block and the deeper control theory are dropped or compressed into a single
advanced slot in Week 12.

---

## Licence

No licence set — default copyright applies. To reuse or adapt this material, please get in touch.

**Anis Koubaa** — Alfaisal University, College of Engineering.
