#!/usr/bin/env python3
"""An open-loop square: 4 sides and 4 turns, all of them timed.

Same idea as simple_move.py, four times, plus turns. Every duration is
distance / speed. Watch the square fail to close -- and note that the
node has no idea that it did.

    ros2 run turtlesim turtlesim_node        <- terminal 1
    ros2 run ee414_course simple_square      <- terminal 2
"""

import math
import signal
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.signals import SignalHandlerOptions

SIDE = 2.0          # metres
SPEED = 1.0         # m/s
TURN = 1.0          # rad/s


def stop(pub):
    """An empty Twist is a full stop. A topic does not retry, so say it
    more than once: one dropped message leaves the robot driving away."""
    for _ in range(5):
        pub.publish(Twist())
        time.sleep(0.05)


def hold(pub, v, w, seconds):
    """Publish one velocity for `seconds`, then stop."""
    msg = Twist()
    msg.linear.x = v
    msg.angular.z = w
    deadline = time.time() + seconds
    while time.time() < deadline:
        pub.publish(msg)
        time.sleep(0.05)
    stop(pub)


def main(args=None):
    rclpy.init(args=args, signal_handler_options=SignalHandlerOptions.NO)
    # Ctrl-C must raise KeyboardInterrupt so the `finally` below runs and
    # the robot is actually stopped. Two things can prevent that, and this
    # line defeats both: rclpy's own handler (turned off above, it kills the
    # context before we can publish a stop) and an inherited SIG_IGN, which
    # is what a script started in the background hands its children.
    signal.signal(signal.SIGINT, signal.default_int_handler)
    node = Node("simple_square")
    pub = node.create_publisher(Twist, "/turtle1/cmd_vel", 10)
    time.sleep(1.0)

    try:
        for i in range(4):
            print(f"  side {i + 1}: forward {SIDE} m, then turn 90 deg")
            hold(pub, SPEED, 0.0, SIDE / SPEED)              # go straight
            hold(pub, 0.0, TURN, math.radians(90) / TURN)    # turn in place
    except KeyboardInterrupt:
        pass
    finally:
        stop(pub)

    print("\n  Look at the window: the turtle is NOT back where it started.")
    print("  Four timed sides and four timed turns, and the error added up.")
    print("  Nothing measured anything, so nothing could correct it.\n")
    rclpy.shutdown()


if __name__ == "__main__":
    main()
