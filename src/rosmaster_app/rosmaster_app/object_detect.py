import os
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from launch_ros.substitutions import FindPackageShare

from ultralytics import YOLO

class Yolov11Node(Node):
    def __init__(self):
        super().__init__('yolov11_node')
        rosmaster_app_path = FindPackageShare('rosmaster_app').find('rosmaster_app')
        yolo_model_path = os.path.join(rosmaster_app_path, 'yolo_model', 'best.pt')
        self.bridge = CvBridge()
        self.image_sub = self.create_subscription(
            Image, '/camera_sensor/image_raw', self.image_callback, 10)
        self.result_img_pub = self.create_publisher(Image, 'detected_image', 10)
        self.yolov11 = YOLO(yolo_model_path, task='detect')

    def image_callback(self, msg):
        label_dic = {0:'beer', 1:'table', 2:'bookshelf'}
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        detect_result = self.yolov11.predict(source=cv_image, imgsz=512, save=False)
        boxes = detect_result[0].boxes.xyxy
        cls = detect_result[0].boxes.cls
        for i in range(len(boxes)):
            cv2.rectangle(cv_image, (int(boxes[i][0]), int(boxes[i][1])),(int(boxes[i][2]), int(boxes[i][3])), color=(255, 255, 0), thickness=2)
            cv2.putText(cv_image, label_dic[int(cls[i].item())], (int(boxes[i][0]), int(boxes[i][1])), color=(255, 255, 0), fontScale=0.8, fontFace=cv2.FONT_HERSHEY_SIMPLEX, thickness=2)
        result_msg = self.bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')
        self.result_img_pub.publish(result_msg)

def main():
    rclpy.init()
    node = Yolov11Node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()