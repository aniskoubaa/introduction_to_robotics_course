#!/usr/bin/env python3
"""Inverse kinematics: the body velocity you asked for, turned into wheel speeds.

Slide reference: "Inverse Kinematics: Body to Wheels".

    w_L = (v - w*L/2) / r
    w_R = (v + w*L/2) / r

This is the direction the robot actually works in. You publish a Twist; the
driver solves these two lines; the motors get numbers. When you ask for
something the motors cannot do, this is where you find out.

    python3 body_to_wheels.py 0.2 1.0
    python3 body_to_wheels.py 0.5 3.0     # asks for too much, and says so
"""

import argparse
import math

WHEEL_RADIUS = 0.033      # r, metres
WHEEL_SEPARATION = 0.160  # L, metres

# The Burger's motors saturate here. Past this the robot does not refuse --
# it just quietly does something other than what you asked.
MAX_WHEEL_SPEED = 14.0    # rad/s


def inverse_kinematics(v, omega, r=WHEEL_RADIUS, L=WHEEL_SEPARATION):
    """Body (v, omega) -> wheel angular speeds (w_left, w_right) in rad/s."""
    w_left = (v - omega * L / 2.0) / r
    w_right = (v + omega * L / 2.0) / r
    return w_left, w_right


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("v", type=float, help="forward speed, m/s (Twist linear.x)")
    parser.add_argument("omega", type=float, help="turning rate, rad/s (Twist angular.z)")
    args = parser.parse_args()

    w_left, w_right = inverse_kinematics(args.v, args.omega)

    print(f"\nTurtleBot 3 Burger:  r = {WHEEL_RADIUS} m   L = {WHEEL_SEPARATION} m")
    print("w_L = (v - wL/2)/r      w_R = (v + wL/2)/r\n")
    print(f"  you asked for   v = {args.v:+.4f} m/s     w = {args.omega:+.4f} rad/s")
    print(f"  wheels must do  w_L = {w_left:+7.2f} rad/s   w_R = {w_right:+7.2f} rad/s")

    fastest = max(abs(w_left), abs(w_right))
    if fastest > MAX_WHEEL_SPEED:
        # Saturation does not scale v and omega equally, so the robot turns
        # differently from the command -- the single most common reason a
        # square drawn open loop comes out as something else.
        scale = MAX_WHEEL_SPEED / fastest
        print(f"\n  *** TOO FAST. The motors stop at {MAX_WHEEL_SPEED} rad/s. ***")
        print(f"  The fastest wheel is asked for {fastest:.2f} rad/s, "
              f"which is {1 / scale:.2f} times what it has.")
        print(f"  Ask instead for   v = {args.v * scale:+.4f} m/s   "
              f"w = {args.omega * scale:+.4f} rad/s   (both scaled by {scale:.3f})")
    else:
        headroom = 100.0 * fastest / MAX_WHEEL_SPEED
        print(f"\n  Within limits: the busiest wheel is at {headroom:.0f}% "
              f"of its {MAX_WHEEL_SPEED} rad/s maximum.")

    # Round-trip check. If these two lines do not reproduce the input, the
    # algebra on the slide is wrong -- and it is not.
    v_back = WHEEL_RADIUS * (w_right + w_left) / 2.0
    w_back = WHEEL_RADIUS * (w_right - w_left) / WHEEL_SEPARATION
    print(f"\n  check: feed those wheels back into the forward model ->"
          f" v = {v_back:+.4f}, w = {w_back:+.4f}")
    assert math.isclose(v_back, args.v, abs_tol=1e-9)
    assert math.isclose(w_back, args.omega, abs_tol=1e-9)
    print("  the two models are inverses of each other, exactly.\n")


if __name__ == "__main__":
    main()
