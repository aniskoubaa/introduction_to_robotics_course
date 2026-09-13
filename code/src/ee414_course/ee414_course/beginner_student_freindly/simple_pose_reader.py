#!/usr/bin/env python3
"""The smallest ROS 2 node that reads where the robot is.

Three things, and every subscriber you ever write has the same three:
a node, a subscription, and a callback.

    ros2 run turtlesim turtlesim_node          <- terminal 1
    ros2 run ee414_course simple_pose_reader   <- terminal 2
"""

import math
import signal

import rclpy
from rclpy.node import Node
from rclpy.signals import SignalHandlerOptions
from turtlesim.msg import Pose


class PoseReader(Node):

    def __init__(self):
        super().__init__("simple_pose_reader")                 # 1. the node
        self.count = 0
        self.create_subscription(                              # 2. subscribe
            Pose, "/turtle1/pose", self.on_pose, 10)

    def on_pose(self, msg):                                    # 3. one message
        self.count += 1
        if self.count % 20:            # turtlesim sends 62 a second: show a few
            return
        print(f"  x={msg.x:6.3f}   y={msg.y:6.3f}   "
              f"theta={msg.theta:+.3f} rad = {math.degrees(msg.theta):+7.1f} deg")


def main(args=None):
    # SignalHandlerOptions.NO lets Ctrl-C reach our own `except` below
    # instead of printing twenty lines of ROS traceback.
    rclpy.init(args=args, signal_handler_options=SignalHandlerOptions.NO)
    # Ctrl-C must raise KeyboardInterrupt so the `finally` below runs and
    # the robot is actually stopped. Two things can prevent that, and this
    # line defeats both: rclpy's own handler (turned off above, it kills the
    # context before we can publish a stop) and an inherited SIG_IGN, which
    # is what a script started in the background hands its children.
    signal.signal(signal.SIGINT, signal.default_int_handler)
    node = PoseReader()
    print("\n  Listening on /turtle1/pose. Drive the turtle. Ctrl-C to stop.\n")
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.1)   # wait for a message
    except KeyboardInterrupt:
        print("\n  stopped.\n")
    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    main()
