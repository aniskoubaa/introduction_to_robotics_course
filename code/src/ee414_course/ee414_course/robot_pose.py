# This file is part of the ee414_course package.
#
# EE 414 — Introduction to Robotics. Week 4: differential-drive kinematics.
#
# Based on RobotPose.py from ros2_course_packages (Copyright (c) 2023 Anis Koubaa),
# licensed CC BY-NC-SA 4.0. Extended for EE 414 with the angle handling that
# Week 4 slide 13 is about.
"""The pose of a robot on a floor: three numbers, and the arithmetic that goes with them.

    x, y      where it is, in metres
    theta     which way it faces, in radians

The original class held the three numbers and nothing else, so every script
that used it wrote its own distance and angle arithmetic — and each one wrote
the angle arithmetic wrongly, in the same way. That arithmetic lives here now,
once, correct.
"""

import math


def normalize_angle(angle):
    """Fold any angle into (-pi, pi].

    THIS IS THE FUNCTION WEEK 4 SLIDE 13 IS ABOUT.

    Headings live on a circle, so 350 degrees and -10 degrees are the same
    direction. Plain subtraction does not know that: a robot at +176 deg and a
    target at -176 deg are 8 degrees apart, but `target - current` gives -352.
    A controller fed -352 turns the long way round, every time, for ever.

    The atan2(sin, cos) trick works because sin and cos are already periodic:
    it throws away the winding and keeps the direction.
    """
    return math.atan2(math.sin(angle), math.cos(angle))


class RobotPose:
    """Where the robot is and which way it faces."""

    def __init__(self, x=0.0, y=0.0, theta=0.0):
        self.x = x
        self.y = y
        self.theta = theta

    # -- the accessors the original had, kept so old scripts still work -----

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def get_theta(self):
        return self.theta

    def set_theta(self, theta):
        self.theta = theta

    def get_pose(self):
        return self

    # -- the arithmetic every motion script needs ---------------------------

    def distance_to(self, other):
        """Straight-line distance to another pose, in metres."""
        return math.hypot(other.x - self.x, other.y - self.y)

    def angle_to(self, other):
        """The heading that points from here to `other`, in radians."""
        return math.atan2(other.y - self.y, other.x - self.x)

    def heading_error_to(self, target_theta):
        """How far to turn to face `target_theta`, wrapped and signed.

        Positive means turn left. The result is always in (-pi, pi], so it is
        always the short way round.
        """
        return normalize_angle(target_theta - self.theta)

    def angle_turned_since(self, start_theta):
        """How far the robot has turned away from `start_theta`, in radians.

        Use this instead of `abs(start.theta - now.theta)`. That expression is
        the bug in the original clean.py: cross the +/-pi seam and it jumps
        from nearly 0 to nearly 2*pi, so a rotate() built on it either stops
        immediately or never stops at all.
        """
        return abs(normalize_angle(self.theta - start_theta))

    def copy(self):
        return RobotPose(self.x, self.y, self.theta)

    def __str__(self):
        return "RobotPose(x={:.3f}, y={:.3f}, theta={:.3f} rad = {:.1f} deg)".format(
            self.x, self.y, self.theta, math.degrees(self.theta))


def yaw_from_quaternion(q):
    """Pull the heading out of a quaternion (the /odom case).

    turtlesim hands you theta directly. A real robot hands you four numbers on
    nav_msgs/msg/Odometry and you do this yourself. It is the only quaternion
    formula EE 414 asks you to write.
    """
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


def quaternion_from_yaw(theta):
    """Turn a heading into a quaternion: (x, y, z, w)."""
    return (0.0, 0.0, math.sin(theta / 2.0), math.cos(theta / 2.0))
