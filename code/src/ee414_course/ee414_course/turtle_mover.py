#!/usr/bin/env python3
# This file is part of the ee414_course package.
#
# EE 414 — Introduction to Robotics. Week 4, slides 29-31 and 38.
#
# Improved from simple_turtlesim_motion.py in ros2_course_packages
# (Copyright (c) 2023 Anis Koubaa), licensed CC BY-NC-SA 4.0.
"""The simplest moving node: one speed, held on a timer, until far enough.

This is open-loop motion. The node decides how far it has gone by multiplying
speed by elapsed time -- it never looks at where the robot actually is. That
is exactly what Week 4 means by open loop, and the point of this script is to
show you how wrong that estimate gets.

    ros2 run ee414_course turtle_mover
    ros2 run ee414_course turtle_mover --distance 8.0 --speed 1.0 --turn 0.0

What changed from the original simple_turtlesim_motion:

  * It stops by cancelling the timer, not by calling rclpy.shutdown() inside
    a callback and then publishing again afterwards.
  * It subscribes to the pose, so it can print the open-loop ESTIMATE next to
    the TRUTH at the end. The gap between them is the lesson.
  * The reset service is waited for instead of assumed to be there.
"""

import argparse
import time

import rclpy

from ee414_course import graceful
from rclpy.node import Node
from std_srvs.srv import Empty

from ee414_course.robot_io import RobotDriver


class TurtleMover(Node):

    def __init__(self, distance, speed, turn):
        super().__init__("turtle_mover")

        self.distance = distance
        self.speed = speed
        self.turn = turn

        self.driver = RobotDriver(self, "turtle")

        # The open-loop estimate: the only thing the node uses to decide.
        self.estimated_distance = 0.0
        self.start_pose = None
        self.last_tick = None

        self.reset_turtlesim()

        if not self.driver.wait_for_pose():
            raise RuntimeError("no pose from turtlesim")
        self.start_pose = self.driver.pose.copy()

        print(f"\n  Driving {distance} m at {speed} m/s "
              f"(turning at {turn} rad/s).")
        print(f"  Expected duration: {distance / speed:.2f} s\n")

        self.finished = False
        self.timer = self.create_timer(0.05, self.tick)

    def reset_turtlesim(self):
        """Put the turtle back in the middle and clear the trail."""
        client = self.create_client(Empty, "/reset")
        if not client.wait_for_service(timeout_sec=3.0):
            self.get_logger().warn("no /reset service; carrying on anyway")
            return
        future = client.call_async(Empty.Request())
        rclpy.spin_until_future_complete(self, future, timeout_sec=3.0)

        # Throw away whatever pose arrived before the reset and spin until a
        # fresh one turns up. Without this, start_pose is the pose the turtle
        # had BEFORE it was teleported back to the middle, and the closing
        # error reported at the end is measured from the wrong point --
        # it was reporting 90% error on a drive that was accurate to 1%.
        self.driver.pose = None
        deadline = time.monotonic() + 2.0
        while self.driver.pose is None and time.monotonic() < deadline:
            rclpy.spin_once(self, timeout_sec=0.05)
        print("  Turtlesim reset.")

    def tick(self):
        now = time.monotonic()
        if self.last_tick is None:
            self.last_tick = now
            return
        dt = now - self.last_tick
        self.last_tick = now

        # THE OPEN-LOOP STEP: distance is speed times time, and nothing else.
        # No pose is consulted to make this decision.
        self.estimated_distance += self.speed * dt

        if self.estimated_distance >= self.distance:
            self.finish()
            return

        self.driver.publish(self.speed, self.turn)

    def finish(self):
        self.timer.cancel()
        self.driver.stop()

        # Only NOW do we look at the pose -- to measure the error, never to
        # have corrected it. Week 5 is the week that closes this loop.
        # No spin_once here: we are inside a timer callback, so the executor
        # is already spinning and has been updating this pose all along.
        end = self.driver.pose

        print("  The robot has stopped.\n")
        print(f"  open-loop estimate : {self.estimated_distance:.4f} m travelled")

        if self.turn == 0.0:
            actually = self.start_pose.distance_to(end)
            print(f"  actually travelled : {actually:.4f} m "
                  f"(straight line from start to finish)")
            error = abs(actually - self.estimated_distance)
            print(f"  error              : {error:.4f} m "
                  f"({100.0 * error / self.distance:.1f}% of the distance asked for)")
        else:
            straight = self.start_pose.distance_to(end)
            print(f"  straight-line gap  : {straight:.4f} m from start to finish")
            print("  (it was turning, so the path is an arc and the distance")
            print("   travelled along it is longer than the gap)")

        print(f"\n  start : {self.start_pose}")
        print(f"  end   : {end}")
        print("\n  Nothing in this node used the pose to decide anything.")
        print("  That is what open loop means.\n")

        # A flag, not raise SystemExit: main()'s spin loop watches it and
        # returns normally, so the shutdown path is the same one Ctrl-C takes.
        self.finished = True


def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--distance", type=float, default=5.0, help="metres")
    parser.add_argument("--speed", type=float, default=1.0, help="m/s")
    parser.add_argument("--turn", type=float, default=0.0,
                        help="rad/s; non-zero draws an arc")
    parsed, _ = parser.parse_known_args(args=args)

    graceful.init(args)
    node = None
    try:
        node = TurtleMover(parsed.distance, parsed.speed, parsed.turn)
        while rclpy.ok() and not graceful.interrupted() and not node.finished:
            rclpy.spin_once(node, timeout_sec=0.1)
    finally:
        if node is not None:
            node.driver.stop()
        graceful.shutdown(node)


if __name__ == "__main__":
    main()
