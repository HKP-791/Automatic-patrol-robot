import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import numpy as np

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.bridge = CvBridge()
        self.latest_image = None
        self.queue_ = []
        self.subscription = self.create_subscription(
            Image,
            '/camera_sensor/image_raw',
            self.image_callback,
            10)
        self.publisher_ = self.create_publisher(
            Image,
            '/camera_sensor/processed_image',
            10)

    def image_callback(self, msg):
        self.latest_image = msg
        if self.latest_image is not None:
            cv_image = self.bridge.imgmsg_to_cv2(self.latest_image)
        self.cv_image = cv_image

    def image_pub(self):
        while self.queue_:
            msg = Image()
            msg.data = self.queue_.pop(0)
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing image')

def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    rclpy.shutdown()

if __name__ == '__main__':
    main()