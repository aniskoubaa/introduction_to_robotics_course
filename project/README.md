# Course Project — 20%

Teams of **3**. A complete autonomous mobile-robot application built in ROS 2, demonstrated
live in Gazebo (or on a TurtleBot3 where hardware is available).

The project is where the four CLOs meet: it requires the architecture understanding of
CLO 1, the analysis of CLO 2, the implementation of CLO 3, and the teamwork and
responsibility of CLO 4.

## Suggested scopes

| Scope | Core challenge | Uses |
|---|---|---|
| Autonomous warehouse delivery | Multi-goal navigation, task sequencing | Nav2, TF2, behaviour trees |
| Coverage / cleaning | Complete-coverage planning under a map | SLAM, costmaps, custom planner |
| Frontier exploration | Autonomous mapping of an unknown world | `slam_toolbox`, frontier detection |
| LiDAR-based person following | Reactive control from live scans | `/scan`, closed-loop control |
| Teams may propose their own — approval required at the proposal milestone. |

## Deliverables

| Deliverable | Weight |
|---|---|
| Functionality — does it work, and how robustly | 40% |
| Software quality and ROS 2 idiom — packages, launch, params, no hard-coded frames | 20% |
| Technical report — 6 pages, `report_template.md` | 20% |
| Presentation — 10 minutes + live demo | 10% |
| Teamwork and peer evaluation | 10% |

Also required: a **Git repository** with a readable history showing all three members
contributing, and a **launch file** that brings up the whole system in one command.

## Milestones

See `milestones/README.md`. Proposal Week 5 · design review Week 13 · demonstration and
report Week 14.

## Files

| File | Description |
|---|---|
| `proposal_template.md` | ❌ To be authored — 2 pages: scope, architecture, division of work, risks |
| `report_template.md` | ❌ To be authored — 6 pages: problem, design, implementation, evaluation, reflection |
| `rubric.md` | ❌ To be authored — the marking scheme above, broken into observable criteria |
| `milestones/` | ❌ To be authored |

## AI-tool policy

Coding agents are permitted and expected. Two conditions: **disclose** what you used and for
what, in the report; and be able to **explain and defend** every line at the demonstration.
A team that cannot explain its own code has not met CLO 3, whatever the code does.
