# 01 — Course Specification

**Status:** ✅ Drafted (V2026 redesign) — **pending EE Department Council approval.**

## Contents

| File | Description |
|---|---|
| `ee414-course-specification-fall2026.md` | **Authoritative source content**, structured 1:1 against TP-153 sections A–G. Edit this first. |
| `ee414-course-specification-fall2026.docx` | Generated from the Markdown (`pandoc -f gfm -t docx`). Working copy for review. |
| `template-ug-course-specification-tp153.docx` / `.pdf` | Blank official ETEC form (unmodified). |

## Regenerating the docx

```bash
pandoc -f gfm -t docx ee414-course-specification-fall2026.md \
  -o ee414-course-specification-fall2026.docx
```

The submission copy must eventually be transferred into the official TP-153 form, not the
plain pandoc output. See `../../SE100/se100_course/01-course-specification/build-docx.py`
for the script pattern that fills the blank form while preserving its styles.

## What this specification does

Rebuilds EE 414 around **ROS 2** as the teaching vehicle. Every theoretical concept —
kinematics, control, perception, transformations, estimation, planning — is introduced in
the lecture and realised the same week as running ROS 2 code in Gazebo. The model is CS460
*Introduction to Mobile Robots* (Prince Sultan University), reduced to a lighter technical
load: **11 taught weeks + 4 weeks** for examination, project and review.

Credit structure stays at the standard Alfaisal **3 (3-0-0)**, 45 contact hours, classroom
100%. Each 3-hour week runs as **2 h lecture + 1 h in-class ROS 2 practice** in a
computer-equipped classroom. No laboratory credit is claimed.

## The four CLOs

Bloom-anchored, ≤ 15 words each, one action verb, one assessable object — short enough to be
recalled without opening the document.

| # | Statement | Bloom | PLO (SO) |
|---|---|---|---|
| CLO 1 — **EXPLAIN** | Explain robot system architectures and the ROS 2 computation graph. | Understand (L2) | PLO 1 (SO 8), PLO 3 (SO 7) |
| CLO 2 — **ANALYZE** | Analyze robot kinematics, motion control and state estimation problems. | Analyze (L4) | PLO 2 (SO 1) |
| CLO 3 — **DEVELOP** | Develop ROS 2 software for robot perception, localization and navigation. | Create (L6) | PLO 4 (SO 2), PLO 5 (SO 6) |
| CLO 4 — **EVALUATE** | Evaluate ethical and safety implications of autonomous robots within a team. | Evaluate (L5) | PLO 6 (SO 3), PLO 7 (SO 4), PLO 8 (SO 5) |

All eight PLOs remain covered, so the FCAR attainment sheet is unaffected.

## Assessment weights

| Instrument | Weight |
|---|---|
| Attendance and participation | 5% |
| ROS 2 assignments (4 graded, lowest dropped) | 15% |
| Quizzes (5 short, lowest dropped) | 5% |
| Midterm Examination I (Week 6) | 15% |
| Midterm Examination II (Week 12) | 15% |
| Course project (Weeks 13–14) | 20% |
| Final Examination (comprehensive) | 25% |

## Next steps

1. Confirm the **computer-equipped classroom** request with the College — the practice hour
   depends on it.
2. Decide the **advanced topic** for Week 12: MoveIt 2 manipulation, or learning-based
   control / VLA models. The specification leaves it to the instructor; the syllabus must fix it.
3. Confirm whether **2–4 TurtleBot3 units** can be funded. The course is fully deliverable in
   Gazebo without them; hardware is an enhancement, not a dependency.
4. Submit to the **EE Department Council**. Fill Reference No. and Date in §G once approved.
5. Only then draft the syllabus (section 02), which must be consistent with the approved CLOs,
   weights and topic order.

## Change log against V2024

The full table is the annex at the end of the Markdown file. The substantive items:

- **Nine CLO rows reduced to four**, all with actual outcome statements. V2024 had five rows
  carrying PLO mappings, teaching strategies and assessment methods but **no outcome text** —
  an ETEC/ABET audit failure.
- **"Forum Postings / Role-Playing" removed** as evidence for a modelling and control outcome.
- **ROS 2 named as the tooling** — V2024 promised "designing, building and programming robots"
  without identifying any software, platform or environment.
- **Content gaps closed**: rigid-body transformations and TF2, URDF modelling and simulation,
  sensors and actuators, LiDAR perception. V2024's topic 2 listed inverse kinematics only.
- **Ethics and safety taught** (Week 13). V2024 mapped PLO 7 / PLO 8 with nothing behind them.
- **Calendar aligned**: 11 taught weeks + 4 reserved, so a week lost to a holiday or a
  university event never costs a topic.
- **Essential reference changed** to Corke (Python edition) + the official ROS 2 documentation;
  Kelly moves to supportive.

The superseded V2024 form is kept at
`../10-additional-documents/ee414-course-specification-v2024-superseded.pdf`.
