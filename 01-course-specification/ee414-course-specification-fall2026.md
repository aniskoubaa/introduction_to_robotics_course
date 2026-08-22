# EE 414 — Introduction to Robotics
## Proposed Course Specification (ROS 2–Centred Redesign), V2026

**Program:** Bachelor of Electrical Engineering · **Department:** Electrical Engineering
**College:** College of Engineering · **Institution:** Alfaisal University
**Prepared by:** Prof. Anis Koubaa · **Date:** 22 August 2026
**Supersedes:** EE 414 Course Specification V2024 (Dr. Asem Ibrahim Alalawan)

> **Design principle.** Robotics is taught *through* ROS 2 (Jazzy/Humble). Every theoretical
> concept — kinematics, control, perception, transformations, localization, planning — is
> introduced in the lecture and immediately realised as running ROS 2 code in Gazebo/TurtleBot.
> Model adapted from CS460 *Introduction to Mobile Robots* (Prince Sultan University), reduced
> to a lighter 11-week technical load plus 4 weeks for assessment, practice and project.

---

## A. General Information About the Course

### 1. Credit Hours

**3 (3-0-0)** — 45 contact hours over 15 weeks, per the standard Alfaisal EE structure.

Each 3-hour week is delivered as **2 hours of lecture + 1 hour of in-class ROS 2 practice**,
conducted in a computer-equipped classroom (or on student laptops). The practice hour remains
formally part of the lecture allocation; no separate laboratory credit is claimed.

### 2. Course Type

Department course · **Elective** · Offered in the **Fourth Year**.

### 3. Course General Description

This course introduces the foundations of robotics — modelling, control, perception,
localization, mapping and motion planning — and develops them through practical software
implementation using the **Robot Operating System 2 (ROS 2)**. Students learn the ROS 2
computation graph, build robot software packages in Python, model robots in URDF, simulate
them in Gazebo, and implement closed-loop motion, obstacle avoidance, state estimation and
autonomous navigation. The course closes with an integrative team project in which students
design, program and demonstrate a complete autonomous mobile-robot behaviour.

### 4. Pre-requisites

EE 306 — Control and Feedback Systems Design.
*Assumed background:* Python programming and Linux command-line familiarity. A self-paced
Linux/Python primer is provided in Week 0 for students who need it.

### 5. Co-requisites

None.

### 6. Course Main Objectives

1. Give students a rigorous understanding of the mathematical foundations of mobile robotics
   (rigid-body transformations, differential-drive kinematics, feedback control, Bayesian state
   estimation, path planning).
2. Give students professional competence in **ROS 2**, the de-facto industrial and research
   middleware for robotics — nodes, topics, services, actions, parameters, TF2, URDF, Gazebo,
   and the Nav2 navigation stack.
3. Enable students to move from a specification to a working, tested autonomous robot behaviour,
   validated in simulation and, where hardware permits, on a physical TurtleBot platform.
4. Develop the professional skills of teamwork, technical communication and responsible
   engineering practice in the context of autonomous systems.

### 7. Teaching Mode

| No | Mode of instruction | Contact hours | Percentage |
|---|---|---|---|
| 1 | Traditional classroom | 45 | 100% |
| 2 | E-learning | — | — |
| 3 | Hybrid | — | — |
| 4 | Distance learning | — | — |

*LMS support (recorded ROS 2 walkthroughs, course code repository, auto-graded exercises)
supplements the classroom but carries no separate contact-hour allocation.*

### 8. Contact Hours

| No | Activity | Contact hours |
|---|---|---|
| 1 | Lectures | 45 |
| 2 | Laboratory / Studio | 0 |
| 3 | Field | 0 |
| 4 | Tutorial | 0 |
| 5 | Others | 0 |
| **Total** | | **45** |

---

## B. Course Learning Outcomes (CLOs), Teaching Strategies and Assessment Methods

Four CLOs, each Bloom-anchored, measurable, and short enough to be memorised by students and staff.

| Code | Course Learning Outcome | Bloom level | Aligned PLO (SO) | Teaching Strategies | Assessment Methods |
|---|---|---|---|---|---|
| **1.0** | **Knowledge and Understanding** | | | | |
| **CLO 1** | **Explain** robot system architectures and the ROS 2 computation graph. | Understand (L2) | PLO 1 (SO 8) — Knowledge base<br>PLO 3 (SO 7) — Lifelong learning | Lecture, guided reading of official ROS 2 documentation, live demonstrations | Quizzes, Midterm I, Final exam |
| **2.0** | **Skills** | | | | |
| **CLO 2** | **Analyze** robot kinematics, motion control and state estimation problems. | Analyze (L4) | PLO 2 (SO 1) — Problem solving | Interactive lecture, in-class problem solving, posted solution files, office hours | Assignments, Quizzes, Midterm I & II, Final exam |
| **CLO 3** | **Develop** ROS 2 software for robot perception, localization and navigation. | Create (L6) | PLO 4 (SO 2) — Creativity and design<br>PLO 5 (SO 6) — Use of engineering tools | Hands-on ROS 2 practice, design discussion, code walkthroughs, simulation experiments | Weekly ROS 2 deliverables, Project, Design exercise |
| **3.0** | **Values, Autonomy and Responsibility** | | | | |
| **CLO 4** | **Evaluate** ethical and safety implications of autonomous robots within a team. | Evaluate (L5) | PLO 6 (SO 3) — Communication and ICT<br>PLO 7 (SO 4) — Values and ethics<br>PLO 8 (SO 5) — Autonomy and responsibility | Case-study discussion, readings, team project with defined roles, presentation rubric | Project report, Project presentation, Peer evaluation, Final exam question |

*Not all SO attainment results need to be reported in the PLO attainment sheet — only the
mappings selected in the Program Specification.*

---

## C. Course Content — 11 Technical Weeks + 4 Assessment/Project Weeks

### C.1 Weekly Plan (3 hours per week: 2 h lecture + 1 h in-class ROS 2 practice)

| Week | Lecture topic (theory) | In-class ROS 2 practice | CLO | Assessment |
|---|---|---|---|---|
| **1** | Introduction to robotics: taxonomy, applications, sense–plan–act; why middleware exists | Ubuntu + ROS 2 installation, `colcon` workspace, first package | 1 | — |
| **2** | ROS 2 architecture: computation graph, DDS, discovery, QoS; ROS 1 → ROS 2 rationale | Nodes in Python (`rclpy`), CLI tools, `rqt_graph`, launch files | 1 | Quiz 1 |
| **3** | Communication models: publish/subscribe, request/response, goal-oriented | Topics and custom messages; services; parameters; actions | 1, 3 | Assignment 1 |
| **4** | Differential-drive kinematics; pose, velocity, odometry | Open-loop motion: `/cmd_vel`, `/odom`, straight-line and rotation primitives | 2, 3 | Quiz 2 |
| **5** | Feedback control for motion: proportional/PID, go-to-goal, stability and tuning | Closed-loop go-to-goal and waypoint-following controller | 2, 3 | Assignment 2 |
| **6** | Sensors and actuators; LiDAR principles, noise and range models | `/scan` processing, reactive obstacle avoidance, wall following | 2, 3 | **Midterm Exam I** |
| **7** | Rigid-body transformations: rotation matrices, homogeneous transforms, frames | TF2: broadcasting, listening, static transforms, debugging the tree in RViz2 | 2, 3 | Quiz 3 |
| **8** | Robot modelling: links, joints, kinematic chains; simulation fidelity | URDF/Xacro model, Gazebo spawn, sensor plugins, RViz2 visualisation | 1, 3 | Assignment 3 |
| **9** | Probabilistic state estimation: uncertainty, Bayes filter, Kalman/EKF; sensor fusion | EKF odometry fusion (`robot_localization`); `rosbag2` capture and replay | 2, 3 | Quiz 4 |
| **10** | Localization and mapping: occupancy grids, SLAM, AMCL particle filter | `slam_toolbox` map building; AMCL localization on a saved map | 2, 3 | Assignment 4 |
| **11** | Motion planning and navigation: configuration space, A*/Dijkstra, global vs. local planners, costmaps | **Nav2**: behaviour tree, planner/controller servers, autonomous point-to-point navigation | 2, 3 | Quiz 5 |
| **12** | Integration: system architecture, launch orchestration, debugging; **selected advanced topic** (manipulation with MoveIt 2, *or* learning-based control / VLA models) | Supervised project work | 3 | **Midterm Exam II** |
| **13** | Robot ethics and safety: safety cases, liability, workforce impact, dual use, open-source licensing | Supervised project work | 4 | Project design review |
| **14** | Course review and exam preparation | Project finalisation | 3, 4 | **Project demonstration + report** |
| **15** | — | — | 1–4 | **Final Examination** |

### C.2 Contact Hours by Topic

| No | Topic | Contact hours |
|---|---|---|
| 1 | Introduction to robotics and ROS 2 architecture | 9 |
| 2 | Robot kinematics and motion modelling | 3 |
| 3 | Feedback control for robot motion | 3 |
| 4 | Sensors, perception and obstacle avoidance | 3 |
| 5 | Transformations, TF2, URDF and simulation | 6 |
| 6 | State estimation, localization and mapping | 6 |
| 7 | Motion planning and autonomous navigation (Nav2) | 3 |
| 8 | Advanced topic (manipulation / learning-based control) | 3 |
| 9 | Robot ethics, safety and professional practice | 3 |
| 10 | Integration, project supervision and review | 6 |
| **Total** | | **45** |

---

## D. Student Assessment Activities

| No | Assessment activity | Timing (week) | % of total | CLO |
|---|---|---|---|---|
| 1 | Attendance and participation | Across the semester | 5% | — |
| 2 | ROS 2 assignments (4 graded, lowest dropped) | Weeks 3, 5, 8, 10 | 15% | 2, 3 |
| 3 | Quizzes (5 short, lowest dropped) | Weeks 2, 4, 7, 9, 11 | 5% | 1, 2 |
| 4 | Midterm Exam I (written) | Week 6 | 15% | 1, 2 |
| 5 | Midterm Exam II (written) | Week 12 | 15% | 2 |
| 6 | Course project — implementation, demonstration, report, peer evaluation | Weeks 13–14 | 20% | 3, 4 |
| 7 | Final Examination (comprehensive, written) | Final exam week | 25% | 1, 2, 4 |
| | **Total** | | **100%** | |

**Project.** Teams of 3. A complete autonomous mobile-robot application in ROS 2 — for example
autonomous warehouse delivery, coverage/cleaning, frontier exploration, or LiDAR-based
person following. Deliverables: a Git repository, a live Gazebo (or TurtleBot hardware) demo,
a 6-page technical report, and a 10-minute presentation. Graded on functionality (40%),
software quality and ROS 2 idiom (20%), report (20%), presentation (10%), peer/teamwork (10%).

---

## E. Learning Resources and Facilities

### 1. References and Learning Resources

| | |
|---|---|
| **Essential References** | 1. P. Corke, *Robotics, Vision and Control: Fundamental Algorithms in Python*, 3rd ed., Springer, 2023.<br>2. **Official ROS 2 documentation** (Jazzy/Humble) — `docs.ros.org` — treated as a primary, examinable resource. |
| **Supportive References** | • A. Kelly, *Mobile Robotics: Mathematics, Models and Methods*, Cambridge, 2013.<br>• K. Lynch and F. Park, *Modern Robotics*, Cambridge University Press, 2017.<br>• S. Thrun, W. Burgard, D. Fox, *Probabilistic Robotics*, MIT Press, 2005.<br>• R. Siegwart, I. Nourbakhsh, D. Scaramuzza, *Introduction to Autonomous Mobile Robots*, 2nd ed., MIT Press, 2011.<br>• N. Correll, B. Hayes, C. Heckman, A. Roncone, *Introduction to Autonomous Robots*, MIT Press, 2022.<br>• F. Martins et al., *A Concise Introduction to Robot Programming with ROS 2*, CRC Press, 2022. |
| **Electronic Materials** | Alfaisal LMS (`elearning.alfaisal.edu/coe/`); course GitHub organisation with all starter packages and solutions; recorded ROS 2 walkthroughs. |
| **Other Learning Materials** | Instructor lecture notes and slide decks; Nav2 and `slam_toolbox` tutorials; TurtleBot3 e-Manual. |

### 2. Required Facilities and Equipment

| Item | Resource |
|---|---|
| **Facilities** | Classrooms are standardized in quality and efficiency. A **computer-equipped classroom** is requested for this course so the weekly ROS 2 practice hour can run in place. |
| **Technology equipment** | Smartboard, podium, data show, internet-connected computer. Machines running Ubuntu 24.04 (native, dual-boot, WSL2 or Docker) with ROS 2, Gazebo and RViz2 pre-installed; no GPU required. LMS access for attendance and grading. |
| **Other equipment** | **2–4 TurtleBot3 Burger/Waffle units (or an equivalent differential-drive platform with 2D LiDAR)** for hardware validation in Weeks 10–14. *If hardware is unavailable, the course is fully deliverable in Gazebo simulation; hardware is an enhancement, not a dependency.* |

---

## F. Assessment of Course Quality

| Assessment area | Assessor | Method |
|---|---|---|
| Effectiveness of teaching | Students | CES (indirect) |
| Effectiveness of student assessment | Faculty / Peer reviewer | Direct — exam and rubric review |
| Quality of learning resources | Students | CES (indirect) |
| Extent to which CLOs have been achieved | Faculty | FCAR (direct) |
| Currency of the ROS 2 technology stack | Course coordinator | Annual review against the current ROS 2 LTS distribution |

---

## G. Specification Approval

| | |
|---|---|
| **Council / Committee** | EE Department Council |
| **Reference No.** | |
| **Date** | |
| **Prepared by** | Prof. Anis Koubaa |
| **Date** | 22 August 2026 |

---

## Annex — What Changed Relative to V2024

| # | V2024 issue | Resolution in this proposal |
|---|---|---|
| 1 | Nine CLO rows, five of them with PLO mappings, teaching strategies and assessments but **no outcome statement** | Reduced to **four** Bloom-anchored CLOs (Understand / Analyze / Create / Evaluate), each measurable and short enough to memorise; all eight PLOs still covered |
| 2 | CLO 1.1 assessed by "Forum Postings / Role-Playing" — not credible evidence for a modelling and control outcome | Knowledge and analysis CLOs assessed by quizzes, midterms and final exam; design CLO by ROS 2 deliverables and project; values CLO by report, presentation and peer evaluation |
| 3 | Objective promised "designing, building and programming robots" with no software, tooling or platform identified | ROS 2, Gazebo, RViz2, `colcon`, TF2, `slam_toolbox`, Nav2 and `rosbag2` named explicitly and exercised weekly; credit structure kept at the standard **3 (3-0-0)**, with 1 of the 3 weekly hours run as in-class ROS 2 practice |
| 4 | Content gaps: no forward kinematics, no sensors, no transformations; topic 2 listed inverse kinematics only | Added rigid-body transformations and TF2, URDF modelling and simulation, sensors and actuators, LiDAR perception |
| 5 | No coverage of ethics, safety or professional responsibility despite PLO 7 / PLO 8 mappings | Week 13 dedicated to robot ethics, safety cases and open-source licensing; assessed under CLO 4 |
| 6 | Content week count not aligned to the academic calendar | Explicit 11 technical weeks + 4 weeks for exam, project and review |
| 7 | Essential reference (Kelly) is a mathematics monograph, difficult for a first robotics course | Corke (Python edition) promoted to essential, with the official ROS 2 documentation as a co-primary source; Kelly retained as supportive |
