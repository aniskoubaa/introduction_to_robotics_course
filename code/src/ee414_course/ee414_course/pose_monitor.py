#!/usr/bin/env python3
# This file is part of the ee414_course package.
#
# EE 414 — Introduction to Robotics. Week 4, slides 9, 10 and 12.
"""The same pose, handed to you two different ways.

turtlesim/msg/Pose gives you `theta`: a float, in radians, ready to use.
nav_msgs/msg/Odometry gives you a quaternion, and you do the atan2 yourself.

This node subscribes to BOTH at once and prints whichever is publishing, so
the difference is something you watch rather than something you are told.

    ros2 run ee414_course pose_monitor

Start turtlesim and drive it, then start TurtleBot 3 and drive that, without
restarting this node. Same robot pose, two shapes of message.
"""

import argparse
import math

import rclpy

from ee414_course import graceful
from nav_msgs.msg import Odometry
from rclpy.node import Node
from turtlesim.msg import Pose as TurtlePose

from ee414_course.robot_pose import yaw_from_quaternion


class PoseMonitor(Node):

    def __init__(self, every):
        super().__init__("pose_monitor")
        self.every = every
        self.n_turtle = 0
        self.n_odom = 0

        # Both subscriptions are made unconditionally. Only one of them will
        # fire, depending on what you have running -- and that is the point.
        self.create_subscription(TurtlePose, "/turtle1/pose", self.on_turtle, 10)
        self.create_subscription(Odometry, "/odom", self.on_odom, 10)

        print()
        print("  Listening on /turtle1/pose AND /odom.")
        print("  Start a simulator and drive it.\n")

    def on_turtle(self, msg):
        self.n_turtle += 1
        if self.n_turtle % self.every:
            return
        print(f"  turtlesim/msg/Pose  x={msg.x:6.3f}  y={msg.y:6.3f}  "
              f"theta={msg.theta:+.4f} rad ({math.degrees(msg.theta):+7.1f} deg)")
        print("                      ^ one float. Nothing to convert.")

    def on_odom(self, msg):
        self.n_odom += 1
        if self.n_odom % self.every:
            return
        p = msg.pose.pose.position
        q = msg.pose.pose.orientation
        yaw = yaw_from_quaternion(q)
        norm = math.sqrt(q.x * q.x + q.y * q.y + q.z * q.z + q.w * q.w)

        print(f"  nav_msgs/Odometry   x={p.x:6.3f}  y={p.y:6.3f}  "
              f"q=({q.x:+.3f}, {q.y:+.3f}, {q.z:+.3f}, {q.w:+.3f})")
        print(f"                      |q| = {norm:.6f}  "
              f"<- always 1, that is the constraint")
        print(f"                      atan2 -> yaw = {yaw:+.4f} rad "
              f"({math.degrees(yaw):+7.1f} deg)  <- you did this")


def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--every", type=int, default=20,
                        help="print one message in every N (default 20)")
    parsed, _ = parser.parse_known_args(args=args)

    graceful.init(args)
    node = PoseMonitor(max(1, parsed.every))
    try:
        while rclpy.ok() and not graceful.interrupted():
            rclpy.spin_once(node, timeout_sec=0.1)
    finally:
        graceful.shutdown(node)


if __name__ == "__main__":
    main()
