import sys
import os

package_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(package_dir)
grand_parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(parent_dir)))
test_draft_dir = os.path.join(grand_parent_dir,'share', 'rosmaster_x3')
sys.path.append(test_draft_dir)

import test_draft.test0 # for test

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist


class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        # 初始化判断，只有接收到消息后才启动小车控制
        self.received_message_count = 0 
        self.has_received_all_data = False

        self.imu_sub = self.create_subscription(
            Imu,
            'imu',
            self.imu_callback,
            10)

        self.laser_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.laser_callback,
            10)
        
        self.odom_sub = self.create_subscription(
            Odometry,
            'odom',
            self.odom_callback,
            10)
        
        self.state_sub = self.create_subscription(
            JointState,
            'joint_states',
            self.state_callback,
            10)
        
        self.num = self.create_subscription(
            UInt16,
            'num',
            self.num_callback,
            10)
        
        self.act = Twist()
        
        # 创建控制消息发布者，话题为/cmd_vel
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

    def publish_velocity(self):
        # 发布控制话题，由gazebo接收实现仿真控制
        self.publisher_.publish(self.act)
    
        # 防止Python垃圾回收
        # self.imu_sub  

    def laser_callback(self, laser_data):
        # self.get_logger().info('I heard: "%s"' % laser_data)
        return laser_data # 话题更新速度10hz

    def imu_callback(self, imu_data):
        # self.get_logger().info('I heard: "%s"' % imu_data)
        return imu_data # 话题更新速度50hz
    
    def odom_callback(self, odom_data):
        # self.get_logger().info('I heard: "%s"' % odom_data)
        return odom_data # 话题更新速度15hz
    
    def state_callback(self, state_data):
        # self.get_logger().info('I heard: "%s"' % state_data)
        # self.state_data = state_data # 话题更新速度15hz
        # if state_data:
        #     self.joint_name = state_data.name
        #     self.joint_pos = state_data.position
        #     self.joint_vel = state_data.velocity
        #     self.joint_eff = state_data.effort
        #     self.received_message_count += 1
        #     self.check_and_start()
        #     self.get_logger().info('I heard: "%s"' % self.state_data)
        return None

    def num_callback(self, num):
        '''
        for test
        '''
        if num:
            self.num = num.data
            # 相加初始化判断条件需要改，num每接收一次都会加1
            self.received_message_count += 1
            self.check_and_start()
            self.get_logger().info('I heard: "%s"' % self.num)

    def check_and_start(self):
        if self.received_message_count >= 2: 
            '''
            用于初始化判断,当接收到的有效消息数量达到6,
            则表示所有用于决策的信息已收集完成，用于防止初始传入空参数或错误格式报错
            '''
            self.has_received_all_data = True
            self.timer = self.create_timer(0.1, self.process_autonomous_driving) # for test

    def process_autonomous_driving(self):
        '''
        for test only
        '''
        model = test_draft.test0.calculator1(self.num)
        ans = model.cal1()
        print(ans)


def main(args=None):
    rclpy.init(args=args)
    node = Listener()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()