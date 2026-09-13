#!/usr/bin/env python3
"""Forward kinematics: two wheel speeds in, one body velocity out.

Slide reference: "Forward Kinematics: Wheels to Body".

    v = r * (w_R + w_L) / 2        forward speed, metres per second
    w = r * (w_R - w_L) / L        turning rate, radians per second

There is no ROS in this file on purpose. It is arithmetic, and a student
should see that the model is arithmetic before it is buried in a node.

    python3 wheels_to_body.py 10 10      # both wheels the same
    python3 wheels_to_body.py --table    # the four cases from the slide
"""

import argparse
import math

# TurtleBot 3 Burger. The same two numbers as the deck, and the same two
# numbers that go into the URDF in a later slide.
WHEEL_RADIUS = 0.033      # r, metres
WHEEL_SEPARATION = 0.160  # L, metres


def forward_kinematics(w_left, w_right, r=WHEEL_RADIUS, L=WHEEL_SEPARATION):
    """Wheel angular speeds (rad/s) -> body (v, omega) in (m/s, rad/s)."""
    v = r * (w_right + w_left) / 2.0
    omega = r * (w_right - w_left) / L
    return v, omega


def describe(w_left, w_right):
    """Print one case the way it would be read aloud in the lecture."""
    v, omega = forward_kinematics(w_left, w_right)

    print(f"  wheels   w_L = {w_left:7.2f} rad/s   w_R = {w_right:7.2f} rad/s")
    print(f"  body     v   = {v:7.4f} m/s     w   = {omega:7.4f} rad/s"
          f"  ({math.degrees(omega):6.1f} deg/s)")

    # The shape of the path follows from v and omega alone.
    if abs(omega) < 1e-9 and abs(v) < 1e-9:
        print("  path     stopped\n")
    elif abs(omega) < 1e-9:
        print("  path     a straight line\n")
    elif abs(v) < 1e-9:
        print("  path     a spin in place (the ICC is the robot's own centre)\n")
    else:
        # R = v / omega is the distance from the robot to the centre of the
        # circle it is currently driving around.
        R = v / omega
        side = "left" if R > 0 else "right"
        print(f"  path     an arc of radius R = v/w = {R:+.4f} m "
              f"(centre is {abs(R):.4f} m to the {side})\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("w_left", nargs="?", type=float, help="left wheel speed, rad/s")
    parser.add_argument("w_right", nargs="?", type=float, help="right wheel speed, rad/s")
    parser.add_argument("--table", action="store_true",
                        help="print the four canonical cases instead")
    args = parser.parse_args()

    print(f"\nTurtleBot 3 Burger:  r = {WHEEL_RADIUS} m   L = {WHEEL_SEPARATION} m")
    print("v = r(w_R + w_L)/2      w = r(w_R - w_L)/L\n")

    if args.table or args.w_left is None:
        for label, wl, wr in [("Both wheels equal", 10.0, 10.0),
                              ("Right faster than left", 5.0, 10.0),
                              ("Equal and opposite", -10.0, 10.0),
                              ("Left wheel stopped", 0.0, 10.0)]:
            print(f"{label}")
            describe(wl, wr)
    else:
        describe(args.w_left, args.w_right)


if __name__ == "__main__":
    main()
