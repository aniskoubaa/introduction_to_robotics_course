#!/usr/bin/env python3
"""Integrating the model: turning v and omega back into x, y, theta.

Slide reference: "Integrating the Model" (Euler against the exact arc) and
the wheel-odometry error sources.

Two modes.

  --compare   No ROS, no simulator. Drive a known quarter-circle on paper at
              several timestep sizes and measure each method against the
              answer trigonometry gives. This is the Euler-versus-arc slide,
              as a table of numbers.

  (default)   Live. Subscribe to /cmd_vel, integrate it both ways, and hold
              the result against what the simulator says really happened.
              Run this in one terminal and drive.py in another.
"""

import argparse
import math

SEP = "-" * 72


# --------------------------------------------------------------------------
# The two integrators. Both take a pose and one timestep of (v, omega).
# --------------------------------------------------------------------------

def step_euler(x, y, theta, v, omega, dt):
    """Pretend the heading is frozen for the whole timestep, then turn."""
    x += v * math.cos(theta) * dt
    y += v * math.sin(theta) * dt
    theta += omega * dt
    return x, y, theta


def step_exact_arc(x, y, theta, v, omega, dt):
    """Follow the arc the robot is actually on. Exact when v and omega are held."""
    if abs(omega) < 1e-9:
        return step_euler(x, y, theta, v, omega, dt)
    R = v / omega                       # radius of the arc
    theta_new = theta + omega * dt
    x += R * (math.sin(theta_new) - math.sin(theta))
    y -= R * (math.cos(theta_new) - math.cos(theta))
    return x, y, theta_new


# --------------------------------------------------------------------------
# Offline comparison
# --------------------------------------------------------------------------

def compare():
    # A quarter circle of radius 1 m, driven at 0.5 m/s. Where does it end?
    # Trigonometry says: starting at the origin facing +x, turning left,
    # the robot finishes at (R, R) -- that is (1, 1) -- facing +y.
    v, omega = 0.5, 0.5          # R = v/omega = 1.0 m
    total_time = (math.pi / 2.0) / omega
    truth = (1.0, 1.0, math.pi / 2.0)

    print()
    print(SEP)
    print("A quarter circle of radius 1.0 m, driven at v = 0.5 m/s, w = 0.5 rad/s")
    print(SEP)
    print(f"The exact finish, from trigonometry:  "
          f"x = {truth[0]:.6f}   y = {truth[1]:.6f}\n")
    print("   timestep      Euler finish            error        arc finish              error")

    for dt in [1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]:
        ex, ey, et = 0.0, 0.0, 0.0
        ax, ay, at = 0.0, 0.0, 0.0

        # Walk the full duration. The last step is whatever time is left over,
        # so every row below covers the same quarter turn -- otherwise we would
        # be measuring a shorter manoeuvre, not a worse integrator.
        remaining = total_time
        while remaining > 1e-12:
            h = min(dt, remaining)
            ex, ey, et = step_euler(ex, ey, et, v, omega, h)
            ax, ay, at = step_exact_arc(ax, ay, at, v, omega, h)
            remaining -= h

        e_err = math.hypot(ex - truth[0], ey - truth[1])
        a_err = math.hypot(ax - truth[0], ay - truth[1])
        print(f"   {dt:5.2f} s     ({ex:7.4f}, {ey:7.4f})     {e_err:.3e}"
              f"    ({ax:7.4f}, {ay:7.4f})     {a_err:.3e}")

    print()
    print("   Read the two error columns. Halving the timestep halves the Euler")
    print("   error -- it is first order, and it never reaches zero. The arc")
    print("   integrator is right to machine precision at every timestep,")
    print("   because holding v and omega constant IS an arc, and it follows one.")
    print()
    print("   This is why the error column matters: at 0.05 s, the rate a real")
    print("   robot actually runs its odometry, Euler is already off by")
    print("   centimetres on ONE quarter turn. Those centimetres accumulate")
    print("   for as long as the robot is switched on, and nothing removes them.")
    print()


# --------------------------------------------------------------------------
# Live mode
# --------------------------------------------------------------------------

def live(robot):
    import rclpy
    from nav_msgs.msg import Odometry
    from rclpy.node import Node
    from turtlesim.msg import Pose as TurtlePose

    from ee414_course import graceful
    from ee414_course.twist_compat import resolve_twist_type, twist_of

    def yaw_from_quaternion(q):
        return math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                          1.0 - 2.0 * (q.y * q.y + q.z * q.z))

    class DeadReckoner(Node):

        def __init__(self):
            super().__init__("dead_reckoning")
            self.euler = None       # our own estimate, Euler
            self.arc = None         # our own estimate, exact arc
            self.truth = None       # what the simulator says
            self.last_cmd = (0.0, 0.0)
            self.last_t = None
            self.reports = 0

            topic = "/cmd_vel" if robot == "tb3" else "/turtle1/cmd_vel"
            # Same trap as drive.py: on Jazzy the TurtleBot 3 bridge uses
            # TwistStamped, and subscribing with the wrong type is silent.
            msg_type = resolve_twist_type(self, topic)
            self.create_subscription(msg_type, topic, self.on_cmd, 10)
            if robot == "tb3":
                self.create_subscription(Odometry, "/odom", self.on_odom, 10)
            else:
                self.create_subscription(TurtlePose, "/turtle1/pose", self.on_turtle, 10)

            # 20 Hz: integrate the command currently in force, exactly the way
            # a real wheel-odometry loop does.
            self.create_timer(0.05, self.on_tick)
            self.get_logger().info(f"Integrating {topic}. Drive the robot now.")

        def on_cmd(self, msg):
            t = twist_of(msg)
            self.last_cmd = (t.linear.x, t.angular.z)

        def on_turtle(self, msg):
            self.truth = (msg.x, msg.y, msg.theta)
            if self.euler is None:
                self.euler = self.arc = self.truth   # start from the truth, once

        def on_odom(self, msg):
            p = msg.pose.pose.position
            self.truth = (p.x, p.y, yaw_from_quaternion(msg.pose.pose.orientation))
            if self.euler is None:
                self.euler = self.arc = self.truth

        def on_tick(self):
            if self.euler is None:
                return
            v, omega = self.last_cmd
            dt = 0.05
            self.euler = step_euler(*self.euler, v, omega, dt)
            self.arc = step_exact_arc(*self.arc, v, omega, dt)

            if abs(v) < 1e-9 and abs(omega) < 1e-9:
                return   # standing still: nothing to report

            self.reports += 1
            if self.reports % 20:
                return
            self.report()

        def report(self):
            tx, ty, _ = self.truth
            ex, ey, _ = self.euler
            ax, ay, _ = self.arc
            print(f"  truth ({tx:6.3f},{ty:6.3f})   "
                  f"euler ({ex:6.3f},{ey:6.3f}) off {math.hypot(ex-tx, ey-ty):.4f}   "
                  f"arc ({ax:6.3f},{ay:6.3f}) off {math.hypot(ax-tx, ay-ty):.4f}")

    graceful.init()
    node = DeadReckoner()
    try:
        # Ctrl-C only sets a flag, so the summary below still runs.
        while rclpy.ok() and not graceful.interrupted():
            rclpy.spin_once(node, timeout_sec=0.1)
    finally:
        if node.truth and node.euler:
            print()
            node.report()
            print("\n  Neither estimate ever looked at the robot. They were computed")
            print("  from the commands alone -- which is exactly what odometry does,")
            print("  and exactly why it drifts.\n")
        graceful.shutdown(node)


def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--compare", action="store_true",
                        help="offline Euler-vs-arc table, no simulator needed")
    parser.add_argument("--robot", default="turtle", choices=["turtle", "tb3"])
    parsed = parser.parse_args(args=args)

    if parsed.compare:
        compare()
    else:
        live(parsed.robot)


if __name__ == "__main__":
    main()
