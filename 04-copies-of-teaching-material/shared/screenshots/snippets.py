#!/usr/bin/env python3
"""Pull the code snapshots for the cue sheet straight out of the sources.

The snippet in the handout and the code on disk cannot drift, because the
handout is generated from the code every time this runs.
"""
import html, os, re, sys

W04 = os.path.expanduser("~/EE414/introduction_to_robotics_course/code/src/ee414_w04_demo")
CRS = "/home/alfaisalx/ros2_ws/src/ee414_course"

def squash_docstrings(lines):
    """Keep the first line of every docstring, drop the rest.

    A snapshot is projected on a wall. The reasoning belongs in the file; the
    slide needs the arithmetic. Long docstrings keep their first line only.
    """
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'(\s*)("""|\'\'\')', line)
        if not m:
            out.append(line); i += 1; continue
        indent, q = m.group(1), m.group(2)
        rest = line[len(indent) + 3:]
        if rest.rstrip().endswith(q):            # a one-line docstring
            out.append(line); i += 1; continue
        j = i + 1
        while j < len(lines) and q not in lines[j]:
            j += 1
        if j - i > 2:                            # more than one line of prose
            out.append(f"{indent}{q}{rest.rstrip()} ...{q}")
        else:
            out.extend(lines[i:j + 1])
        i = j + 1
    return out


def grab(path, first, last, dedent=None):
    lines = open(path).read().splitlines()[first - 1:last]
    if path.endswith(".py"):
        lines = squash_docstrings(lines)
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if dedent is None:
        dedent = min((len(l) - len(l.lstrip()) for l in lines if l.strip()), default=0)
    return "\n".join(l[dedent:] if len(l) >= dedent else l for l in lines)

# id -> (root, relative path, first line, last line, summary, note)
SNIPS = {
 "wrap": (CRS, "ee414_course/robot_pose.py", (22, 35),
   "normalize_angle — the whole of slide 13",
   "One line of arithmetic. <code>sin</code> and <code>cos</code> are already periodic, so "
   "<code>atan2</code> of the pair throws the winding away and keeps the direction."),

 "quat": (W04, "ee414_w04_demo/quaternion_demo.py", (24, 34),
   "heading &#8596; quaternion, both directions",
   "A floor robot only ever rotates about <code>z</code>, so two of the four numbers are always "
   "zero. <code>yaw_from_quat</code> is what tf2 runs at every edge of the tree."),

 "twistcompat": (W04, "ee414_w04_demo/twist_compat.py", (22, 42),
   "asking the graph which Twist the topic wants",
   "Why every script in both packages runs on turtlesim <em>and</em> TurtleBot 3 without being "
   "edited. Subscribing with the wrong type is silent: nothing moves, and nothing complains."),

 "sixfields": (CRS, "ee414_course/nonholonomic.py", (48, 61),
   "setting any of the six Twist fields by name",
   "The message accepts all six. The robot honours two. Nothing in ROS 2 stands between them."),

 "fk": (W04, "ee414_w04_demo/wheels_to_body.py", (25, 29),
   "forward kinematics — wheels to body",
   "Two lines of arithmetic. The other ninety in the file are printing."),

 "ik": (W04, "ee414_w04_demo/body_to_wheels.py", (28, 32),
   "inverse kinematics — body to wheels",
   "The same two equations, solved the other way round. This is the direction a real robot works "
   "in: you ask for <code>v</code> and <code>&#969;</code>, the wheels are what it has."),

 "saturate": (W04, "ee414_w04_demo/body_to_wheels.py", (49, 54),
   "what a real robot does when you ask for too much",
   "Scale <b>both</b> <code>v</code> and <code>&#969;</code> by the same factor. Clamping them "
   "separately changes the shape of the path, which is the other half of why the square comes "
   "out crooked."),

 "urdf": (W04, "urdf/burger_min.urdf", (35, 56),
   "the wheel, in URDF",
   "<code>r</code> is written down. <code>L</code> is not: it is the distance between two joint "
   "origins, and only the transform tree can work it out."),

 "sdf": (W04, "worlds/diff_drive_demo.sdf", (439, 451),
   "the one place both constants are read at run time",
   "Change <code>wheel_separation</code> here and the robot still drives perfectly. Only its "
   "report of where it went is wrong, by the same factor, for ever."),

 "odomread": (W04, "ee414_w04_demo/pose_watch.py", [(58, 58), (62, 65)],
   "what you actually get out of /odom",
   "<code>turtlesim/Pose</code> hands you <code>theta</code>. <code>nav_msgs/Odometry</code> hands "
   "you four numbers and leaves the trigonometry to you. <code>|q|</code> is printed so the class "
   "can watch it stay at 1.000000."),

 "integrators": (W04, "ee414_w04_demo/dead_reckoning.py", (29, 45),
   "the two integrators, side by side",
   "Euler freezes the heading for the whole step, then turns. The arc form follows the circle the "
   "robot is genuinely on, and is <b>exact</b> whenever <code>v</code> and <code>&#969;</code> are "
   "held constant — which, between two <code>/cmd_vel</code> messages, they are."),

 "openloop": (W04, "ee414_w04_demo/drive.py", (64, 78),
   "the whole of open loop",
   "Publish, wait, stop. The pose IS subscribed to, but only to report the error at the end — "
   "never to decide anything."),

 "closedloop": (CRS, "ee414_course/go_to_goal.py", [(91, 98), (110, 119)],
   "the same problem, closed loop",
   "Read the pose, work out the error, act on it, repeat. No duration is computed in advance. "
   "Put this beside the snapshot above: the difference between them is Week 5."),
}


def render(key):
    root, rel, spans, summary, note = SNIPS[key]
    if isinstance(spans[0], int):
        spans = [tuple(spans)]
    path = os.path.join(root, rel)
    a, b = spans[0][0], spans[-1][1]
    raw = [open(path).read().splitlines()[lo - 1:hi] for lo, hi in spans]
    flat = [l for blk in raw for l in blk if l.strip()]
    shared = min((len(l) - len(l.lstrip()) for l in flat), default=0)
    chunks = [grab(path, lo, hi, dedent=shared) for lo, hi in spans]
    joined = chunks[0]
    for nxt in chunks[1:]:
        pad = " " * (len(nxt) - len(nxt.lstrip()))
        joined += f"\n\n{pad}# ...\n\n{nxt}"
    code = html.escape(joined)
    pkg = "ee414_w04_demo" if root == W04 else "ee414_course"
    shown = rel if rel.startswith(pkg + "/") else f"{pkg}/{rel}"
    return (f'      <details class="code">\n'
            f'        <summary>Code · {summary}</summary>\n'
            f'        <p class="path">{shown}'
            f'<span class="ln">lines {a}–{b}</span></p>\n'
            f'        <pre><code>{code}</code></pre>\n'
            f'        <p class="cnote">{note}</p>\n'
            f'      </details>\n')

# ---------------------------------------------------------------------------
# The BEGINNER versions of the same ideas.
#
# Each one sits directly above the full snapshot of the same concept, so the
# room reads the forty-line version first and the production version second.
# Same generation rule: quoted from the files on disk, never retyped.
# ---------------------------------------------------------------------------
BEG = os.path.join(CRS, "ee414_course/beginner_student_freindly")

# id of the full snapshot it goes above -> (file, spans, summary, note)
SIMPLE = {
 "wrap": ("simple_angle_wrap.py", (13, 15),
   "the same fix, on its own",
   "No class, no node, and no import except <code>math</code>. It prints 8&nbsp;degrees "
   "where the plain subtraction gives &minus;352."),

 "fk": ("simple_kinematics.py", (10, 18),
   "forward kinematics, and nothing else",
   "The two constants and the two equations, in nine lines. The <em>sum</em> of the wheel "
   "speeds produces forward motion; the <em>difference</em> produces rotation."),

 "ik": ("simple_kinematics.py", (21, 25),
   "inverse kinematics, and nothing else",
   "The same two equations solved the other way round, in the same file."),

 "sixfields": ("simple_nonholonomic.py", (43, 54),
   "publishing the field that does nothing",
   "Four lines produce the demonstration. <code>msg.linear.y</code> is a valid field of a "
   "valid message, published to a valid topic, and the turtle does not move."),

 "odomread": ("simple_pose_reader.py", (20, 33),
   "the smallest node that reads a pose",
   "A node, a subscription, a callback. Every subscriber follows these three steps in "
   "this order."),

 "openloop": ("simple_move.py", (43, 57),
   "open loop, in fifteen lines",
   "<code>seconds = DISTANCE / SPEED</code> is the whole control law. No line below it reads "
   "the pose. That is the definition of open loop."),

 "closedloop": ("simple_go_to_goal.py", (52, 75),
   "closed loop, in the same shape",
   "Four lines compute the error from the most recent pose; the next two convert it into a "
   "velocity. That is the only difference from the program below."),
}


def render_simple(key):
    """The beginner snapshot for `key`, or '' if there is no beginner version."""
    if key not in SIMPLE:
        return ""
    rel, spans, summary, note = SIMPLE[key]
    if isinstance(spans[0], int):
        spans = [tuple(spans)]
    path = os.path.join(BEG, rel)
    a, b = spans[0][0], spans[-1][1]
    flat = [l for lo, hi in spans
            for l in open(path).read().splitlines()[lo - 1:hi] if l.strip()]
    shared = min((len(l) - len(l.lstrip()) for l in flat), default=0)
    code = html.escape("\n\n".join(grab(path, lo, hi, dedent=shared) for lo, hi in spans))
    return (f'      <details class="code simple">\n'
            f'        <summary>Simple · {summary}</summary>\n'
            f'        <p class="path">beginner_student_freindly/{rel}'
            f'<span class="ln">lines {a}–{b}</span></p>\n'
            f'        <pre><code>{code}</code></pre>\n'
            f'        <p class="cnote">{note}</p>\n'
            f'      </details>\n')


if __name__ == "__main__":
    for k in SNIPS:
        print(render(k))
