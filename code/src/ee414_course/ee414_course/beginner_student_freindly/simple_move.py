#!/usr/bin/env python3
"""Open loop: drive for distance / speed seconds, then stop.

The whole control law is one division. Nothing in this file ever asks
where the robot actually is -- that is what OPEN LOOP means.

    ros2 run turtlesim turtlesim_node        <- terminal 1
    ros2 run ee414_course simple_move        <- terminal 2
"""

import signal
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.signals import SignalHandlerOptions

DISTANCE = 2.0      # metres we want to travel
SPEED = 1.0         # metres per second


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
    node = Node("simple_move")
    pub = node.create_publisher(Twist, "/turtle1/cmd_vel", 10)
    time.sleep(1.0)

    seconds = DISTANCE / SPEED            # <-- THE ENTIRE CONTROL LAW
    print(f"\n  {DISTANCE} m at {SPEED} m/s  ->  hold for {seconds:.2f} s\n")

    msg = Twist()
    msg.linear.x = SPEED

    try:
        deadline = time.time() + seconds
        while time.time() < deadline:
            pub.publish(msg)              # a topic does not latch: keep sending
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        stop(pub)

    print("  Stopped. Did it really travel 2 m? Nothing here checked.")
    print("  Run it twice and compare. See simple_go_to_goal.py.\n")
    rclpy.shutdown()


if __name__ == "__main__":
    main()
