#!/usr/bin/env python3
# This file is part of the ee414_course package.
#
# EE 414 — Introduction to Robotics. Week 4, slide 17.
"""Ask the robot to move sideways, and watch nothing happen.

A Twist has six numbers. A differential-drive robot uses two of them. This
script commands the four it cannot use, one at a time, and reads the pose
before and after each attempt.

The commands are valid. They publish cleanly. No error is raised, because
nothing is wrong with the MESSAGE -- the field exists, the motion does not.

    ros2 run ee414_course nonholonomic
    ros2 run ee414_course nonholonomic --robot tb3

This is the constraint

    xdot * sin(theta) - ydot * cos(theta) = 0

not as a formula to memorise, but as a thing you have seen a robot obey.
"""

import argparse
import time

import rclpy

from ee414_course import graceful
from geometry_msgs.msg import Twist, TwistStamped
from rclpy.node import Node

from ee414_course.robot_io import ROBOTS, RobotDriver, resolve_twist_type

LINE = "-" * 68


class Nonholonomic(Node):

    def __init__(self, robot):
        super().__init__("nonholonomic")
        self.robot = robot
        self.driver = RobotDriver(self, robot)
        self.cmd_topic = ROBOTS[robot]["cmd"]
        self.msg_type = resolve_twist_type(self, self.cmd_topic)
        self.raw_pub = self.create_publisher(self.msg_type, self.cmd_topic, 10)

    def publish_raw(self, **fields):
        """Publish a Twist with arbitrary fields set, including useless ones."""
        if self.msg_type is TwistStamped:
            msg = TwistStamped()
            msg.header.stamp = self.get_clock().now().to_msg()
            twist = msg.twist
        else:
            msg = Twist()
            twist = msg

        for name, value in fields.items():
            part, axis = name.split("_")
            setattr(getattr(twist, part), axis, float(value))
        self.raw_pub.publish(msg)

    def try_field(self, label, seconds=2.0, **fields):
        """Command one field for a while and see whether the pose changes."""
        if graceful.interrupted():
            return
        # Let the robot settle first. The simulator integrates whatever command
        # was last in force for the rest of its timestep, so reading the "before"
        # pose too early catches the tail of the previous test and reports a few
        # centimetres of motion that this test did not cause.
        self.driver.stop()
        for _ in range(6):
            if graceful.interrupted():
                return
            rclpy.spin_once(self, timeout_sec=0.05)
            time.sleep(0.05)
        before = self.driver.pose.copy()

        print(f"\n{LINE}")
        print(f"  {label}")
        print(f"{LINE}")
        print(f"  before : x={before.x:.6f}  y={before.y:.6f}  "
              f"theta={before.theta:.6f}")

        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline and not graceful.interrupted():
            self.publish_raw(**fields)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(0.05)
        self.driver.stop()

        rclpy.spin_once(self, timeout_sec=0.3)
        after = self.driver.pose

        print(f"  after  : x={after.x:.6f}  y={after.y:.6f}  "
              f"theta={after.theta:.6f}")

        moved = before.distance_to(after)
        turned = abs(after.theta - before.theta)
        if moved < 1e-6 and turned < 1e-6:
            print("  result : NOTHING MOVED. Not approximately -- identically.")
        else:
            print(f"  result : moved {moved:.4f} m, turned {turned:.4f} rad")
        return moved, turned


def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--robot", default="turtle", choices=["turtle", "tb3"])
    parsed, _ = parser.parse_known_args(args=args)

    graceful.init(args)
    node = None
    try:
        node = Nonholonomic(parsed.robot)
        if not node.driver.wait_for_pose():
            return

        print("\n  A Twist has six numbers. Let us try them one at a time.")

        node.try_field("linear.y = 2.0   (pure sideways: 'strafe left')",
                       linear_y=2.0)
        node.try_field("linear.z = 2.0   (straight up: 'fly')",
                       linear_z=2.0)
        node.try_field("angular.x = 2.0  (roll)", angular_x=2.0)
        node.try_field("angular.y = 2.0  (pitch)", angular_y=2.0)

        print(f"\n{LINE}")
        print("  Now the two that DO work")
        print(f"{LINE}")
        node.try_field("linear.x = 1.0   (forward)", linear_x=1.0, seconds=1.5)
        node.try_field("angular.z = 1.0  (turn on the spot)",
                       angular_z=1.0, seconds=1.5)

        if graceful.interrupted():
            print("\n  Ctrl-C: stop sent, nothing left running.\n")
            return

        print(f"\n{LINE}")
        print("  Four of the six fields did nothing at all, and ROS 2 never")
        print("  complained. There is nothing wrong with the message: the")
        print("  field exists. There is no wheel arrangement on this robot")
        print("  that can produce that motion.")
        print()
        print("  That is what a nonholonomic constraint is. The robot can")
        print("  still REACH any pose on the floor -- it just cannot go")
        print("  there directly. Parallel parking is the proof.")
        print(f"{LINE}\n")

    finally:
        if node is not None:
            node.driver.stop()
        graceful.shutdown(node)


if __name__ == "__main__":
    main()
