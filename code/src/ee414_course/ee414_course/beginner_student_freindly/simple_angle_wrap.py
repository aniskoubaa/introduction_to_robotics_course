#!/usr/bin/env python3
"""Never subtract two headings directly. No ROS.

This is the single most common bug in robot motion code, and it is one
line to fix.

    ros2 run ee414_course simple_angle_wrap
"""

import math


def normalize(angle):
    """Fold any angle back into -180 .. +180 degrees. THE FIX."""
    return math.atan2(math.sin(angle), math.cos(angle))


def main(args=None):
    facing = math.radians(176)     # the robot faces  +176 deg
    target = math.radians(-176)    # the goal is at   -176 deg

    naive = math.degrees(target - facing)
    fixed = math.degrees(normalize(target - facing))

    print("\n  robot faces  +176 deg")
    print("  goal is at   -176 deg")
    print("  Draw it: they are 8 degrees apart, across the seam at 180.\n")
    print(f"  naive     target - facing    = {naive:+.1f} deg")
    print(f"  wrapped   normalize(t - f)   = {fixed:+.1f} deg\n")
    print("  Given the naive number, the robot turns 352 degrees the wrong")
    print("  way to make an 8 degree correction -- every time it crosses")
    print("  the seam. Always wrap the DIFFERENCE.\n")


if __name__ == "__main__":
    main()
