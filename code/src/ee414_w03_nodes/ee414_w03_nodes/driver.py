"""Parameters: declare, then read. Nothing here is hard-coded."""
import rclpy
from rclpy.node import Node


class Driver(Node):

    def __init__(self):
        super().__init__('driver')
        self.declare_parameter('max_speed', 0.22)
        self.declare_parameter('frame_id', 'base_link')
        self.create_timer(2.0, self.tick)

    def tick(self):
        speed = self.get_parameter('max_speed').value
        frame = self.get_parameter('frame_id').value
        self.get_logger().info(f'max_speed={speed}  frame_id={frame}')


def main():
    rclpy.init()
    rclpy.spin(Driver())
    rclpy.shutdown()
