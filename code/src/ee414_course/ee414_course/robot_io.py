# This file is part of the ee414_course package.
#
# EE 414 — Introduction to Robotics. Week 4.
"""Talking to the turtle and to the robot with the same code.

Two annoyances sit between a beginner's script and a robot that moves, and
neither of them announces itself:

  1. The topic is `/turtle1/cmd_vel` on turtlesim and `/cmd_vel` on a
     TurtleBot 3.

  2. On ROS 2 Jazzy the TurtleBot 3 Gazebo bridge carries
     geometry_msgs/msg/TwistStamped, while turtlesim carries
     geometry_msgs/msg/Twist. Publish the wrong one of those two and ROS 2
     says NOTHING AT ALL. The types do not match, so no connection is ever
     made; your publisher reports success and the robot sits perfectly still.
     There is no error anywhere to read.

     Check it yourself from a terminal:   ros2 topic type /cmd_vel

This module asks the graph which type the topic really carries and sends that.
Every motion script in this package uses it, which is why they all run on both
robots without being edited.
"""

import time

import rclpy
from geometry_msgs.msg import Twist, TwistStamped
from nav_msgs.msg import Odometry
from turtlesim.msg import Pose as TurtlePose

from ee414_course import graceful
from ee414_course.robot_pose import RobotPose, yaw_from_quaternion

# Which topics each robot uses.
ROBOTS = {
    "turtle": {"cmd": "/turtle1/cmd_vel", "pose": "/turtle1/pose"},
    "tb3": {"cmd": "/cmd_vel", "pose": "/odom"},
}


def resolve_twist_type(node, topic, timeout=3.0):
    """Ask the graph which message type `topic` carries."""
    topic = topic if topic.startswith("/") else "/" + topic
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        for name, types in node.get_topic_names_and_types():
            if name == topic and types:
                if "geometry_msgs/msg/TwistStamped" in types:
                    return TwistStamped
                if "geometry_msgs/msg/Twist" in types:
                    return Twist
        time.sleep(0.1)

    # Nobody is bound to the topic yet, which is the turtlesim case: our
    # publisher gets there first. Twist is the right default.
    return Twist


class RobotDriver:
    """A velocity publisher and a pose subscriber, for either robot.

    Use it like this:

        driver = RobotDriver(node, "turtle")
        driver.wait_for_pose()
        driver.publish(0.2, 0.0)      # forward 0.2 m/s, no turning
        print(driver.pose)
    """

    def __init__(self, node, robot="turtle"):
        if robot not in ROBOTS:
            raise ValueError(f"robot must be 'turtle' or 'tb3', not {robot!r}")

        self.node = node
        self.robot = robot
        self.cmd_topic = ROBOTS[robot]["cmd"]
        self.pose_topic = ROBOTS[robot]["pose"]
        self.pose = None           # a RobotPose, once the first message lands

        self.msg_type = resolve_twist_type(node, self.cmd_topic)
        self.stamped = self.msg_type is TwistStamped
        self.publisher = node.create_publisher(self.msg_type, self.cmd_topic, 10)

        if robot == "tb3":
            node.create_subscription(Odometry, self.pose_topic, self._on_odom, 10)
        else:
            node.create_subscription(TurtlePose, self.pose_topic, self._on_turtle, 10)

        node.get_logger().info(
            f"{self.cmd_topic} carries geometry_msgs/msg/{self.msg_type.__name__} "
            f"-- publishing that.")

    # -- incoming ----------------------------------------------------------

    def _on_turtle(self, msg):
        self.pose = RobotPose(msg.x, msg.y, msg.theta)

    def _on_odom(self, msg):
        p = msg.pose.pose.position
        self.pose = RobotPose(p.x, p.y, yaw_from_quaternion(msg.pose.pose.orientation))

    def wait_for_pose(self, timeout=10.0):
        """Block until the first pose arrives. Returns True if it did."""
        waited = 0.0
        while self.pose is None and waited < timeout and not graceful.interrupted():
            rclpy.spin_once(self.node, timeout_sec=0.1)
            waited += 0.1
        if self.pose is None:
            self.node.get_logger().error(
                f"No pose on {self.pose_topic}. Is the simulator running?")
            return False
        return True

    # -- outgoing ----------------------------------------------------------

    def publish(self, v=0.0, omega=0.0):
        """Send one velocity command: v forward (m/s), omega turning (rad/s)."""
        if self.stamped:
            msg = TwistStamped()
            msg.header.stamp = self.node.get_clock().now().to_msg()
            msg.twist.linear.x = float(v)
            msg.twist.angular.z = float(omega)
        else:
            msg = Twist()
            msg.linear.x = float(v)
            msg.angular.z = float(omega)
        self.publisher.publish(msg)

    def stop(self):
        """Stop, and say so more than once.

        A topic does not retry. One dropped stop message leaves the robot
        driving away with nothing left to tell it otherwise.

        Note there is no spin_once in here. Publishing does not need the
        executor, and stop() gets called from inside timer callbacks -- where
        spinning raises "Executor is already spinning".

        The rclpy.ok() guard is for Ctrl-C: publishing on a context that has
        already been shut down raises RCLError, and a traceback is the last
        thing a demonstration needs.
        """
        if not rclpy.ok():
            return
        for _ in range(5):
            self.publish(0.0, 0.0)
            time.sleep(0.02)
