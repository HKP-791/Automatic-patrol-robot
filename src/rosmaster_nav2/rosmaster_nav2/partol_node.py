import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from rclpy import time
from tf2_ros import TransformListener, Buffer
import tf_transformations
from partol_interfaces.srv import SpeechText


class partolNode(BasicNavigator):
    def __init__(self):
        super().__init__('partol_node')
        self.declare_parameter('initial_point', [0.0, 0.0, 0.0])
        self.declare_parameter('target_points', [0.0, 0.0, 0.0, 1.0, 1.0, 1.57])
        self.initial_point = self.get_parameter('initial_point').value
        self.initial_point = self.get_parameter('target_points').value
        self.buffer_ = Buffer()
        self.listener_ = TransformListener(self.buffer_, self)
        self.speech_client_ = self.create_client(SpeechText, 'speech_text')

    def get_pose(self, x, y, yaw):
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.pose.position.x = x
        pose.pose.position.y = y
        rotation_quat = tf_transformations.quaternion_from_euler(0, 0, yaw)
        pose.pose.orientation.x = rotation_quat[0]
        pose.pose.orientation.y = rotation_quat[1]
        pose.pose.orientation.z = rotation_quat[2]
        pose.pose.orientation.w = rotation_quat[3]
        return pose

    def init_robot(self):
        self.initial_point_ = self.get_parameter('initial_point').value
        self.setInitialPose(self.get_pose(
            self.initial_point_[0], self.initial_point_[1], self.initial_point_[2]))
        self.waitUntilNav2Active()

    def get_target_point(self):
        points = []
        self.target_points_ = self.get_parameter('target_points').value
        for index in range(int(len(self.target_points_)/3)):
            x = self.target_points_[index*3]
            y = self.target_points_[index*3+1]
            yaw = self.target_points_[index*3+2]
            points.append([x, y, yaw])
            self.get_logger().info(f'target point: {points[index]}')
        return points

    def nav_to_pose(self, target_pose):
        self.waitUntilNav2Active
        result = self.goToPose(target_pose)
        while not self.isTaskComplete():
            feedback = self.getFeedback()
            if feedback:
                self.get_logger().info(f'estimated time left: {feedback.estimated_time_remaining}')
        result = self.getResult()
        if result == TaskResult.SUCCEEDED:
            self.get_logger().info('Goal succeeded!')
        elif result == TaskResult.CANCELED:
            self.get_logger().info('Goal was canceled!')
        elif result == TaskResult.FAILED:
            self.get_logger().info('Goal failed!')
        else:
            self.get_logger().info('Goal has an invalid returnstatus!')

    def get_current_pose(self):
        while rclpy.ok():
            try:
                tf = self.buffer_.lookup_transform('map', 'base_footprint', time.Time(seconds=0),
                                                   time.Duration(seconds=1))
                transform = tf.transform
                return transform
            except Exception as e:
                self.get_logger().info('get current pose failed: {}'.format(e))

    def speech_text(self, text):
        while not self.speech_client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting...')
        request = SpeechText.Request()
        request.text = text
        future = self.speech_client_.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            result = future.result().result
            if result:
                self.get_logger().info(f'speech succeed: {text}')
            else:
                self.get_logger().warn(f'speech failed: {text}')
        else:
            self.get_logger().warn('request failed')

def main():
    rclpy.init()
    partol = partolNode()
    partol.speech_text(text='initalizing')
    partol.init_robot()
    partol.speech_text(text='ready')
    while rclpy.ok():
        points = partol.get_target_point()
        while rclpy.ok():
            for point in points:
                x, y, yaw = point[0], point[1], point[2]
                target_pose = partol.get_pose(x, y, yaw)
                partol.speech_text(text=f'I am going to position {int(x)}, {int(y)}')
                partol.nav_to_pose(target_pose)
        rclpy.shutdown()