# Slide design review — EE 414 decks against the legacy ROS course

**Date:** 22 August 2026
**Reviewed:** `anis_slides_legacy/ros-for-beginners-I-2020-slides.key.pdf` (295 slides),
`ros-for-beginners-II-slam-navigation-2020-slides.pdf` (278 slides). The two `.key` files
(`ros2-for-beginners.key`, `opencv-ros.key`) are Keynote binaries and were not readable.
**Against:** the eight EE 414 decks authored so far (Weeks 1–3, 7).

---

## 1. The one measurement that matters

Words of body text per slide, header/footer excluded:

| Deck | Median words/slide | Mean | Visual-only slides |
|---|---:|---:|---:|
| **ROS for Beginners I (legacy)** | **12** | 27 | 20% |
| **ROS for Beginners II (legacy)** | **20** | 31 | 10% |
| EE414 W01A Course Overview | 86 | 70 | 5 (all section dividers) |
| EE414 W01B What Is a Robot | 93 | 77 | 2 |
| EE414 W02A Computation Graph | 87 | 67 | 3 |
| EE414 W02B First Nodes | 62 | 54 | 3 |
| EE414 W03A Communication Models | 72 | 64 | 5 |
| EE414 W03B Your Own Interfaces | 57 | 51 | 3 |
| EE414 W07A Transformations | 96 | 73 | 4 |
| EE414 W07B TF2 in Practice | 78 | 65 | 2 |

**The EE 414 slides carry four to seven times more text per slide than the decks that sold.**

That is not a stylistic difference. A 90-word slide takes a student roughly 25 seconds to read,
and during those 25 seconds they are not listening. Every slide becomes a silent reading break
that the instructor talks over. A 12-word slide is read in two seconds and then the room looks
up — which is the only state in which teaching happens.

I wrote documents and projected them. The legacy decks are slides.

### What caused it

The `04-copies-of-teaching-material/README.md` standing rule says **"30 slides is the ceiling
for a 1.5-hour session."** Combined with a fixed amount of content, that rule could only be
satisfied by compressing prose onto slides. **The rule was actively harmful and should be
replaced** (§4.1).

---

## 2. Seven techniques in the legacy decks worth adopting

### 2.1 One line of code per slide, built up

The publisher is taught across slides titled: *Create a Publisher Object* → *Create and
Initialize a ROS Node* → *Publish the ROS Message* → *Running the Talker Node*. Each slide shows
the file as it stands, with the newly added line highlighted. The service client gets the same
treatment across eight slides: *Import the Service Request and Response* → *Create the Service
Client Proxy* → *Wait for the service before start communication* → *Execute the client*.

EE 414 currently drops an 18-line node in a single box with prose underneath (W02B, `talker.py`).
A student who loses the thread at line 4 has no way back in.

### 2.2 Real screenshots, not typeset code

The legacy decks show actual TurtleSim windows, actual terminal output, actual `rosmsg show`
results. EE 414 renders idealised code in a simulated terminal window.

The typeset version is prettier and it is weaker evidence. A screenshot says *this is what your
screen will look like*. A typeset listing says *this is what I claim your screen will look like*
— and students spot the difference immediately when their own output has an extra warning line.

This does not conflict with standing rule 2 ("every command has been run"). **A screenshot is
the artifact of having run it.**

### 2.3 Explore an existing system before building one

Legacy Week 1 order: install → run TurtleSim → `rosnode list` → `rostopic echo` → drive the
turtle with teleop → *only then* write a publisher. Six slides of poking at a system somebody
else wrote, before authoring anything.

EE 414 W02B goes to `ros2 pkg create` on slide 4. The vocabulary from W02A has nothing concrete
attached to it yet.

### 2.4 A single application as the spine of a block

*Divide and Conquer Approach*: Step 1 move straight → Step 2 rotate in place → Step 3 go to goal
→ Step 4 spiral → **Step 5 integrate all together to develop the cleaning application.**

Five lecture units, one artifact, and the student can see the whole shape from the first slide.
EE 414's weeks are currently independent exercises that happen to be in sequence.

### 2.5 Motivation before mechanism

The legacy deck opens with a `WHY ROS?` section: path planning video, navigation video, flying a
drone, a self-driving car, then ROS's industrial impact, then the instructor's own deployed work
(COROS, ROSLink, 5G teleoperation, truck platooning). Roughly 15 slides of *why you want this*
before a single technical claim.

EE 414 W01A argues by prose contrast ("two courses you could take"). The argument is sound and it
is text. Video of a real robot doing the thing does the same work in fifteen seconds.

### 2.6 Full-bleed typographic questions as dividers

`WHY QUATERNION?` occupies an entire slide in 100-point type on white. It is a pause, a rhythm
change, and a question the next five slides answer. EE 414 uses a small coloured box with the
section name — functional, forgettable.

### 2.7 Three registers on one slide

*Basic Motion Types: Go to Goal* places the `Twist` fields on the left (with the two that change
in red), the live TurtleSim window in the middle, and "PID Controller / Proportional / Integral /
Derivative" on the right. **What to set · what it looks like · what it is called** — 25 words
total, and the student holds all three at once.

Also note the colour discipline: red marks *the part that varies*, never decoration.

---

## 3. What the EE 414 decks do that the legacy decks do not — keep all of it

This is not a one-way comparison. The following are genuine improvements and must survive the
redesign:

| | |
|---|---|
| **Consequence-driven framing** | "Here is what your robot does on demo day", not "prefer actions for long tasks" |
| **Deliberate failure** | The Week 3 callback deadlock and the Week 2 five failures, caused by the student under supervision |
| **Diagnostic order** | Four commands, in sequence, that separate three identical-looking symptoms |
| **`underhood` / `inthefield` asides** | Mechanism and industrial cost, visually distinct, four lines maximum |
| **Notation as a type check** | `T_AB T_CD` compiles and is nonsense; the subscripts are the only defence |
| **Checkpoints** | Room management built into the deck |
| **Bloom-mapped CLOs and an exam blueprint** | 40% of every written exam is code on paper |
| **Reproducible source** | LaTeX in git, one shared preamble, `\rosver` pinned in a single place |

The legacy decks are stronger *slides*. The EE 414 decks are stronger *pedagogical design*. The
target is the second inside the first.

---

## 4. Recommended changes

### 4.1 Replace the slide-count rule with a word-count rule — highest priority

Delete: *"Thirty slides is the ceiling for a 1.5-hour session."*

Adopt:

> **No slide body exceeds 25 words.** Section dividers and code slides are exempt.
> A 1.5-hour session runs 40–60 slides. Slide count is not a quality signal; words per
> slide is.

Everything cut goes into `\note{}` — beamer speaker notes, compiled to a separate
`*_notes.pdf`. **Nothing is lost; it moves to where the instructor reads it and the student does
not.** The current prose is genuinely good teaching material and it is in the wrong place.

### 4.2 Progressive code reveal

Add a `\codestep` macro to the shared preamble: same listing, one more line, the new line
highlighted. An 18-line node becomes five slides. Cost: repetition in the `.tex`. Benefit: no
student is ever lost at line 4 with nowhere to re-enter.

### 4.3 A screenshot pipeline

Create `04-copies-of-teaching-material/shared/screenshots/` with:
- the captured PNGs, named `WNNx_<what>.png`
- a `capture.md` recording the exact command and world used for each

Real output, regenerable on a distribution upgrade, and it satisfies standing rule 2 by
construction. **This is the single largest production cost of the redesign** and should be
budgeted honestly — perhaps 2–3 hours per week of material.

### 4.4 Restructure every B session as explore → build

Ten minutes poking at a running system, then authoring. W02B becomes: launch TurtleBot3 →
`node list` → `topic list` → `topic echo /odom` → drive it with teleop → *now* build a package.
The vocabulary from A gets something concrete attached before anything is created.

### 4.5 One application per block

| Weeks | Spine artifact |
|---|---|
| 2–3 | The talker/listener pair, extended each week |
| 4–6 | **`patrol_bot`** — drive straight, rotate, go-to-goal, then avoid obstacles. Weeks 4, 5 and 6 are Steps 1–3 of one application. |
| 7–8 | The same robot, now correctly described in URDF with a full frame tree |
| 9–11 | **`explorer_bot`** — estimate, map, localize, navigate |

State the whole decomposition on one slide at the start of each block, exactly as *Divide and
Conquer* does.

### 4.6 Four new slide devices in the preamble

| Macro | Purpose |
|---|---|
| `\bigq{WHY QUATERNIONS?}` | Full-bleed typographic question divider |
| `\codestep` | Progressive code reveal with the new line highlighted |
| `\triptych{}{}{}` | The three-register layout: what to set · what it looks like · what it is called |
| `\pathmap{N}` | The course learning-path map with week N highlighted, shown at each week opening |

### 4.7 Add video slots to Week 1

Three 30–60 second clips before any technical content: a warehouse fleet, an inspection robot in
the field, a Nav2 robot replanning around a person. Then one slide of your own deployed work.
The legacy deck spends 15 slides on this and it is not self-indulgence — it is why students stay
awake in Week 6.

### 4.8 One instructor slide

The legacy decks open with credentials, lab, research interests. EE 414 has none. For a
fourth-year elective taught by the author of a best-selling course on exactly this stack, one
slide buys attention that the content then has to earn anyway.

---

## 5. Worked example: W02B `talker.py`, rewritten

**Current — one slide, 18 lines of code plus prose:**

> `talker.py — in ee414_w02_first_node/` · full class, imports, `__init__`, `create_publisher`,
> `create_timer`, `tick`, message construction, publish, log, counter.

**Proposed — five slides, each under 15 words:**

| # | Title | Body | Notes carry |
|---|---|---|---|
| 1 | A node is a class | 3 lines: imports + `class Talker(Node)` | Why subclassing, what `Node` gives you |
| 2 | Give it a name | + `super().__init__('talker')`, line highlighted | The name is what `ros2 node list` shows |
| 3 | Declare what it publishes | + `create_publisher(String, 'chatter', 10)` | Type, topic, queue depth; forward ref to QoS |
| 4 | Decide when it fires | + `create_timer(0.5, self.tick)` | **No `while` loop.** The framework calls you. |
| 5 | Fill and send | + the `tick` body | Message construction, `get_logger` |

Slide 5 then sits beside a **screenshot of the real terminal** showing `[INFO] [talker]: sent:
hello 0`.

Same content. Five times the pace, one fifth the reading, and a student who drifts at slide 3
rejoins at slide 4.

---

## 6. What not to carry over

- **ROS 1, catkin, `rosmsg`, `roscore`.** The legacy decks are Noetic-era. All ROS 2 equivalents
  are already correct in the EE 414 decks.
- **295-slide decks.** That is Udemy pacing — self-paced, pausable, rewindable. A classroom
  session is 40–60 slides at the same density.
- **Screenshot rot.** The legacy decks cannot be updated for a new distribution without
  recapturing everything by hand. §4.3's `capture.md` is the mitigation and must not be skipped.
- **C++ alongside Python.** The legacy course teaches both. EE 414 deliberately teaches only
  Python; that decision stands.

---

## 7. Suggested order of work

| # | Action | Cost | Effect |
|---|---|---|---|
| 1 | Replace the slide-count rule with the 25-word rule in `04-.../README.md` | minutes | Unblocks everything below |
| 2 | Add `\note{}` support and a notes-PDF build target to the shared preamble | ~1 h | Gives the prose somewhere to go |
| 3 | Add `\bigq`, `\codestep`, `\triptych`, `\pathmap` | ~2 h | The new slide vocabulary |
| 4 | Rewrite W01A and W01B at the new density | ~4 h | Proves the format before eight more weeks exist |
| 5 | Screenshot pipeline + recapture W02–W03 | ~6 h | The evidence layer |
| 6 | Rewrite W02, W03, W07 | ~8 h | Brings the authored weeks into line |
| 7 | Author Weeks 4–6 natively in the new format | — | Never write another dense deck |

**Do step 4 before authoring Weeks 4–6.** Rewriting eight decks is affordable; rewriting
twenty-two is not.

---

## 8. The honest summary

The EE 414 decks were built as if the slide were the artifact the student takes away. It is not
— the slide is what is on the wall while a person talks, and the artifact is the exercise sheet,
the lab checklist and the repository. The legacy decks understand this and the EE 414 decks do
not, which is why one of them sold and the other reads like a specification.

The fix is not to weaken the content. It is to move roughly 70% of the words from the slide body
into speaker notes, cut every code listing into single-line steps, and put real screenshots where
idealised listings currently sit.
