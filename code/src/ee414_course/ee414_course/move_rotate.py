#!/usr/bin/env python3
# This file is part of the ee414_course package.
#
# EE 414 — Introduction to Robotics. Week 4, slides 20, 13 and 35.
#
# Improved from clean.py in ros2_course_packages
# (Copyright (c) 2023 Anis Koubaa), licensed CC BY-NC-SA 4.0.
"""move() and rotate(): the two primitives everything else is built from.

Works on turtlesim and on TurtleBot 3 without being edited.

    ros2 run ee414_course move_rotate --shape straight --distance 2.0
    ros2 run ee414_course move_rotate --shape rotate --angle 90
    ros2 run ee414_course move_rotate --shape square --distance 2.0
    ros2 run ee414_course move_rotate --robot tb3 --shape square --distance 0.5 \
        --speed 0.15 --turn-rate 0.5

Three things were fixed relative to the original clean.py:

  1. ROTATION MEASUREMENT. The original used

         math.degrees(abs(start_pose.theta - self.pose.theta))

     which breaks the moment theta crosses the +/-pi seam: the measured
     rotation jumps to nearly 360 and rotate() stops far too early. Here it is
     abs(normalize_angle(now - start)). Run `ros2 run ee414_course angle_wrap`
     to watch the original fail.

  2. THE SPEED GUARDS. The original checked `angular_speed_degree > 30` and
     then printed "must be lower than 0.5". The limits now match the robot and
     the message names the number it is enforcing.

  3. MEASURING WITHOUT CORRECTING. The pose is read to report the closing
     error at the end. It is never used to decide what to do next, because
     this is Week 4. Week 5 closes the loop.
"""

import argparse
import math
import time

import rclpy

from ee414_course import graceful
from rclpy.node import Node

from ee414_course.robot_io import RobotDriver
from ee414_course.robot_pose import normalize_angle

# What each robot can actually do. Ask for more and it saturates silently.
LIMITS = {
    "turtle": {"v": 2.0, "w": 2.0},
    "tb3": {"v": 0.22, "w": 2.84},
}


class MoveRotate(Node):

    def __init__(self, robot, rate_hz=20.0):
        super().__init__("move_rotate")
        self.robot = robot
        self.rate_hz = rate_hz
        self.limits = LIMITS[robot]
        self.driver = RobotDriver(self, robot)

    # -- the one loop both primitives are built on -------------------------

    def hold(self, v, omega, seconds):
        """Publish one velocity for a fixed wall-clock time, then stop.

        Pace this on the WALL CLOCK. Pacing it with
        rclpy.spin_once(timeout_sec=period) looks equivalent and is not:
        spin_once returns the moment a callback is ready, and the pose is
        arriving at 62 Hz, so the loop runs far faster than intended and every
        motion finishes short.
        """
        period = 1.0 / self.rate_hz
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline and not graceful.interrupted():
            self.driver.publish(v, omega)
            rclpy.spin_once(self, timeout_sec=0.0)   # drain callbacks, never block
            time.sleep(period)
        self.driver.stop()

    # -- the primitives -----------------------------------------------------

    def move(self, distance, speed):
        """Drive `distance` metres forward (or backward if negative)."""
        speed = abs(speed)
        if speed > self.limits["v"]:
            print(f"  [!] {speed} m/s is above this robot's limit of "
                  f"{self.limits['v']} m/s -- clamping.")
            speed = self.limits["v"]

        seconds = abs(distance) / speed
        direction = math.copysign(speed, distance)
        print(f"  move   {distance:+.3f} m at {speed:.3f} m/s "
              f"-> hold for {seconds:.3f} s")
        self.hold(direction, 0.0, seconds)

    def rotate(self, angle_degrees, rate_rad_s):
        """Turn `angle_degrees` on the spot. Positive is left."""
        rate = abs(rate_rad_s)
        if rate > self.limits["w"]:
            print(f"  [!] {rate} rad/s is above this robot's limit of "
                  f"{self.limits['w']} rad/s -- clamping.")
            rate = self.limits["w"]

        angle = math.radians(angle_degrees)
        seconds = abs(angle) / rate
        direction = math.copysign(rate, angle)

        start_theta = self.driver.pose.theta
        print(f"  rotate {angle_degrees:+.1f} deg at {rate:.3f} rad/s "
              f"-> hold for {seconds:.3f} s")
        self.hold(0.0, direction, seconds)

        # Measure the turn the wrap-safe way. This is the corrected line.
        rclpy.spin_once(self, timeout_sec=0.2)
        turned = abs(normalize_angle(self.driver.pose.theta - start_theta))
        naive = abs(self.driver.pose.theta - start_theta)
        print(f"         turned {math.degrees(turned):.1f} deg "
              f"(the naive subtraction would say "
              f"{math.degrees(naive):.1f} deg)")

    # -- shapes --------------------------------------------------------------

    def square(self, side, speed, turn_rate):
        print(f"  square: 4 sides of {side} m, 4 turns of 90 deg\n")
        for i in range(4):
            if graceful.interrupted():
                break
            print(f"  -- side {i + 1}")
            self.move(side, speed)
            self.rotate(90.0, turn_rate)

    def arc(self, angle_degrees, speed, turn_rate):
        seconds = abs(math.radians(angle_degrees)) / abs(turn_rate)
        R = speed / turn_rate
        print(f"  arc    radius R = v/w = {R:.3f} m, {angle_degrees} deg "
              f"-> hold for {seconds:.3f} s")
        self.hold(speed, turn_rate, seconds)


def run(node, args):
    start = node.driver.pose.copy()
    print(f"\n  start : {start}\n")

    if args.shape == "straight":
        node.move(args.distance, args.speed)
    elif args.shape == "rotate":
        node.rotate(args.angle, args.turn_rate)
    elif args.shape == "arc":
        node.arc(args.angle, args.speed, args.turn_rate)
    elif args.shape == "square":
        node.square(args.distance, args.speed, args.turn_rate)

    if graceful.interrupted():
        print("\n  Ctrl-C: stop sent, nothing left running.\n")
        return

    rclpy.spin_once(node, timeout_sec=0.3)
    end = node.driver.pose
    print(f"\n  end   : {end}")

    gap = start.distance_to(end)
    dtheta = math.degrees(normalize_angle(end.theta - start.theta))
    print(f"  moved : {gap:.4f} m from the start point, "
          f"heading changed by {dtheta:+.1f} deg")

    if args.shape == "square":
        print(f"\n  CLOSING ERROR: {gap:.4f} m, {abs(dtheta):.1f} deg off heading")
        print("  The node never measured anything in order to correct it.")
        print("  Run it twice and you will get two different answers.\n")
    else:
        print()


def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--robot", default="turtle", choices=["turtle", "tb3"])
    parser.add_argument("--shape", default="straight",
                        choices=["straight", "rotate", "arc", "square"])
    parser.add_argument("--distance", type=float, default=2.0, help="metres")
    parser.add_argument("--angle", type=float, default=90.0, help="degrees")
    parser.add_argument("--speed", type=float, default=1.0, help="m/s")
    parser.add_argument("--turn-rate", type=float, default=1.0, help="rad/s")
    parsed, _ = parser.parse_known_args(args=args)

    graceful.init(args)
    node = None
    try:
        node = MoveRotate(parsed.robot)
        if not node.driver.wait_for_pose():
            return
        run(node, parsed)
    finally:
        if node is not None:
            node.driver.stop()
        graceful.shutdown(node)


if __name__ == "__main__":
    main()
