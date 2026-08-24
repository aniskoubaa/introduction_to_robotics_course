| **Class Time:** *TBC — see the verification note at the end* | **Class Location:** *TBC — a computer-equipped classroom is requested* |
|---|---|
| **Prerequisite:** EE 306 (Control and Feedback Systems Design) | **Credit hours:** 3 |
| **Co-requisite:** None | **Contact hours:** 3+0+0 |

## Course Instructor/Coordinator Information

| **Instructor Name:** Prof. Anis Koubaa | **Office Location:** *TBC* |
|---|---|
| **Email:** akoubaa@alfaisal.edu | **Office Phone:** *TBC* |
| **Instructor Name:** Dr. Asem Ibrahim Alalwan | **Office Location:** *TBC* |
| **Email:** *TBC* | **Office Phone:** *TBC* |
| **Office Hours:** *TBC — both instructors, or by appointment* | |

## Course Description

This course introduces the foundations of robotics — modelling, control, perception,
localization, mapping and motion planning — and develops them through practical software
implementation using the Robot Operating System 2 (ROS 2). It treats a robot as a system of
concurrent programs that sense the world, estimate their own state within it, decide what to
do, and act, and it builds that system one layer at a time across the semester.

The course is applied throughout. Each week pairs a theory session with a session in which the
same idea is written, run and debugged in ROS 2 on a simulated differential-drive mobile robot.
Students progress from a single publisher node to a complete autonomous system that builds a map
of an unseen room, localizes itself within that map, plans a path to a commanded goal, and
drives there while avoiding obstacles. A team project applies the full stack to a realistic
application, and a dedicated unit on robot ethics and safety addresses the professional
responsibilities that come with deploying autonomous machines around people.

## Course Learning Outcomes (CLOs)

By the end of this course, you will be able to:

- **Explain** robot system architectures and the ROS 2 computation graph. (CLO 1)

- **Analyze** robot kinematics, motion control and state estimation problems. (CLO 2)

- **Develop** ROS 2 software for robot perception, localization and navigation. (CLO 3)

- **Evaluate** ethical and safety implications of autonomous robots within a team. (CLO 4)

## Course Objectives

The objective of this course is to give students a working command of the autonomy pipeline —
perception, estimation, localization, planning and control — and the software engineering
practice needed to implement it. Students develop the mathematical foundations of rigid-body
transformation, differential-drive kinematics, feedback control and probabilistic state
estimation, and they exercise each of them in code on the same robot in the same week the
theory is taught. The course builds on the feedback-control foundation of EE 306 and supplies
what lies between a controller and a working robot: concurrency, coordinate frames, sensor
noise, and the middleware that holds a distributed robot system together. It prepares students
for capstone projects in robotics and for roles in industrial automation, logistics and
inspection robotics.

## Required Textbooks, Tools, or Materials

**Required Textbook:** P. Corke, *Robotics, Vision and Control: Fundamental Algorithms in
Python*, 3rd edition, Springer, 2023.

**Required and examinable:** the official ROS 2 documentation (`docs.ros.org`). This is treated
as a primary source, not a supplement — reading it accurately is a skill this course assesses.

**Supplementary:** A. Kelly, *Mobile Robotics: Mathematics, Models and Methods* (Cambridge,
2013); K. Lynch and F. Park, *Modern Robotics* (Cambridge, 2017); S. Thrun, W. Burgard and
D. Fox, *Probabilistic Robotics* (MIT Press, 2005); R. Siegwart, I. Nourbakhsh and
D. Scaramuzza, *Introduction to Autonomous Mobile Robots*, 2nd ed. (MIT Press, 2011);
F. Martins et al., *A Concise Introduction to Robot Programming with ROS 2* (CRC Press, 2022).

**Software, pinned:** ROS 2 Jazzy Jalisco on Ubuntu 24.04 LTS, Gazebo Harmonic, Python 3.12.
Native, dual-boot, WSL2 or Docker are all supported; no GPU is required. **Installation is due
before Week 2** — see the setup guide in the course repository, which includes a verification
script that must report `PASS` on every row.

**Online resources:** Alfaisal LMS (`elearning.alfaisal.edu`) for announcements, grades and
submissions; the course GitHub repository for slides, starter packages and lab sheets.

**Hardware:** 2–4 TurtleBot3 units are used for hardware validation in the later weeks where
available. The course is fully deliverable in Gazebo simulation; hardware is an enhancement,
not a dependency.

## Instructional Methods

The course runs as **two 1.5-hour sessions each week**. The first is a theory session —
derivation, worked problems and discussion. The second is an in-class ROS 2 session in which
students implement that week's idea on their own machines, guided, with the instructor typing
alongside them and defined checkpoints where the room stops until everyone is together.

Concepts are introduced by deliberate failure wherever possible: students watch the obvious
approach break before the tool that fixes it is named. Reactive obstacle avoidance is made to
fail in a U-shaped trap in Week 6, and that unresolved failure is what makes mapping and
planning in Weeks 10 and 11 answers rather than announcements. Weekly ROS 2 deliverables build
one cumulative workspace across the semester, and a team project applies the whole stack. Every
command shown in class is one the students then run themselves.

## Assessments and Grading Breakdown

Assessment combines five short quizzes and two midterm exams (CLOs 1–2), four graded ROS 2
programming assignments (CLOs 2–3), a comprehensive final exam (CLOs 1, 2, 4), and a team
project with implementation, live demonstration, report, presentation and peer evaluation
(CLOs 3–4).

**Written exams are 40% code.** Every written exam in this course asks students to read ROS 2
code and to write it on paper. This is stated in Week 1 and again in Week 5.

### Assessment Components

| **Assessment Type** | **When** | **Weight** | **CLOs** |
|---|---|---|---|
| Attendance and participation | Across the semester | 5% | — |
| ROS 2 assignments (4 graded, lowest dropped) | Weeks 3, 5, 8, 10 | 15% | 2, 3 |
| Quizzes (5 short, lowest dropped) | Weeks 2, 4, 7, 9, 11 | 5% | 1, 2 |
| Midterm Exam 1 (written) | Week 6 | 15% | 1, 2 |
| Midterm Exam 2 (written) | Week 12 | 15% | 2 |
| Course project (implementation, demo, report, peer evaluation) | Weeks 13–14 | 20% | 3, 4 |
| Final Exam (comprehensive, written) | Final exam week | 25% | 1, 2, 4 |
| **Total Weight** | | **100%** | |

**Project.** Teams of 3. A complete autonomous mobile-robot application in ROS 2 — for example
autonomous warehouse delivery, coverage cleaning, frontier exploration, or LiDAR-based person
following. Deliverables: a Git repository with a history showing all three members working, a
live Gazebo or TurtleBot demonstration, a 6-page technical report, and a 10-minute presentation.
Graded on functionality (40%), software quality and ROS 2 idiom (20%), report (20%),
presentation (10%), and peer/teamwork (10%). Teams form in Week 4; proposals are due in Week 5.

### Grading Scale

This course follows the Alfaisal University undergraduate grading scale:

| **Letter Grade** | A+ | A | B+ | B | C+ | C | D+ | D | F |
|---|---|---|---|---|---|---|---|---|---|
| **Percentage** | 95–100 | 90–94 | 85–89 | 80–84 | 75–79 | 70–74 | 65–69 | 60–64 | 0–59 |

## Course Schedule

This weekly schedule outlines the semester's topics, learning activities, and assessed
assignments. It serves as a working plan and may be adjusted in response to instructional needs
or institutional requirements. Any updates will be communicated promptly through Moodle and your
University email.

| **Week** | **Date** | **Session A — theory** | **Session B — ROS 2 practice** | **Assessment / due** |
|---|---|---|---|---|
| 1 | Aug 23–27 | Introduction to robotics: taxonomy, applications, sense–plan–act; why middleware exists | ROS 2 installation walkthrough; `colcon` workspace | Install ROS 2 and run the setup check **before Week 2** |
| 2 | Aug 30 – Sep 3 | ROS 2 architecture: computation graph, DDS, discovery, QoS; ROS 1 → ROS 2 | Nodes in Python (`rclpy`), CLI tools, `rqt_graph`, launch files | Quiz 1; Assignment 1 assigned |
| 3 | Sep 6–10 | Communication models: publish/subscribe, request/response, goal-oriented | Topics, custom messages, services, parameters, actions | Assignment 1 due |
| 4 | Sep 13–17 | Differential-drive kinematics; pose, velocity, odometry | Open-loop motion: `/cmd_vel`, `/odom`, motion primitives | Quiz 2; **project teams form** |
| 5 | Sep 20–24 | Feedback control for motion: proportional/PID, go-to-goal, stability and tuning | Closed-loop go-to-goal and waypoint following | Assignment 2 assigned; **project proposal due** |
| 6 | Sep 27 – Oct 1 | Sensors and actuators; LiDAR principles, noise and range models | `/scan` processing, wall following, Bug 0 — and watching it fail | **Midterm Exam 1**; Assignment 2 due |
| 7 | Oct 4–8 | Rigid-body transformations: rotation matrices, homogeneous transforms, frames | TF2: broadcasting, listening, static transforms, debugging in RViz2 | Quiz 3 |
| 8 | Oct 11–15 | Robot modelling: links, joints, kinematic chains; simulation fidelity | URDF/Xacro model, Gazebo spawn, sensor plugins | Assignment 3 assigned |
| 9 | Oct 18–22 | Probabilistic state estimation: uncertainty, Bayes filter, Kalman/EKF; sensor fusion | EKF odometry fusion (`robot_localization`); `rosbag2` | Quiz 4; Assignment 3 due |
| 10 | Oct 25–29 | Localization and mapping: occupancy grids, SLAM, AMCL particle filter | `slam_toolbox` map building; AMCL on a saved map | Assignment 4 assigned |
| 11 | Nov 1–5 | Motion planning: configuration space, A*/Dijkstra, global vs. local planners, costmaps | Nav2: behaviour tree, planner and controller servers, autonomous navigation | Quiz 5; Assignment 4 due |
| 12 | Nov 8–12 | Integration: system architecture, launch orchestration, debugging; selected advanced topic | Supervised project work | **Midterm Exam 2** |
| 13 | Nov 15–19 | Robot ethics and safety: safety cases, liability, workforce impact, dual use, licensing | Supervised project work | **Project design review** |
| 14 | Nov 22–26 | Course review and exam preparation | Project finalisation | **Project demonstration, report and presentation** |
| 15 | Nov 29 – Dec 3 | Final examination period | — | **Final Exam** |

> **The dates in this table are derived from a Week 1 start of Sunday 23 August 2026 and have
> not been checked against the official academic calendar.** Verify them, and in particular
> check whether Saudi National Day (23 September) falls inside Week 5 and displaces a session.

## Course and University Policies

### Classroom Behavior Expectations

To provide the best possible learning environment, all students are expected to demonstrate
respect, active participation, and punctuality in the classroom. Late arrivals and frequent
leaves during class disrupt focus and can impact the learning environment for everyone.
Students are expected to arrive on time and stay for the full session.

**Laptops are required in the second session of each week** and are expected to be used for the
ROS 2 work in progress. In the theory session, and during any exam or quiz, electronic devices
are not permitted except with the instructor's permission.

### Attendance Policy

The [Alfaisal University Attendance Policy](https://catalog.alfaisal.edu/class-attendance-policy)
will be followed. Students are expected to attend all scheduled classes as attendance is
mandatory. Students are allowed up to a maximum of 15% absences without valid and documented
excuses. Coming to class 5 minutes after the start of class time will be recorded as an absence.
For medical absences, submit an official medical report through the Student Affairs e-form
within 3 days to be counted as excused. As stated in the university policy, routine or
non-urgent medical appointments are not recorded as excused absences. Students missing 15% or
more of classes without a valid excuse will be denied entry to the final exam and will be issued
a failing grade (DN).

### Late Work and Make-Up Exam Policy

Late work and make-up for missed assignments, quizzes, and midterms will not be allowed except
for reasons deemed acceptable under the University
[Make-up Exams Policy](https://catalog.alfaisal.edu/makeup-exams) and the
[Alfaisal University Attendance Policy](https://catalog.alfaisal.edu/class-attendance-policy).
Students who miss a final exam may only request a make-up in cases of documented medical illness
or serious personal circumstances beyond the student's control. A written request and original
signed documentation must be submitted before the scheduled exam, and all communication must be
by email with the University Registrar copied. If approved, the missed final exam must be
completed as soon as possible after the scheduled exam date, unless it is an extended illness,
in line with the university policy. For non-final exams, students must contact the instructor as
soon as possible before the assessment (with documentation if requested), and any approved
make-up will be scheduled at a reasonable time and location.

### Incomplete Course Policy

Students are expected to complete all course work by the end of the semester. When this is not
possible as a result of illness or other circumstances, an incomplete grade (I) may be
considered as per the [University's Incomplete Course
Policy](https://admissions.alfaisal.edu/ar/storage/app/media/pdf/sa-policies/Incomplete%20Course%20Policy.pdf).
Students must submit a request with documentation to the Office of the Registrar before the last
day of classes and complete all work within four weeks from the last day of exams.

### Academic Honesty Policy

Academic integrity is foundational to your education and the credibility of your degree. Any
form of cheating, plagiarism, collusion, or falsification is strictly prohibited. Academic
misconduct includes but is not limited to: copying on exams or assignments, plagiarism,
submitting AI-generated work without disclosure, unauthorized collaboration, the presence of
unauthorized materials or devices during exams, and falsification of work.

**In a programming course, this needs to be concrete.** Discussing an approach with a classmate
is encouraged. Reading another student's code and typing it in is not, and neither is handing
your code to someone else. Every line you submit must be one you can explain and modify on
request. Team project work is collaborative by design, and the repository history is expected to
show all three members contributing — a history showing one author is itself a finding.

Students who engage in academic misconduct will face serious consequences ranging from a failing
grade (FF) in the course to dismissal from the university. All violations are documented in your
academic record. Refer to the [University's Academic Offences
Policy](https://catalog.alfaisal.edu/academic-offences) for more detail.

### AI Use Policy

Alfaisal University encourages thoughtful exploration of AI technologies while maintaining
academic integrity. In this course, the use of AI tools (e.g. ChatGPT, Claude, GitHub Copilot)
is **permitted with two conditions**:

1. **Disclose it.** State in your submission where you used an AI tool and for what.
2. **Defend it.** You may be asked to explain any line of what you submit, and to modify it on
   the spot. Inability to do so is treated under the Academic Honesty Policy.

Allowed: brainstorming, clarifying concepts, debugging help, and improving the writing of
reports. Not allowed: generating complete assignment or project deliverables, or submitting code
you do not understand. **AI use is strictly prohibited during quizzes, midterm exams, and the
final exam.**

A practical warning specific to this course: AI assistants confidently produce **ROS 1** code, or
code for a ROS 2 distribution several versions old, and it looks correct. Recognising and
debugging that is a skill this course teaches, and it is a good reason to understand what you
submit.

## Accessibility and Disability Services

Students with disabilities, medical conditions (temporary or permanent), or disorders that may
affect their learning should register with the [Counseling and Skills Development Unit
(CSDU)](https://admissions.alfaisal.edu/en/counseling-and-skills-development-unit-csdu) and
submit official medical documentation at the beginning of each semester to access support and
services. Reasonable accommodations, such as extended time on exams or alternative testing
environments, can be arranged to help you succeed while maintaining academic standards. Please
inform your course instructor by the second week of the semester about any accommodations you
need. All accommodation information is handled confidentially.

## Student Support and Resources

At Alfaisal University, your academic success and personal growth are important. The university
offers a wide range of resources to support you throughout your learning journey:

- [Academic Success Center](https://asc.alfaisal.edu/): free subject tutoring, writing support
  and feedback, study skills workshops, time management support, and academic coaching.
- [Alfaisal Library](https://lib.alfaisal.edu/): research assistance, access to academic
  databases and journals, study spaces, and information literacy workshops.
- [Academic Advising](https://admissions.alfaisal.edu/en/academic-advisement): course selection,
  degree planning, academic policies guidance, and registration questions.
- [Counseling and Skills Development Unit
  (CSDU)](https://admissions.alfaisal.edu/en/counseling-and-skills-development-unit-csdu):
  counseling for personal and psychological well-being, disability accommodations, and skills
  development workshops.
- [IT Helpdesk](https://its.alfaisal.edu/it-e-services): technical support for Moodle, email,
  software, and other technology needs.

**Course-specific support:** if your installation fails, or your Linux is weak, say so in Week 1
rather than Week 6. The setup guide includes a primer and a verification script, and nobody has
ever failed this course because of Linux — people fall behind by not saying they were lost in
Week 2.

## Line of Communication

Students should raise course-related issues in the following order: (1) Course
Instructor/Professor; (2) Department Chair, if unresolved within a reasonable time; (3) Vice
Dean for Academic & Student Affairs, if the issue merits escalation; (4) Dean — issues may then
be addressed by the Dean or escalated to the President at the Dean's discretion.

## Disclaimer

The syllabus outlines the course expectations and schedule and may be subject to changes as
needed to enhance the learning experience. Changes will be announced via Moodle and Alfaisal
email. It is the responsibility of each student to ensure the activation of his/her university
e-mail in order to receive course news and announcements. Please check these platforms regularly
and refer to the University Student Handbook for official policies.

---

## Notes for the instructors — remove before publishing to students

The following need filling in or checking before this syllabus is issued:

| Item | Status |
|---|---|
| Class days, time and room | **TBC** |
| Office locations, phone numbers, office hours | **TBC** |
| Dr. Asem Ibrahim Alalwan's email | **TBC** |
| Spelling of Dr. Alalwan's surname | The superseded V2024 specification writes **Alalawan**; this syllabus uses **Alalwan**. Confirm which is right — it appears on every slide deck as well. |
| Week dates | Derived from a Week 1 start of **Sunday 23 August 2026**, not checked against the official academic calendar. Check especially whether **Saudi National Day, 23 September**, falls inside Week 5 and displaces a session. |
| Final exam date | Set by the Registrar; not yet known. |
| Page header | Set in the Word header: course code and title, department, college, term. |
