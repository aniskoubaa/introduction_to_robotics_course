#!/usr/bin/env python3
"""Closed loop: look at the pose, then decide. Compare with simple_square.py.

simple_square.py computes durations in advance and hopes. This one reads
where the robot IS on every cycle and lets the error choose the speed.
It arrives from wherever it starts, every time.

    ros2 run turtlesim turtlesim_node          <- terminal 1
    ros2 run ee414_course simple_go_to_goal    <- terminal 2
"""

import math
import signal
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.signals import SignalHandlerOptions
from turtlesim.msg import Pose

GOAL_X, GOAL_Y = 8.0, 8.0
TOLERANCE = 0.2          # metres: close enough
K_LINEAR = 1.0           # P gains: how hard to react to the error
K_ANGULAR = 4.0
MAX_V, MAX_W = 2.0, 2.0  # no motor is infinitely fast: clamp what you ask for


def normalize(angle):
    """Fold an angle into -pi .. +pi. See simple_angle_wrap.py."""
    return math.atan2(math.sin(angle), math.cos(angle))


def clamp(value, limit):
    """Never ask for more than the robot has."""
    return max(-limit, min(limit, value))


class GoToGoal(Node):

    def __init__(self):
        super().__init__("simple_go_to_goal")
        self.pose = None
        self.arrived = False
        self.pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.create_subscription(Pose, "/turtle1/pose", self.on_pose, 10)
        self.create_timer(0.1, self.control)     # 10 times a second

    def on_pose(self, msg):
        self.pose = msg

    def control(self):
        if self.pose is None or self.arrived:
            return

        # ---- THE CLOSED LOOP: three lines, and all of them LOOK ----------
        dx = GOAL_X - self.pose.x
        dy = GOAL_Y - self.pose.y
        distance = math.hypot(dx, dy)
        heading_error = normalize(math.atan2(dy, dx) - self.pose.theta)
        # ------------------------------------------------------------------

        if distance < TOLERANCE:
            self.pub.publish(Twist())
            print(f"\n  Arrived. {distance:.3f} m from the goal.")
            print("  It got here by looking, not by timing.\n")
            self.arrived = True
            return

        msg = Twist()
        msg.angular.z = clamp(K_ANGULAR * heading_error, MAX_W)   # P controller
        # Turn first if badly aimed, otherwise the two errors fight.
        if abs(heading_error) < math.radians(20):
            msg.linear.x = clamp(K_LINEAR * distance, MAX_V)
        self.pub.publish(msg)
        print(f"  distance {distance:5.2f} m   "
              f"heading error {math.degrees(heading_error):+6.1f} deg")


def main(args=None):
    rclpy.init(args=args, signal_handler_options=SignalHandlerOptions.NO)
    # Ctrl-C must raise KeyboardInterrupt so the `finally` below runs and
    # the robot is actually stopped. Two things can prevent that, and this
    # line defeats both: rclpy's own handler (turned off above, it kills the
    # context before we can publish a stop) and an inherited SIG_IGN, which
    # is what a script started in the background hands its children.
    signal.signal(signal.SIGINT, signal.default_int_handler)
    node = GoToGoal()
    print(f"\n  Driving to ({GOAL_X}, {GOAL_Y}).\n")
    try:
        while rclpy.ok() and not node.arrived:
            rclpy.spin_once(node, timeout_sec=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        # A topic does not retry. One dropped stop message and the robot
        # drives away with nothing left to tell it otherwise -- so say it
        # five times, and give the last one time to leave.
        for _ in range(5):
            node.pub.publish(Twist())
            time.sleep(0.05)
        rclpy.shutdown()


if __name__ == "__main__":
    main()
