#!/usr/bin/env python3
"""Why the four numbers, and why they are the numerically stable four.

Slide reference: "Why Four Numbers? The Case for the Quaternion" and
"The Same Idea, Drawn: Axis, Angle, and Lock".

Four short demonstrations, each one printing its own evidence:

    1. a flat robot's quaternion is just its heading, written differently
    2. the unit-norm constraint, and what breaks it
    3. drift repair: one line for a quaternion, a page for a matrix
    4. gimbal lock, watched as it happens

    python3 quaternion_demo.py            # all four
    python3 quaternion_demo.py --part 4   # just gimbal lock
"""

import argparse
import math

SEP = "-" * 68


def quat_from_yaw(theta):
    """A rotation about z only -- the only kind a floor robot ever has."""
    return (0.0, 0.0, math.sin(theta / 2.0), math.cos(theta / 2.0))


def yaw_from_quat(x, y, z, w):
    """Pull the heading back out. This is what tf2 does at the edges."""
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    return math.atan2(siny_cosp, cosy_cosp)


def quat_multiply(a, b):
    """Compose two rotations. Note what is NOT here: no sin, no cos, no division."""
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
            aw * bw - ax * bx - ay * by - az * bz)


def norm(q):
    return math.sqrt(sum(c * c for c in q))


def part1():
    print(SEP)
    print("1. A flat robot's quaternion IS its heading, written differently")
    print(SEP)
    print("   A robot on a floor turns about one axis: straight up, z.")
    print("   So x and y are always 0, and only z and w carry the heading.\n")
    print("   heading        quaternion (x, y, z, w)                    back again")
    for deg in [0, 45, 90, 180, -90]:
        theta = math.radians(deg)
        q = quat_from_yaw(theta)
        back = math.degrees(yaw_from_quat(*q))
        print(f"   {deg:4d} deg      ({q[0]:.3f}, {q[1]:.3f}, {q[2]:+.4f}, {q[3]:+.4f})"
              f"        {back:+7.1f} deg")
    print("\n   Two of the four numbers are always zero and you still only ever")
    print("   had one angle. Nothing was lost and nothing was gained -- yet.")
    print("   The gain shows up in part 4, when the robot leaves the floor.\n")


def part2():
    print(SEP)
    print("2. Four numbers, one constraint")
    print(SEP)
    print("   x^2 + y^2 + z^2 + w^2 = 1, always. That is what makes four")
    print("   numbers describe three degrees of freedom.\n")
    q = quat_from_yaw(math.radians(37))
    print(f"   a real heading of 37 deg -> ({q[0]:.3f}, {q[1]:.3f}, {q[2]:.6f}, {q[3]:.6f})")
    print(f"   its norm = {norm(q):.15f}\n")

    bad = (0.0, 0.0, 0.5, 0.5)
    print(f"   now an invented one       -> {bad}")
    print(f"   its norm = {norm(bad):.15f}   <-- not 1, so this is not a rotation")
    print(f"   it claims a heading of {math.degrees(yaw_from_quat(*bad)):.1f} deg, but the")
    print("   length is wrong, so it also scales anything it is applied to.\n")
    fixed = tuple(c / norm(bad) for c in bad)
    print(f"   divide by the norm        -> ({fixed[0]:.3f}, {fixed[1]:.3f}, "
          f"{fixed[2]:.6f}, {fixed[3]:.6f})")
    print(f"   norm now = {norm(fixed):.15f}   <-- a rotation again, of "
          f"{math.degrees(yaw_from_quat(*fixed)):.1f} deg\n")


def part3():
    print(SEP)
    print("3. Drift, and how cheaply it is repaired")
    print(SEP)
    print("   Odometry composes a small rotation thousands of times a minute.")
    print("   Every multiplication rounds. Watch the norm walk away from 1.\n")

    step = quat_from_yaw(math.radians(0.05))   # one small turn, applied over and over
    q = (0.0, 0.0, 0.0, 1.0)
    print("   composings        norm                      error from 1")
    for i in range(1, 200001):
        q = quat_multiply(q, step)
        if i in (1, 100, 1000, 10000, 100000, 200000):
            n = norm(q)
            print(f"   {i:9d}        {n:.15f}       {abs(n - 1.0):.3e}")

    n = norm(q)
    print(f"\n   After 200000 compositions the norm is off by {abs(n - 1.0):.3e}.")
    print("   The repair is one line:\n")
    print("       q = q / norm(q)\n")
    q = tuple(c / n for c in q)
    print(f"   norm now = {norm(q):.15f}\n")
    print("   A 3x3 rotation matrix drifts too, but its constraint is that all")
    print("   three columns stay unit length AND mutually perpendicular -- six")
    print("   conditions, not one. Repairing it means re-orthonormalising, which")
    print("   is Gram-Schmidt or an SVD. That is the whole argument: tf2 stores")
    print("   quaternions because the cheap repair is the one you can afford to")
    print("   do every single cycle.\n")


def part4():
    print(SEP)
    print("4. Gimbal lock, watched as it happens")
    print(SEP)
    print("   Roll-pitch-yaw recovers yaw with a division by cos(pitch).")
    print("   Tilt the pitch towards 90 degrees and watch that divisor go to zero.\n")
    print("   pitch        cos(pitch)          1/cos(pitch)")
    for pitch_deg in [0, 45, 80, 89, 89.9, 89.99, 89.999, 90.0]:
        c = math.cos(math.radians(pitch_deg))
        if abs(c) < 1e-15:
            print(f"   {pitch_deg:7.3f}      {c:.3e}       DIVISION BY ZERO")
        else:
            print(f"   {pitch_deg:7.3f}      {c:.6e}       {1.0 / c:.6e}")

    print("\n   At pitch = 90 the first and third axes point the same way, so")
    print("   rolling and yawing do the identical thing. One degree of freedom")
    print("   has vanished from the representation -- not from the robot.\n")
    print("   The quaternion for that same orientation is ordinary:")
    half = math.radians(90.0) / 2.0
    q = (0.0, math.sin(half), 0.0, math.cos(half))   # pitch 90 about y
    print(f"       (x, y, z, w) = ({q[0]:.4f}, {q[1]:.4f}, {q[2]:.4f}, {q[3]:.4f})")
    print(f"       norm = {norm(q):.15f}")
    print("\n   No zero, no infinity, nothing special about it at all. There are")
    print("   no rings to line up, so there is nothing to lock.\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--part", type=int, choices=[1, 2, 3, 4],
                        help="run only one part")
    args = parser.parse_args()

    parts = {1: part1, 2: part2, 3: part3, 4: part4}
    print()
    if args.part:
        parts[args.part]()
    else:
        for i in (1, 2, 3, 4):
            parts[i]()


if __name__ == "__main__":
    main()
