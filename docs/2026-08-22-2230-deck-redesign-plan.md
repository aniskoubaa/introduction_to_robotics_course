# EE 414 — deck redesign plan

**Date:** 22 August 2026
**Supersedes:** §7 of the density review and §7 of the content/flow review. Those documents
remain the evidence; **this document is the operative plan.**
**Sources:** `2026-08-22-2153-slide-design-review-against-legacy-decks.md`,
`2026-08-22-2210-content-and-flow-review-against-legacy-decks.md`

---

## 0. The constraint that shapes everything

> ⚠️ **Fall 2026 Week 1 is Sunday 23 August — tomorrow.**
> (Assumed from the MAI 580 Fall 2026 calendar, same institution and term. **Confirm the EE 414
> section timetable before acting on the dates below.**)

This is not a redesign with a clear runway. It is a running semester with two decks already
built at the wrong density and nine weeks unwritten. The plan is therefore triaged into:

| Horizon | Rule |
|---|---|
| **T-0 — this weekend** | Only what Week 1 cannot run without |
| **T+1 week** | The format, so Week 2 onward is never authored densely again |
| **Rolling** | Two weeks ahead, permanently, in the new format |
| **Deferred** | Retrofitting Weeks 2, 3 and 7 — they are *usable* as they stand |

**The decisive judgement:** the existing decks are dense, not wrong. Delivering W01 as-is on
Sunday is survivable. Authoring nine more weeks at that density is not. **So the format change
takes priority over the retrofit.**

---

## 1. What changes — the new standing rules

Replacing the current standing rules in `04-copies-of-teaching-material/README.md`.

### Format (from the density review)

1. **No slide body exceeds 25 words.** Section dividers and code slides exempt.
2. **A 1.5-hour session is 40–60 slides.** Slide count is not a quality signal.
3. **Everything cut goes into `\note{}`** and compiles to a separate `*_notes.pdf`.
4. **Code is revealed one line per slide**, the new line highlighted.
5. **Real screenshots, not typeset listings**, wherever the student will compare against their
   own screen.

### Flow (from the content review)

6. **Every week opens with the previous week's solution failing.** The escalating problem
   statement is the spine of the course.
7. **Every mathematical topic gets one everyday analogy** before the formalism.
8. **Every major concept closes with a numbered procedure** — *how to decide*, not just how it
   works.
9. **Every B session is demo-first**: see it run, explore it from the CLI, then build it.
10. **Why-first for tools; pain-first for mathematics.** Never answer "why X" before the student
    has felt the problem X solves.

---

## 2. T-0 — before Sunday

Ordered. Stop when the time runs out; everything below the line survives one week of delay.

| # | Task | Effort | Why it cannot wait |
|---|---|---|---|
| 1 | **`setup/README.md` + `check_ros2_setup.py`**, tested on WSL2 and Docker at minimum | 4 h | Both W01 decks send students to it; **W02B cannot run without it**, and students need the weekend after Week 1 to install |
| 2 | **Assign `ROS_DOMAIN_ID` values** and put the list in the LMS | 15 min | Without it, Week 2 is a room where everyone's nodes see everyone else's |
| 3 | **Add three video slots + one out-of-scope slide to W01A** | 1 h | Cheapest possible improvement to the first impression; no rewrite needed, just insertion |
| 4 | **Add the instructor slide** to W01A | 15 min | One slide of credibility, delivered once |
| — | *line: everything below can slip a week* | | |
| 5 | Confirm the section timetable, room, and whether it is computer-equipped | — | Determines whether Week 2 is deliverable at all |

**W01A and W01B ship as they are.** They are dense; they are also correct, and they are the two
decks whose content is least harmed by density (policy, assessment, taxonomy). Read from the
notes, do not read from the slide.

---

## 3. T+1 — the format, before Week 2 is authored

| # | Task | Effort | Output |
|---|---|---|---|
| 1 | **Preamble: `\note{}` support + notes-PDF build target** | 1 h | The prose has somewhere to go |
| 2 | **Preamble: five new macros** | 3 h | The new slide vocabulary |
| 3 | **Pilot: rewrite W01B at the new density and flow** | 5 h | Proves the format on a deck already delivered — zero risk, full information |
| 4 | **Screenshot pipeline** — `shared/screenshots/` + `capture.md` | 3 h | The evidence layer |

### The five macros

| Macro | Purpose |
|---|---|
| `\bigq{WHY QUATERNIONS?}` | Full-bleed typographic question divider |
| `\codestep` | Progressive code reveal, new line highlighted |
| `\triptych{}{}{}` | What to set · what it looks like · what it is called |
| `\pathmap{N}` | Course map with week N highlighted, at each week opening |
| `\procedure` | The numbered "how to decide" list that closes a concept |

**Why W01B and not W01A as the pilot:** W01B is the first deck with real technical content and
the clearest test of `\codestep` and the analogy rule. W01A is mostly policy and gains least.

---

## 4. Curriculum changes

Four content decisions, folded into the existing 11-week structure. **None requires a change to
the approved credit structure or the CLOs.**

### 4.1 Bug algorithms enter Week 6B — decided

Week 6 becomes:

| | |
|---|---|
| **6A** | Sensors and actuators; LiDAR principles, noise, range models; **real commercial hardware** (Hokuyo, RPLidar, RGBD) with ranges and prices |
| **6B** | `/scan` processing → wall following → **Bug 0** → **watch it fail in a U-shaped trap** |

**Week 6B must end with the failure, not the success.** That unresolved failure then hangs over
Weeks 7–9 and is what makes SLAM in Week 10 an answer rather than an announcement. It is the
single highest-value structural change in this plan.

Specification impact: topic 4 in §C.2 should be renamed **"Sensors, perception and reactive
navigation"**. The hours are unchanged. Since the specification is still pending Council
approval, **make this edit now** rather than after.

### 4.2 Week 11 gains real algorithmic content

A* expands from a bullet to **8–12 animated slides** — open and closed lists filled in step by
step, then the heuristic changed to show the effect. DWA and trajectory scoring get their own
treatment. This is the one algorithm in the course a student can understand end to end.

### 4.3 Week 12 gains the robot-setup checklist

What a robot must provide before the navigation stack will run: a valid TF tree, odometry, a
laser source, a base controller accepting `/cmd_vel`, a map. Issued as **a one-page checklist the
project teams tick off** — this is the integration knowledge that decides whether projects work.

### 4.4 Parameters get provenance

One slide, reused: **how to measure a real robot's maximum velocity and acceleration**, and put
the measured numbers into the configuration. Plus a **before/after pair** for every tuning topic
— Week 5 gains, Week 9 covariances, Week 10 resolution, Week 11 inflation.

---

## 5. Rolling cadence — the rule for the rest of the semester

> **Author two weeks ahead, natively in the new format. Never retrofit.**

Per week of material, at the new density and flow:

| Artifact | Effort |
|---|---|
| A deck (40–60 slides) + notes | 5 h |
| B deck (40–60 slides) + notes | 5 h |
| Starter package in `code/src/` | 3 h |
| Screenshots + expected-output transcript | 3 h |
| Lab sheet + week README | 2 h |
| **Total per week** | **~18 h** |

Nine weeks unwritten (4, 5, 6, 8, 9, 10, 11, 12, 13) ≈ **160 hours**. At two weeks ahead of a
15-week semester that is roughly **12–15 hours per week of authoring**, sustained.

**This is the number that matters, and it should be checked against reality before Week 3.** If
it is not sustainable, the honest responses are (a) reuse the legacy decks directly for Weeks
10–11, updating ROS 1 → ROS 2, or (b) drop the advanced topic in Week 12. Both are better than
authoring nine dense weeks and rewriting them in January.

---

## 6. Deferred — the retrofit

Weeks 2, 3 and 7 are **delivered or deliverable as they stand**. Retrofit them only if the
rolling cadence leaves room, in this order:

| Priority | Deck | Why |
|---|---|---|
| 1 | **W07A** — resequence per the flow review §6 | Worst-ordered deck: rotation before translation, no concrete two-frame anchor, 3D compressed to one table row. **Do this before Week 7 delivers**, not after |
| 2 | **W07B** — replace checkpoint 4 with the turtle follower | A complete behaviour instead of an abstract point |
| 3 | **W02A** — move QoS or workspaces out | Nine concepts in 90 minutes; the densest lecture in the course |
| 4 | **W02B** — insert 10 minutes of exploration before `pkg create` | Applies rule 9 |
| 5 | **W03A** — move parameters out of the "three shapes" spine | Parameters interrupt the argument |
| 6 | **W01A/W01B** — full density rewrite | Already delivered; lowest return |

**W07A is the exception to "deferred".** It is scheduled for Week 7, it is the worst-ordered
deck, and the resequence is already written out. Treat it as a rolling-cadence item, not a
retrofit.

---

## 7. What is explicitly not changing

- **The specification** — CLOs, credit structure, assessment weights, the 11+4 calendar. None of
  this review touches the approved design.
- **Python only, no C++.** The legacy course teaches both; a 45-hour elective cannot.
- **No OpenCV, rosserial, drones or arms.** Correct scoping — but now **stated on a slide in
  Week 1** so students know in week one.
- **The pedagogical devices that are working:** deliberate failure, the diagnostic order,
  `underhood`/`inthefield`, notation as a type check, checkpoints, the exam blueprint.

---

## 8. Decisions needed from the instructor

| # | Question | Blocks |
|---|---|---|
| 1 | **Is Week 1 Sunday 23 August?** And what is the section timetable? | The whole T-0 list |
| 2 | Is the classroom computer-equipped, or do students bring laptops? | Whether Week 2 is deliverable |
| 3 | Are TurtleBot3 units available, or is the course Gazebo-only? | Weeks 10–14 |
| 4 | Who captures the screenshots — is there a machine with the real stack running? | The evidence layer, §3.4 |
| 5 | Is ~15 h/week of authoring realistic, or should Weeks 10–11 reuse the legacy decks? | The rolling cadence, §5 |
| 6 | Week 12 advanced topic: MoveIt 2, or learning-based control / VLA? | Week 12 |

---

## 9. Summary

**Tonight:** the setup guide, domain IDs, four slides inserted into W01A. Deliver Week 1 as it
is.

**This week:** the notes mechanism and five macros, then rewrite W01B as the pilot. From that
point nothing is ever authored densely again.

**From Week 2 onward:** two weeks ahead, in the new format, with Bug 0 planted in Week 6 so that
SLAM in Week 10 answers a failure the students watched happen.

**Retrofit last, and W07A first among the retrofits** — it is the worst deck and it is scheduled.
