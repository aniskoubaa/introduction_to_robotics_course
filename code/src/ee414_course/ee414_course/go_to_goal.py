#!/usr/bin/env python3
# This file is part of the ee414_course package.
#
# EE 414 — Introduction to Robotics. Week 4 slide 38, and the bridge to Week 5.
#
# Improved from go_to_goal() in clean.py, ros2_course_packages
# (Copyright (c) 2023 Anis Koubaa), licensed CC BY-NC-SA 4.0.
"""Closed loop: measure the error, then act on it. Contrast with move_rotate.

Run move_rotate first and watch the square fail to close. Then run this and
watch the robot arrive, from wherever it happens to be, every time.

    ros2 run ee414_course go_to_goal --x 8.0 --y 8.0
    ros2 run ee414_course go_to_goal --robot tb3 --x 1.0 --y 0.5

The difference from every other script in this package is one line:

    error = goal - where_I_actually_am        <- it looks

Everything else in Week 4 computes a duration up front and hopes. This reads
the pose on every cycle and lets the error decide the speed. That is Week 5's
whole subject, and this is a preview of it.

What changed from the original go_to_goal():

  1. THE HEADING ERROR IS WRAPPED. The original computed

         angular_speed = (desired_angle_goal - self.pose.get_theta()) * p_gain

     With the goal behind the robot that difference can exceed pi, and the
     robot then turns the long way round -- sometimes spinning almost a full
     circle to make a small correction. Here it is normalize_angle(...).

  2. THE SPEEDS ARE CLAMPED. An unclamped P controller asks for whatever the
     error times the gain happens to be, which on a TurtleBot 3 is usually
     several times what the motors have. See kinematics.py for what saturation
     does to the shape of the path.

  3. IT DRIVES FORWARD ONLY WHEN ROUGHLY FACING THE GOAL. Otherwise a large
     heading error and a large distance error fight each other and the robot
     drives a long curve instead of turning first.

  4. IT GIVES UP. The original loop had no timeout, so an unreachable goal
     meant a node that never returned.
"""

import argparse
import math
import time

import rclpy

from ee414_course import graceful
from rclpy.node import Node

from ee414_course.robot_io import RobotDriver
from ee414_course.robot_pose import RobotPose, normalize_angle

LIMITS = {
    "turtle": {"v": 2.0, "w": 2.0},
    "tb3": {"v": 0.22, "w": 2.84},
}


class GoToGoal(Node):

    def __init__(self, robot, goal, tolerance):
        super().__init__("go_to_goal")
        self.robot = robot
        self.goal = goal
        self.tolerance = tolerance
        self.limits = LIMITS[robot]
        self.driver = RobotDriver(self, robot)

        # P gains. Bigger means a more urgent response to the same error.
        self.k_linear = 1.0
        self.k_angular = 4.0

    def clamp(self, value, limit):
        return max(-limit, min(limit, value))

    def run(self, timeout=60.0):
        start = self.driver.pose.copy()
        print(f"\n  start : {start}")
        print(f"  goal  : x={self.goal.x:.3f}  y={self.goal.y:.3f}")
        print(f"  stop when within {self.tolerance} m\n")

        deadline = time.monotonic() + timeout
        ticks = 0

        while time.monotonic() < deadline and not graceful.interrupted():
            rclpy.spin_once(self, timeout_sec=0.05)
            pose = self.driver.pose

            # ---- THE CLOSED LOOP: look, then decide ----------------------
            distance = pose.distance_to(self.goal)
            heading_to_goal = pose.angle_to(self.goal)
            heading_error = normalize_angle(heading_to_goal - pose.theta)
            # --------------------------------------------------------------

            if distance < self.tolerance:
                self.driver.stop()
                print(f"\n  Goal reached after {ticks} cycles.")
                print(f"  end   : {pose}")
                print(f"  final distance to goal: {distance:.4f} m")
                print("\n  It arrived because it kept looking. Nothing here")
                print("  computed a duration in advance.\n")
                return True

            omega = self.clamp(self.k_angular * heading_error, self.limits["w"])

            # Turn first if badly misaligned; otherwise a big heading error and
            # a big distance error fight, and the robot swings out on a curve.
            if abs(heading_error) > math.radians(20.0):
                v = 0.0
            else:
                v = self.clamp(self.k_linear * distance, self.limits["v"])

            self.driver.publish(v, omega)

            ticks += 1
            if ticks % 20 == 0:
                print(f"  distance {distance:6.3f} m   "
                      f"heading error {math.degrees(heading_error):+7.1f} deg   "
                      f"-> v={v:.3f}  w={omega:+.3f}")

            time.sleep(0.05)

        self.driver.stop()
        if graceful.interrupted():
            # Do not report a timeout that did not happen.
            print("\n  Ctrl-C: stop sent, nothing left running.\n")
            return False
        print(f"\n  Gave up after {timeout:.0f} s. "
              f"Still {self.driver.pose.distance_to(self.goal):.3f} m away.")
        print("  A goal outside the arena, or a robot that cannot reach it.\n")
        return False


def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--robot", default="turtle", choices=["turtle", "tb3"])
    parser.add_argument("--x", type=float, default=8.0)
    parser.add_argument("--y", type=float, default=8.0)
    parser.add_argument("--tolerance", type=float, default=0.2, help="metres")
    parsed, _ = parser.parse_known_args(args=args)

    graceful.init(args)
    node = None
    try:
        node = GoToGoal(parsed.robot, RobotPose(parsed.x, parsed.y), parsed.tolerance)
        if not node.driver.wait_for_pose():
            return
        node.run()
    finally:
        if node is not None:
            node.driver.stop()
        graceful.shutdown(node)


if __name__ == "__main__":
    main()
