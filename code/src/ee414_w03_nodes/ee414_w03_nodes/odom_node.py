"""The service server half. Prove it from the terminal before writing a client."""
import rclpy
from rclpy.node import Node

from ee414_w03_interfaces.srv import ResetOdom


class OdomNode(Node):

    def __init__(self):
        super().__init__('odom_node')
        self.x = 12.5
        self.create_service(ResetOdom, 'reset_odom', self.on_reset)

    def on_reset(self, request, response):
        self.x = 0.0
        response.success = True
        response.message = 'odometry zeroed'
        return response


def main():
    rclpy.init()
    rclpy.spin(OdomNode())
    rclpy.shutdown()
