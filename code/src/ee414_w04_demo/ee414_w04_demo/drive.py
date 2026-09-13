#!/usr/bin/env python3
"""Open-loop motion: pick a speed, hold it for a time, hope.

Slide reference: the differential-drive model, and "Open Loop, Defined".

Every primitive here is the same three lines:

    duration = how_far / how_fast
    publish the Twist for that long
    publish a zero Twist to stop

Nothing is ever measured in order to decide what to do next. The pose IS
subscribed to -- but only to report the error at the end, never to correct
it. Week 5 is the week that closes this loop.

    ros2 run ee414_w04_demo drive --shape straight --distance 2.0
    ros2 run ee414_w04_demo drive --shape square --robot tb3
"""

import argparse
import math
import sys
import time

import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from turtlesim.msg import Pose as TurtlePose

from ee414_w04_demo import graceful
from ee414_w04_demo.twist_compat import CmdVelPublisher


def yaw_from_quaternion(q):
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


class Driver(Node):

    def __init__(self, robot, rate_hz=20.0):
        super().__init__("drive")
        self.rate_hz = rate_hz

        if robot == "tb3":
            self.pub = CmdVelPublisher(self, "/cmd_vel")
            self.create_subscription(Odometry, "/odom", self.on_odom, 10)
        else:
            self.pub = CmdVelPublisher(self, "/turtle1/cmd_vel")
            self.create_subscription(TurtlePose, "/turtle1/pose", self.on_turtle, 10)

        self.pose = None   # (x, y, theta), or None until the first message

    def on_turtle(self, msg):
        self.pose = (msg.x, msg.y, msg.theta)

    def on_odom(self, msg):
        p = msg.pose.pose.position
        self.pose = (p.x, p.y, yaw_from_quaternion(msg.pose.pose.orientation))

    # ---- the primitives -------------------------------------------------

    def send_for(self, v, omega, seconds):
        """Hold one Twist for a fixed time. This is the whole of open loop.

        The clock here must be the wall clock. Pacing the loop with
        spin_once(timeout_sec=period) looks equivalent and is not: spin_once
        returns the moment a callback is ready, and the pose is arriving at
        62 Hz, so the loop finishes early and the robot travels short.
        """
        period = 1.0 / self.rate_hz
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline and not graceful.interrupted():
            self.pub.publish(v, omega)
            rclpy.spin_once(self, timeout_sec=0.0)   # drain callbacks, never block
            time.sleep(period)
        self.stop()

    def stop(self):
        # A few repeats: one dropped stop message leaves the robot driving.
        if not rclpy.ok():
            return
        for _ in range(5):
            self.pub.stop()
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(0.02)

    def move_straight(self, distance, speed):
        seconds = abs(distance / speed)
        print(f"  straight: {distance} m at {speed} m/s -> hold for {seconds:.3f} s")
        self.send_for(math.copysign(speed, distance), 0.0, seconds)

    def rotate(self, angle_rad, rate):
        seconds = abs(angle_rad / rate)
        print(f"  rotate:   {math.degrees(angle_rad):.1f} deg at "
              f"{rate} rad/s -> hold for {seconds:.3f} s")
        self.send_for(0.0, math.copysign(rate, angle_rad), seconds)

    def wait_for_pose(self, timeout=5.0):
        waited = 0.0
        while self.pose is None and waited < timeout and not graceful.interrupted():
            rclpy.spin_once(self, timeout_sec=0.1)
            waited += 0.1
        return self.pose is not None


def run_shape(node, args):
    start = node.pose
    print(f"\n  start pose  x={start[0]:.3f}  y={start[1]:.3f}  "
          f"theta={math.degrees(start[2]):+.1f} deg\n")

    if args.shape == "straight":
        node.move_straight(args.distance, args.speed)

    elif args.shape == "rotate":
        node.rotate(math.radians(args.angle), args.turn_rate)

    elif args.shape == "arc":
        # Forward and turning at once: v and omega both non-zero.
        seconds = abs(math.radians(args.angle) / args.turn_rate)
        R = args.speed / args.turn_rate
        print(f"  arc:      radius R = v/w = {R:.3f} m, "
              f"{args.angle} deg -> hold for {seconds:.3f} s")
        node.send_for(args.speed, args.turn_rate, seconds)

    elif args.shape == "square":
        print(f"  square:   4 sides of {args.distance} m, 4 turns of 90 deg")
        for i in range(4):
            if graceful.interrupted():
                break
            print(f"  -- side {i + 1}")
            node.move_straight(args.distance, args.speed)
            node.rotate(math.pi / 2.0, args.turn_rate)

    elif args.shape == "spiral":
        # Constant omega, rising v: the radius R = v/omega grows every step.
        print(f"  spiral:   omega fixed at {args.turn_rate} rad/s, v rising")
        v = 0.0
        for _ in range(40):
            if graceful.interrupted():
                break
            v += args.speed / 40.0
            node.send_for(v, args.turn_rate, 0.25)

    end = node.pose
    print(f"\n  end pose    x={end[0]:.3f}  y={end[1]:.3f}  "
          f"theta={math.degrees(end[2]):+.1f} deg")

    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dtheta = math.atan2(math.sin(end[2] - start[2]), math.cos(end[2] - start[2]))
    print(f"  moved       dx={dx:+.3f}  dy={dy:+.3f}  "
          f"dtheta={math.degrees(dtheta):+.1f} deg")

    if graceful.interrupted():
        print("\n  Ctrl-C: stop sent, nothing left running.\n")
        return

    if args.shape == "square":
        # The closing error is the deliverable: a square commanded open loop
        # does not come back to where it started, and this is by how much.
        gap = math.hypot(dx, dy)
        print(f"\n  CLOSING ERROR: {gap:.4f} m from where it started, "
              f"{abs(math.degrees(dtheta)):.1f} deg off heading")
        print("  Nothing was measured to correct this. That is what open loop means.")
    print()


def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--shape", default="straight",
                        choices=["straight", "rotate", "arc", "square", "spiral"])
    parser.add_argument("--robot", default="turtle", choices=["turtle", "tb3"])
    parser.add_argument("--distance", type=float, default=2.0, help="metres")
    parser.add_argument("--angle", type=float, default=90.0, help="degrees")
    parser.add_argument("--speed", type=float, default=1.0, help="m/s")
    parser.add_argument("--turn-rate", type=float, default=1.0, help="rad/s")
    parsed = parser.parse_args(args=args)

    graceful.init()
    node = Driver(parsed.robot)
    try:
        if not node.wait_for_pose():
            src = "/odom" if parsed.robot == "tb3" else "/turtle1/pose"
            node.get_logger().error(f"No pose on {src}. Is the simulator running?")
            return 1
        run_shape(node, parsed)
    finally:
        node.stop()
        graceful.shutdown(node)
    return 0


if __name__ == "__main__":
    sys.exit(main())
