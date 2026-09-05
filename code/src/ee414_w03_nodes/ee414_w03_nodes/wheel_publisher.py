"""Publish the Week 3 custom message, so `ros2 topic echo` shows your own fields."""
import rclpy
from rclpy.node import Node

from ee414_w03_interfaces.msg import WheelState


class WheelPublisher(Node):

    def __init__(self):
        super().__init__('wheel_publisher')
        self.pub = self.create_publisher(WheelState, 'wheel_state', 10)
        self.create_timer(0.5, self.tick)

    def tick(self):
        msg = WheelState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.left_rad_s = 2.4
        msg.right_rad_s = 2.4
        msg.estopped = False
        self.pub.publish(msg)


def main():
    rclpy.init()
    rclpy.spin(WheelPublisher())
    rclpy.shutdown()
