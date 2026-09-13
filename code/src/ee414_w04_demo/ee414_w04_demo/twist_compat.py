#!/usr/bin/env python3
"""One topic, two message types, and a failure that makes no noise at all.

`/cmd_vel` has carried geometry_msgs/msg/Twist for years. On ROS 2 Jazzy the
TurtleBot 3 Gazebo bridge publishes geometry_msgs/msg/TwistStamped instead --
the same twist, with a header bolted on so the command can be timestamped.

If you publish the wrong one of those two, ROS 2 does not complain. The types
do not match, so no connection is ever made; your publisher succeeds, your
messages go nowhere, and the robot sits still. There is no error to read.

So: ask the graph which type the topic actually carries, and send that.

    ros2 topic type /cmd_vel          # the same question, from the terminal
"""

import time

from geometry_msgs.msg import Twist, TwistStamped


def resolve_twist_type(node, topic, timeout=3.0):
    """Return the message class `topic` carries, or Twist if nobody says.

    The graph takes a moment to populate after a node starts, so this polls
    rather than asking once and giving up.
    """
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

    # Nothing is bound to the topic yet -- this is the turtlesim case, where
    # our publisher is the first one there. Twist is the right default.
    return Twist


class CmdVelPublisher:
    """Publishes (v, omega) on `topic`, in whichever type that topic uses."""

    def __init__(self, node, topic, queue=10):
        self.node = node
        self.topic = topic
        self.msg_type = resolve_twist_type(node, topic)
        self.stamped = self.msg_type is TwistStamped
        self.pub = node.create_publisher(self.msg_type, topic, queue)

        node.get_logger().info(
            f"{topic} carries {self.msg_type.__module__.split('.')[0]}"
            f"/msg/{self.msg_type.__name__} -- publishing that.")

    def publish(self, v=0.0, omega=0.0):
        if self.stamped:
            msg = TwistStamped()
            msg.header.stamp = self.node.get_clock().now().to_msg()
            msg.twist.linear.x = float(v)
            msg.twist.angular.z = float(omega)
        else:
            msg = Twist()
            msg.linear.x = float(v)
            msg.angular.z = float(omega)
        self.pub.publish(msg)

    def stop(self):
        self.publish(0.0, 0.0)


def twist_of(msg):
    """Read the twist out of either message type."""
    return msg.twist if hasattr(msg, "twist") else msg
