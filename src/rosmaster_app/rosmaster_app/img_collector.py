import rclpy
import os
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import UInt16
import cv2
from cv_bridge import CvBridge

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.bridge = CvBridge()
        self.count = 1
        self.latest_image = None
        self.queue_ = []
        self.subscription = self.create_subscription(
            Image,
            '/camera_sensor/image_raw',
            self.image_callback,
            10)
        self.subscription = self.create_subscription(
            UInt16,
            '/num',
            self.save_img,
            10
        )
        self.publisher_ = self.create_publisher(
            Image,
            '/camera_sensor/processed_image',
            10
        )

    def image_callback(self, msg):
        self.latest_image = msg
        if self.latest_image is not None:
            cv_image = self.bridge.imgmsg_to_cv2(self.latest_image)
        self.cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)


    def save_img(self, msg):
        cv2.imwrite(os.path.join('/home/ica/auto_parking/dataset/images', f'img{self.count:02d}.jpg'), self.cv_image)
        self.count += 1

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