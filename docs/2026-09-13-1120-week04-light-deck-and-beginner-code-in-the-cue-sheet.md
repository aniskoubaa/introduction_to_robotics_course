# Week 4 — a fifteen-slide light deck, and the beginner code in the cue sheet

**2026-09-13 11:20 UTC.** Two requests, both for the hands-on session:

> "I want 15 slides that present all concepts quickly before I go to hands-on.
> keep initial version and make light version"

and, on the cue sheet, the beginner code beside the full code.

## The light deck

`week04/slides/EE414_W04A_light.tex` → `.pdf`, 16 pages: a title page and
fifteen content slides. `EE414_W04A_differential_drive.tex` (40 slides) is
unchanged.

It is **not** a subset of the big deck's frames. Fifteen frames copied out of
forty would teach fifteen concepts and silently drop twenty-five. Instead every
concept in Deck A appears here, reduced to one claim and one piece of evidence:

| | Slide |
|---|---|
| 1 | Pose in the Plane |
| 2 | Two Representations of Orientation |
| 3 | Velocity and the Twist Message |
| 4 | The Nonholonomic Constraint |
| 5 | The Differential-Drive Robot |
| 6 | Forward Kinematics: Wheels to Body |
| 7 | The Instantaneous Centre and the Turning Radius |
| 8 | Inverse Kinematics and Actuator Saturation |
| 9 | From Velocity to Position: Integration |
| 10 | Wheel Odometry and Its Error Sources |
| 11 | Angle Normalisation |
| 12 | Open-Loop Motion Control |
| 13 | The Open-Loop Square |
| 14 | Closed-Loop Motion Control: Preview of Week 5 |
| 15 | Laboratory Session |

It uses the shared preamble, so the palette, the terminal-window code boxes and
the block colours are the ones the rest of the course uses. It declares **no
`\section`**: `\AtBeginSection` would insert an Outline frame for each one and
the deck would no longer be fifteen slides.

The code boxes quote the **beginner scripts** — the same files the students run
in the lab — so the projected slide and their terminal agree.

Every number on the slides came from a run on this machine: the four
`simple_kinematics` cases, the 2.016 m that `simple_move` travels when
commanded 2.000 m, and the 0.185 m closing error of `simple_square`.

### Two corrections made during the work

**Slide titles.** The first version used conversational titles ("The bug that
will bite you today: angles wrap"). They were replaced with formal Title Case
noun phrases matching the existing decks. The frame numbering was dropped; the
footer already carries the page number.

**Language.** The prose was rewritten for students who do not speak English as a
first language: no idioms, no phrasal verbs where a plain verb exists, and no
rhetorical constructions. "Ask for too much and the robot does not refuse — it
saturates" became "A robot does not reject an impossible command. It saturates."
"Hands you" became "provides". "Cuts the corner" became "falls short of the true
arc". The same pass was applied to the seven new cue-sheet notes.

### Layout

The house standard is zero overfull boxes — `EE414_W04A_differential_drive.log`
has none. The first build of the light deck had eight, the worst 49 pt. They
were removed by shortening prose and tightening vertical space, not by shrinking
type. Final build: **0 overfull vboxes, 0 overfull hboxes.**

The robot diagram on slide 5 was drawn twice. The first attempt put the $L$
label on top of the forward arrow and the $\omega$ labels inside the robot body.
It was redrawn with the dimension line outside the body and the wheel-speed
labels clear to the right.

## Beginner code in the cue sheet

The cue sheet already carried thirteen collapsed `Code ·` snapshots from the
full sources. Seven of them now have a green `Simple ·` snapshot immediately
**above** them, holding the same idea from
`beginner_student_freindly/`: angle normalisation, forward kinematics, inverse
kinematics, the six Twist fields, the minimal subscriber, open loop, and closed
loop.

Above, not below, on purpose: in the lecture the room reads the forty-line
version first and the production version second.

Generated the same way as everything else in the handout —
`shared/screenshots/snippets.py` gained a `SIMPLE` table and a
`render_simple()`, and `shared/screenshots/insert_simple.py` places the blocks.
`insert_simple.py` is **idempotent**: it strips any beginner blocks from a
previous run before placing them again, so the handout can be regenerated
whenever the beginner scripts change. The colour is the only signal that
distinguishes them — green for the version you read aloud, indigo for the
version that ships.

## Where the two packages live

Asked during this session, and worth recording because the answer is not
guessable: `ee414_w04_demo` and `ee414_course` are **separate packages in
separate workspaces**.

| Package | Source | Built into |
|---|---|---|
| `ee414_w04_demo` | `code/src/ee414_w04_demo/` | `code/install/` |
| `ee414_course` | `~/ros2_ws/src/ee414_course/` | `~/ros2_ws/install/` |

`shared/screenshots/rosenv.sh` sources both, which is why the cue sheet can use
whichever package makes a point better in the same terminal.

**A duplicate now exists and should be resolved.** The previous commit copied
`ee414_course` into `code/src/ee414_course/` so that it would be under version
control at all. The copy that actually builds and runs is still the one in
`~/ros2_ws`. Two copies of the same package will drift. The clean fix is to make
`~/ros2_ws/src/ee414_course` a symlink to the repository copy, but that was not
done on the evening before a lecture.
