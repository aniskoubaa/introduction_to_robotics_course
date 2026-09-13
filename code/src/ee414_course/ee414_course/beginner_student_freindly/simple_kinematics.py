#!/usr/bin/env python3
"""Differential drive, as arithmetic. No ROS, no robot, no simulator.

The whole model is the four lines of algebra below. Read them before you
read anything longer.

    ros2 run ee414_course simple_kinematics
"""

r = 0.033      # wheel radius, in metres        (TurtleBot 3 Burger)
L = 0.160      # distance between wheels, metres


def forward(wL, wR):
    """Wheel speeds in (rad/s)  ->  how the BODY moves."""
    v = r * (wR + wL) / 2      # forward speed, m/s
    w = r * (wR - wL) / L      # turn rate, rad/s
    return v, w


def inverse(v, w):
    """How the body should move  ->  the wheel speeds that do it."""
    wL = (v - w * L / 2) / r
    wR = (v + w * L / 2) / r
    return wL, wR


def main(args=None):
    print("\nFORWARD   wheels -> body")
    for wL, wR in [(10, 10), (5, 10), (-10, 10), (0, 10)]:
        v, w = forward(wL, wR)
        print(f"  wL={wL:4}  wR={wR:4}  ->  v={v:+.4f} m/s   w={w:+.4f} rad/s")

    print("\nINVERSE   body -> wheels")
    wL, wR = inverse(0.2, 1.0)
    print(f"  v=0.20  w=1.00  ->  wL={wL:+.2f}   wR={wR:+.2f} rad/s")

    print("\nLook at the last forward line: one wheel stopped.")
    print("The turn radius is v/w = 0.0800 m, which is exactly L/2.")
    print("Stop one wheel and the robot pivots about THAT WHEEL.\n")


if __name__ == "__main__":
    main()
