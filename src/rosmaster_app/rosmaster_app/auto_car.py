import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import numpy as np
import os
import onnxruntime as ort

class AutoParkingNode(Node):
    def __init__(self):
        super().__init__('auto_parking_node')
        
        # ROS 2 话题初始化
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.lidar_sub = self.create_subscription(LaserScan, 'scan', self.lidar_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, 'odom', self.odom_callback, 10)

        # 模型加载
        self.model = ort.InferenceSession('./path/to/your/model.onnx')
        
        # 数据存储
        self.current_scan = None  # 激光雷达数据
        self.current_pose = None  # 小车的位置信息
        self.is_parking_done = False  # 停车状态

        # 日志
        self.get_logger().info('AutoParkingNode 已初始化')

    def lidar_callback(self, scan_data):
        """订阅雷达数据"""
        self.current_scan = scan_data
        # self.get_logger().debug('已更新雷达数据')

    def odom_callback(self, odom_data):
        """订阅里程计数据"""
        self.current_pose = odom_data
        # self.get_logger().debug('已更新里程计数据')

    def make_decision(self):
        """基于当前传感器数据进行决策"""
        if self.current_scan is None or self.current_pose is None:
            self.get_logger().warning('尚未收到完整的传感器数据')
            return None
        
        # 如果还有需要别的数据请参考我之前发出的文档
        scan_sec = self.current_scan.header.stamp.sec
        scan_nanosec = self.current_scan.header.stamp.nanoces
        scan_ranges = self.current_scan.ranges
        linear_velocity = self.current_pose.twist.twist.linear
        angular_velocity = self.current_pose.twist.twist.angular
        odom_sec = self.current_pose.header.stamp.sec
        odom_nanosec = self.current_pose.header.stamp.nanosec
        position = self.current_pose.pose.pose.position
        orientation = self.current_pose.pose.pose.orientation
        # 传给小车前最好把odom和scan的时间对齐检查一下先
        self.get_logger().info(f'scan time sec: {scan_sec},nanotime: {scan_nanosec}')
        self.get_logger().info(f'scan range: {scan_ranges}')
        self.get_logger().info(f'odom time sec: {odom_sec},nanotime: {odom_nanosec}')
        self.get_logger().info(f"position x: {position.x},y: {position.y},z: {position.z},rotation:{orientation.z}")
        self.get_logger().info(f"velocity x: {linear_velocity.x},y: {linear_velocity.y},z: {linear_velocity.z},rotation:{angular_velocity.z}")

        # 传感器数据编译为模型输入
        # 根据训练数据的规范调整输入格式
        # observation = np.hstack([self.current_scan, 
        #                          [self.current_pose.position.x, 
        #                           self.current_pose.position.y, 
        #                           self.current_pose.orientation.z]])
        observation = observation.reshape(1, -1).astype(np.float32)
        # ONNX 推理
        action = self.model.run(['action'], {'observation': observation})[0].flatten()
        return action

    def publish_control(self, action):
        """发布控制命令"""
        cmd = Twist()
        # 发出的消息必须是速度的形式，这里的action如果不是速度还得改
        cmd.linear.x = action[0]  # 模型输出的线速度
        cmd.angular.z = action[1]  # 模型输出的角速度
        self.cmd_vel_pub.publish(cmd)
        self.get_logger().info(f'已发布控制命令: 线速度={cmd.linear.x}, 角速度={cmd.angular.z}')

    def control_loop(self):
        """控制循环"""
        rate = self.create_rate(10)  # 10 Hz
        while rclpy.ok():
            rclpy.spin_once(self)  # 更新传感器数据
            if self.is_parking_done:
                self.stop_car()
                break

            # 决策与控制
            action = self.make_decision()
            if action is not None:
                self.publish_control(action)
            rate.sleep()

    def stop_car(self):
        """停车操作"""
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd)
        self.get_logger().info('停车完成')

def main(args=None):
    rclpy.init(args=args)
    node = AutoParkingNode()
    try:
        node.control_loop()
    except KeyboardInterrupt:
        node.get_logger().info('手动终止程序')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
