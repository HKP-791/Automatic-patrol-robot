from sensor_msgs.msg import LaserScan
from tf2_msgs.msg import TFMessage
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
import rclpy
from rclpy.node import Node

class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        # 初始化判断，只有接收到消息后才启动小车控制

        self.laser_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.laser_callback,
            10)
    
        self.subscription = self.create_subscription(
            TFMessage,
            '/tf',
            self.tf_callback,
            10)
        
        self.state_sub = self.create_subscription(
            JointState,
            'joint_states',
            self.state_callback,
            10)
        
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10)

    def laser_callback(self,laser_data):
        # self.get_logger().info('I heard: "%s"' % laser_data)
        return laser_data # 话题更新速度10hz
    
    def tf_callback(self,tf_data):
        for transform in tf_data.transforms:
            if transform.child_frame_id == "base_footprint":
                position = transform.transform.translation
                rotation = transform.transform.rotation
                # self.get_logger().info(f"X: {position.x}, Y: {position.y}, Z: {position.z}, rotation:{rotation.z}")
    
    def state_callback(self, state_data):
        # self.get_logger().info('I heard: "%s"' % state_data)
        self.state_data = state_data # 话题更新速度15hz
        if state_data:
            self.joint_name = state_data.name
            self.joint_pos = state_data.position
            self.joint_vel = state_data.velocity
            self.joint_eff = state_data.effort
            # self.get_logger().info('I heard: "%s"' % self.state_data)

    def odom_callback(self,odom_data):
        linear_velocity = odom_data.twist.twist.linear
        angular_velocity = odom_data.twist.twist.angular
        sec = odom_data.header.stamp.sec
        nanosec = odom_data.header.stamp.nanosec
        position = odom_data.pose.pose.position
        orientation = odom_data.pose.pose.orientation
        self.get_logger().info(f'time sec: {sec},nanotime: {nanosec}')
        self.get_logger().info(f"position x: {position.x},y: {position.y},z: {position.z},rotation:{orientation.z}")
        self.get_logger().info(f"velocity x: {linear_velocity.x},y: {linear_velocity.y},z: {linear_velocity.z},rotation:{angular_velocity.z}")



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
        