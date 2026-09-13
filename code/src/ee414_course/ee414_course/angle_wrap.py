#!/usr/bin/env python3
# This file is part of the ee414_course package.
#
# EE 414 — Introduction to Robotics. Week 4, slide 13.
"""Angles wrap, and that is where the bugs live.

No ROS. Pure arithmetic, and a real bug.

This script exists because of a line in the original course code. In
ros2_motion_python/clean.py, rotate() decided when to stop like this:

    rotated_related_angle_degree = math.degrees(abs(start_pose.theta - self.pose.theta))

That is correct right up until theta crosses the +/-pi seam, and then it is
catastrophically wrong -- the measured rotation jumps from nearly 0 to nearly
360 in one timestep. go_to_goal() had the same problem in its heading error.

Both are fixed in this package. This script shows why the fix was needed.

    ros2 run ee414_course angle_wrap
"""

import math

LINE = "-" * 72


def normalize_angle(angle):
    """Fold any angle into (-pi, pi]. The fix, in one line."""
    return math.atan2(math.sin(angle), math.cos(angle))


def part1_the_seam():
    print(LINE)
    print("1. Two headings that are 8 degrees apart")
    print(LINE)
    a = math.radians(176)     # facing almost due west, just north of it
    b = math.radians(-176)    # facing almost due west, just south of it

    print(f"   robot faces   {math.degrees(a):+7.1f} deg")
    print(f"   target is at  {math.degrees(b):+7.1f} deg")
    print("   Draw it: they are 8 degrees apart, across the seam at 180.\n")

    naive = b - a
    fixed = normalize_angle(b - a)

    print(f"   naive    target - current  = {math.degrees(naive):+8.1f} deg")
    print(f"   wrapped  normalize(t - c)  = {math.degrees(fixed):+8.1f} deg")
    print()
    print("   A controller given the naive number turns 352 degrees the wrong")
    print("   way to achieve an 8 degree correction. It will do that every")
    print("   single time the robot crosses the seam.")
    print()


def part2_the_rotate_bug():
    print(LINE)
    print("2. The bug in the original rotate(), watched as it happens")
    print(LINE)
    print("   A robot spins left at 30 deg/s. It starts at +170 degrees.")
    print("   rotate() wants to stop after it has turned 40 degrees.\n")

    start = math.radians(170.0)
    theta = start
    dt = 0.2
    omega = math.radians(30.0)

    print("    time    heading      buggy measure      correct measure")
    stopped_buggy = None
    stopped_fixed = None

    for step in range(1, 12):
        t = step * dt
        # The simulator reports theta already wrapped -- which is what every
        # real pose topic does, and exactly what breaks the naive expression.
        theta = normalize_angle(theta + omega * dt)

        buggy = math.degrees(abs(start - theta))
        correct = math.degrees(abs(normalize_angle(theta - start)))

        flag = ""
        if stopped_buggy is None and buggy >= 40.0:
            stopped_buggy = t
            flag += "   <-- buggy stops here"
        if stopped_fixed is None and correct >= 40.0:
            stopped_fixed = t
            flag += "   <-- correct stops here"

        print(f"   {t:4.1f}s   {math.degrees(theta):+8.1f}    "
              f"{buggy:9.1f} deg     {correct:9.1f} deg{flag}")

    print()
    print(f"   The robot really turned {math.degrees(abs(normalize_angle(theta - start))):.0f} degrees.")
    print(f"   The buggy measure crossed 40 at t = {stopped_buggy:.1f}s, after a")
    print(f"   real turn of only {math.degrees(omega) * stopped_buggy:.0f} degrees --")
    print("   because the heading wrapped from +180 to -180 and the naive")
    print("   subtraction read that jump as a 340-degree rotation.")
    print()
    print("   The fix is to wrap the DIFFERENCE, not to trust the difference:")
    print("       turned = abs(normalize_angle(now - start))")
    print()


def part3_where_it_bites():
    print(LINE)
    print("3. Where this shows up in the rest of the course")
    print(LINE)
    print("   Week 4  rotate() stops at the wrong time, or never stops.")
    print("   Week 5  a P controller on heading spins the long way round.")
    print("   Week 7  tf2 gives you quaternions partly to avoid this: there")
    print("           is no seam in a quaternion to trip over.")
    print("   Week 11 a goal behind the robot makes Nav2 turn the wrong way.")
    print()
    print("   One rule: NEVER subtract two headings without wrapping the result.")
    print("   In this package that is robot_pose.normalize_angle().")
    print()


def main(args=None):
    print()
    part1_the_seam()
    part2_the_rotate_bug()
    part3_where_it_bites()


if __name__ == "__main__":
    main()
