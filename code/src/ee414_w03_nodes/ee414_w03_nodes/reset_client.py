"""Calling a service from inside a callback — the two ways it fails, and the fix.

    ros2 run ee414_w03_nodes reset_client --ros-args -p mode:=spin  # loud failure
    ros2 run ee414_w03_nodes reset_client --ros-args -p mode:=hang  # silent hang
    ros2 run ee414_w03_nodes reset_client --ros-args -p mode:=fix   # works

All three call the same service from the same subscriber callback. The only
difference is whether the callback waits for the reply itself.

  spin  rclpy.spin_until_future_complete() inside a callback.  Jazzy notices and
        raises `Executor is already spinning` — an error you can search for.
  hang  client.call() inside a callback.  Nothing is raised. The node freezes,
        keeps running, and prints nothing more. This is the dangerous one.
  fix   call_async() + add_done_callback().  The callback returns immediately.
"""
import rclpy
from rclpy.node import Node

from ee414_w03_interfaces.msg import WheelState
from ee414_w03_interfaces.srv import ResetOdom


class ResetClient(Node):

    def __init__(self):
        super().__init__('reset_client')
        self.declare_parameter('mode', 'fix')
        self.mode = self.get_parameter('mode').value

        self.cli = self.create_client(ResetOdom, 'reset_odom')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('waiting for /reset_odom ...')

        self.create_subscription(WheelState, 'wheel_state', self.on_msg, 10)
        self.get_logger().info(f"mode={self.mode} - subscribed to /wheel_state")

    def on_msg(self, msg):
        request = ResetOdom.Request(zero_heading=True)

        if self.mode == 'spin':
            future = self.cli.call_async(request)
            rclpy.spin_until_future_complete(self, future)   # <- raises
            self.get_logger().info('never printed')

        elif self.mode == 'hang':
            self.get_logger().info('callback: calling the service, waiting for the reply ...')
            response = self.cli.call(request)               # <- never returns
            self.get_logger().info(f'never printed: {response.message}')

        else:
            future = self.cli.call_async(request)
            future.add_done_callback(self.on_reply)
            return

    def on_reply(self, future):
        self.get_logger().info(f'reply: {future.result().message}')


def main():
    rclpy.init()
    rclpy.spin(ResetClient())
    rclpy.shutdown()
