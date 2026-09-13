#!/usr/bin/env python3
# This file is part of the ee414_course package.
#
# EE 414 — Introduction to Robotics. Week 4, slides 20-23.
"""The differential-drive model, as arithmetic. No ROS, no simulator.

Run this before you run anything that moves. The whole model is four lines of
algebra, and it is worth seeing them as four lines of algebra before they are
buried inside a node.

    FORWARD  (wheels -> body)        INVERSE  (body -> wheels)
    v = r (wR + wL) / 2              wL = (v - w L / 2) / r
    w = r (wR - wL) / L              wR = (v + w L / 2) / r

Try it:

    ros2 run ee414_course kinematics                 # the four classic cases
    ros2 run ee414_course kinematics --wheels 0 10   # left wheel stopped
    ros2 run ee414_course kinematics --body 0.2 1.0  # what the wheels must do
"""

import argparse
import math

# TurtleBot 3 Burger. These are the two numbers the whole lecture uses, and
# the same two that go into the URDF later in the week.
WHEEL_RADIUS = 0.033        # r, metres
WHEEL_SEPARATION = 0.160    # L, metres
MAX_WHEEL_SPEED = 14.0      # rad/s, where the Burger's motors give up

LINE = "-" * 70


def forward_kinematics(w_left, w_right, r=WHEEL_RADIUS, L=WHEEL_SEPARATION):
    """Two wheel speeds (rad/s) in, one body velocity (m/s, rad/s) out."""
    v = r * (w_right + w_left) / 2.0
    omega = r * (w_right - w_left) / L
    return v, omega


def inverse_kinematics(v, omega, r=WHEEL_RADIUS, L=WHEEL_SEPARATION):
    """A body velocity in, the two wheel speeds it needs out."""
    w_left = (v - omega * L / 2.0) / r
    w_right = (v + omega * L / 2.0) / r
    return w_left, w_right


def describe_path(v, omega):
    """Say what shape the robot draws, given v and omega.

    The shape follows from those two numbers alone -- that is the whole reason
    the model is useful.
    """
    if abs(omega) < 1e-9 and abs(v) < 1e-9:
        return "stopped"
    if abs(omega) < 1e-9:
        return "a straight line"
    if abs(v) < 1e-9:
        return "a spin in place (the centre of the turn is the robot itself)"

    # R = v / omega is the distance to the Instantaneous Centre of Curvature:
    # the point the robot is, right now, driving around.
    R = v / omega
    side = "left" if R > 0 else "right"
    return (f"an arc of radius R = v/w = {R:+.4f} m "
            f"(the centre is {abs(R):.4f} m to the {side})")


def show_wheels(w_left, w_right):
    """Print one forward-kinematics case the way you would read it aloud."""
    v, omega = forward_kinematics(w_left, w_right)
    print(f"  wheels   wL = {w_left:7.2f} rad/s     wR = {w_right:7.2f} rad/s")
    print(f"  body     v  = {v:7.4f} m/s       w  = {omega:7.4f} rad/s "
          f"({math.degrees(omega):6.1f} deg/s)")
    print(f"  path     {describe_path(v, omega)}")
    print()


def show_body(v, omega):
    """Print one inverse-kinematics case, and check it round-trips."""
    w_left, w_right = inverse_kinematics(v, omega)
    print(f"  you ask for     v  = {v:+.4f} m/s       w  = {omega:+.4f} rad/s")
    print(f"  wheels must do  wL = {w_left:+7.2f} rad/s     wR = {w_right:+7.2f} rad/s")

    fastest = max(abs(w_left), abs(w_right))
    if fastest > MAX_WHEEL_SPEED:
        # A real robot does not refuse an impossible command. It saturates,
        # and then drives something other than what you asked for -- which is
        # the most common reason an open-loop square comes out crooked.
        scale = MAX_WHEEL_SPEED / fastest
        print()
        print(f"  *** TOO FAST: the motors stop at {MAX_WHEEL_SPEED} rad/s ***")
        print(f"  The busiest wheel is asked for {fastest:.2f} rad/s, "
              f"{1 / scale:.2f} times what it has.")
        print(f"  Ask instead for v = {v * scale:+.4f}, w = {omega * scale:+.4f} "
              f"(scale BOTH by {scale:.3f}, or the shape changes)")
    else:
        print(f"  Within limits: the busiest wheel is at "
              f"{100.0 * fastest / MAX_WHEEL_SPEED:.0f}% of maximum.")

    # Feed the answer back through the forward model. If this does not give
    # the input back, one of the two formulas above is wrong.
    v_back, w_back = forward_kinematics(w_left, w_right)
    print(f"\n  check: those wheels, through the forward model, give "
          f"v = {v_back:+.4f}, w = {w_back:+.4f}")
    assert math.isclose(v_back, v, abs_tol=1e-9)
    assert math.isclose(w_back, omega, abs_tol=1e-9)
    print("  the two models are exact inverses of each other.")
    print()


def main(args=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--wheels", nargs=2, type=float, metavar=("wL", "wR"),
                        help="forward: two wheel speeds in rad/s")
    parser.add_argument("--body", nargs=2, type=float, metavar=("v", "w"),
                        help="inverse: forward speed m/s and turn rate rad/s")
    parsed = parser.parse_args(args=args)

    print()
    print(LINE)
    print(f"TurtleBot 3 Burger:   r = {WHEEL_RADIUS} m      L = {WHEEL_SEPARATION} m")
    print(LINE)
    print()

    if parsed.wheels:
        print("FORWARD KINEMATICS   v = r(wR+wL)/2    w = r(wR-wL)/L\n")
        show_wheels(*parsed.wheels)
        return

    if parsed.body:
        print("INVERSE KINEMATICS   wL = (v - wL/2)/r    wR = (v + wL/2)/r\n")
        show_body(*parsed.body)
        return

    # No arguments: walk the four cases the slides draw.
    print("FORWARD KINEMATICS   v = r(wR+wL)/2    w = r(wR-wL)/L\n")
    for label, wl, wr in [("1. Both wheels the same speed", 10.0, 10.0),
                          ("2. Right wheel faster than left", 5.0, 10.0),
                          ("3. Equal and opposite", -10.0, 10.0),
                          ("4. Left wheel stopped", 0.0, 10.0)]:
        print(label)
        show_wheels(wl, wr)

    print(LINE)
    print("Look at case 4 again. The radius is 0.0800 m, which is exactly L/2.")
    print("Stop one wheel and the robot pivots about that wheel -- not about")
    print("its own centre. The arithmetic said so before the robot did.")
    print(LINE)
    print()

    print("INVERSE KINEMATICS   wL = (v - wL/2)/r    wR = (v + wL/2)/r\n")
    print("A reasonable request:")
    show_body(0.2, 1.0)
    print("Asking for more than the motors have:")
    show_body(0.5, 3.0)


if __name__ == "__main__":
    main()
