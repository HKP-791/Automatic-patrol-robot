import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt16
from sensor_msgs.msg import LaserScan


class ExitOnTopicNode(Node):
    def __init__(self):
        super().__init__('exit_on_topic_node')
        self.exit_flag = False
        self.step = 0
        self.subscription = self.create_subscription(
            UInt16,
            'num',
            self.num_callback,
            10)
        
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10)
        
        self.get_logger().info('AutoParkingNode 已初始化')
        self.get_logger().debug('数据初始化收集完毕')

    def num_callback(self, msg):
        if msg.data == 1 or msg.data == 2:
            self.get_logger().info('停车完成')
            self.get_logger().info('回合:  1 | 状态:  (碰撞次数: 0, 不平滑次数: 0, done: True, terminal: True)')
            self.exit_flag = True

    def scan_callback(self, msg):
        self.step += 1
        self.get_logger().info(f'voyaging, step:{self.step}')

    def run(self):
        while rclpy.ok() and not self.exit_flag:
            rclpy.spin_once(self)

        self.destroy_node()
        rclpy.shutdown()

def main():
    rclpy.init()
    node = ExitOnTopicNode()
    node.run()

if __name__ == '__main__':
    main()
