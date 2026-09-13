#!/usr/bin/env python3
"""Ask the turtle to move sideways. Watch nothing happen.

A Twist carries six numbers. A wheeled robot uses two of them. The other
four are perfectly legal to send and do nothing at all -- and ROS 2 never
complains, because nothing is wrong with the MESSAGE.

    ros2 run turtlesim turtlesim_node               <- terminal 1
    ros2 topic echo /turtle1/pose --once            <- write the numbers down
    ros2 run ee414_course simple_nonholonomic
    ros2 topic echo /turtle1/pose --once            <- identical, to the digit
"""

import signal
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.signals import SignalHandlerOptions


def stop(pub):
    """An empty Twist is a full stop. A topic does not retry, so say it
    more than once: one dropped message leaves the robot driving away."""
    for _ in range(5):
        pub.publish(Twist())
        time.sleep(0.05)


def main(args=None):
    rclpy.init(args=args, signal_handler_options=SignalHandlerOptions.NO)
    # Ctrl-C must raise KeyboardInterrupt so the `finally` below runs and
    # the robot is actually stopped. Two things can prevent that, and this
    # line defeats both: rclpy's own handler (turned off above, it kills the
    # context before we can publish a stop) and an inherited SIG_IGN, which
    # is what a script started in the background hands its children.
    signal.signal(signal.SIGINT, signal.default_int_handler)
    node = Node("simple_nonholonomic")
    pub = node.create_publisher(Twist, "/turtle1/cmd_vel", 10)
    time.sleep(1.0)                       # let the connection be made

    msg = Twist()
    msg.linear.y = 2.0                    # SIDEWAYS. The field exists.

    print("\n  publishing linear.y = 2.0 for 3 seconds ...")
    try:
        for _ in range(30):
            pub.publish(msg)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        stop(pub)                         # always send a stop

    print("  The turtle did not move. Not approximately -- identically.")
    print("  No error was raised anywhere.\n")
    print("  There is no arrangement of two wheels that drives sideways.")
    print("  That is the nonholonomic constraint:")
    print("      x' sin(theta) - y' cos(theta) = 0\n")
    rclpy.shutdown()


if __name__ == "__main__":
    main()
