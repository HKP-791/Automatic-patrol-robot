import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import UInt16
import tkinter as tk
from tkinter import messagebox
import threading

class TeleopGUI(Node):
    def __init__(self):
        super().__init__('teleop_gui')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.num_publisher = self.create_publisher(UInt16, 'num', 10)
        self.num_  = UInt16()
        self.velocity_ = Twist()
        self.velocity_.linear.x = 0.0
        self.velocity_.angular.z = 0.0
        self.speed_scale_ = 0.5  # 速度缩放因子

        # 创建GUI窗口
        self.root = tk.Tk()
        self.root.title("ROS 2 Teleoperation GUI")

        # 创建按钮
        self.q_button = tk.Button(self.root, text="Q", command=self.on_q_press)
        self.q_button.grid(row=0, column=0)

        self.w_button = tk.Button(self.root, text="W", command=self.on_w_press)
        self.w_button.grid(row=0, column=1)

        self.e_button = tk.Button(self.root, text="E", command=self.on_e_press)
        self.e_button.grid(row=0, column=2)

        self.a_button = tk.Button(self.root, text="A", command=self.on_a_press)
        self.a_button.grid(row=1, column=0)

        self.s_button = tk.Button(self.root, text="S", command=self.on_s_press)
        self.s_button.grid(row=1, column=1)

        self.d_button = tk.Button(self.root, text="D", command=self.on_d_press)
        self.d_button.grid(row=1, column=2)

        self.up_button = tk.Button(self.root, text="up", command=self.on_up_press)
        self.up_button.grid(row=2, column=0)

        self.down_button = tk.Button(self.root, text="do", command=self.on_down_press)
        self.down_button.grid(row=2, column=1)

        self._shot = tk.Button(self.root, text="sh", command=self.screen_shot)
        self._shot.grid(row=2, column=2)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.on_stop_press)
        self.stop_button.grid(row=3, column=0, columnspan=3)

        # 创建一个线程用于ROS 2节点的spin
        self.ros2_thread = threading.Thread(target=self.ros2_spin)
        self.ros2_thread.daemon = True
        self.ros2_thread.start()

        # 运行GUI主循环
        self.root.mainloop()

    def on_q_press(self):
        self.velocity_.angular.z = -self.speed_scale_
        self.publish_velocity()

    def on_w_press(self):
        self.velocity_.linear.x = self.speed_scale_
        self.publish_velocity()

    def on_e_press(self):
        self.velocity_.angular.z = self.speed_scale_
        self.publish_velocity()

    def on_a_press(self):
        self.velocity_.linear.y = -self.speed_scale_
        self.publish_velocity()

    def on_s_press(self):
        self.velocity_.linear.x = -self.speed_scale_
        self.publish_velocity()

    def on_d_press(self):
        self.velocity_.linear.y = self.speed_scale_
        self.publish_velocity()

    def on_stop_press(self):
        self.velocity_.linear.x = 0.0
        self.velocity_.linear.y = 0.0
        self.velocity_.angular.z = 0.0
        self.publish_velocity()

    def on_up_press(self):
        self.velocity_.linear.x = self.velocity_.linear.x*1.2
        self.velocity_.linear.y = self.velocity_.linear.y*1.2
        self.velocity_.angular.z = self.velocity_.angular.z*1.2
        self.publish_velocity()

    def on_down_press(self):
        self.velocity_.linear.x = self.velocity_.linear.x*0.8
        self.velocity_.linear.y = self.velocity_.linear.y*0.8
        self.velocity_.angular.z = self.velocity_.angular.z*0.8
        self.publish_velocity()

    def screen_shot(self):
        self.num_.data = 1
        self.publish_num()

    def publish_velocity(self):
        self.publisher_.publish(self.velocity_)

    def publish_num(self):
        self.num_publisher.publish(self.num_)

    def ros2_spin(self):
        try:
            rclpy.spin(self)
        except Exception as e:
            messagebox.showerror("ROS 2 Error", str(e))
            self.root.quit()

def main(args=None):
    rclpy.init(args=args)
    try:
        node = TeleopGUI()
    except Exception as e:
        messagebox.showerror("Initialization Error", str(e))
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()