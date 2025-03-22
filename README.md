1.第一次使用要在auto_parking目录下用colcon build编译一下，每次使用前要cd到auto_parking目录下source
2.编写了两个.launch.py，分别用于启动rviz2和建立了世界的gazebo.可以通过下命令启动导入了无人机的rviz2和gazebo。
```bash
ros2 launch rosmaster_x3 display_gazebo.launch.py
ros2 launch rosmaster_x3 display_rviz2.launch.py
```
3.无人车的urdf描述文件和仿真世界的world文件位于位于
```text
/auto_parking/src/rosmaster_x3/urdf/rosmaster_x3.urdf
/auto_parking/src/rosmaster_x3/world/auto_parking.world
```
4.目前无人车已经实现了普通相机、深度相机、激光雷达、imu惯性测量单元、tf里程记和键盘控制行进。不过现在的键盘控制还是以前轮转向后轮固定的方式运行。普通相机、深度相机、激光雷达、imu惯性测量单元、tf里程记的话题分别为
```text
/camera_sensor/image_raw
/camera_sensor/depth/image_raw
/scan
/imu
/odom
```
5.可以通过rviz2、rqt和gazegbo查看实时视频和雷达点云等数据（推荐rviz2）.操控小车移动可以通过调用节点进行控制
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
6.小车的转动惯量等物理特性还没做，等准备上代码训练的时候加。现在在做navigation2。