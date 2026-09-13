#!/usr/bin/env python3
"""The same pose, handed to you two different ways.

Slide reference: "Two Ways ROS 2 Hands You a Pose".

turtlesim/msg/Pose gives you  theta, a float, in radians.
nav_msgs/msg/Odometry gives you a quaternion, and you do the atan2 yourself.

This node subscribes to both and prints whichever is publishing, so the
difference is visible in one terminal rather than described.

    ros2 run ee414_w04_demo pose_watch
"""

import math

import rclpy
from nav_msgs.msg import Odometry
from ee414_w04_demo import graceful
from rclpy.node import Node
from turtlesim.msg import Pose as TurtlePose


def yaw_from_quaternion(q):
    """Extract the heading from a quaternion. The two lines tf2 runs at the edges."""
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


class PoseWatch(Node):

    def __init__(self):
        super().__init__("pose_watch")

        # Both subscriptions are made unconditionally. Only one of them will
        # ever fire, depending on what you started -- and that is the point.
        self.create_subscription(TurtlePose, "/turtle1/pose", self.on_turtle, 10)
        self.create_subscription(Odometry, "/odom", self.on_odom, 10)

        self.count_turtle = 0
        self.count_odom = 0

        self.get_logger().info("Listening on /turtle1/pose AND /odom.")
        self.get_logger().info("Start turtlesim, or TurtleBot 3, and drive it.")
        print()

    def on_turtle(self, msg):
        # One in every 20 messages: turtlesim publishes at 62 Hz and the point
        # is made just as well at 3 Hz.
        self.count_turtle += 1
        if self.count_turtle % 20:
            return
        print(f"  turtlesim/msg/Pose   x={msg.x:6.3f}  y={msg.y:6.3f}  "
              f"theta={msg.theta:+.4f} rad  ({math.degrees(msg.theta):+7.1f} deg)"
              f"   <- handed to you, already an angle")

    def on_odom(self, msg):
        self.count_odom += 1
        if self.count_odom % 10:
            return
        p = msg.pose.pose.position
        q = msg.pose.pose.orientation
        yaw = yaw_from_quaternion(q)
        n = math.sqrt(q.x * q.x + q.y * q.y + q.z * q.z + q.w * q.w)
        print(f"  nav_msgs/Odometry    x={p.x:6.3f}  y={p.y:6.3f}  "
              f"q=({q.x:+.3f},{q.y:+.3f},{q.z:+.3f},{q.w:+.3f})  |q|={n:.6f}")
        print(f"                       atan2 -> yaw={yaw:+.4f} rad "
              f"({math.degrees(yaw):+7.1f} deg)   <- you did the conversion")


def main(args=None):
    graceful.init(args)
    node = PoseWatch()
    try:
        while rclpy.ok() and not graceful.interrupted():
            rclpy.spin_once(node, timeout_sec=0.1)
    finally:
        graceful.shutdown(node)


if __name__ == "__main__":
    main()
