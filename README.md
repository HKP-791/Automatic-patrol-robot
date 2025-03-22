# 基于ROS2机器人操控系统和Navigation2导航框架的自动巡检机器人

## 1.项目介绍
本项目基于ROS2、Navigation2和Yolo设计了一个自动巡检机器人，该机器人在Gazebo仿真环境中运行。机器人可以依照设定的路点进行巡检，每到达一个路店时播放到达的目标点信息，同时车载的摄像头会实时检测是否发现目标物体，并在发现目标物体时进行数量统计、发音警告并拍照保存。小车具备静态和动态避障功能，且能够在受困时发音播报并脱困。

各功能包的功能如下:
- rosmaster_x3:机器人描述文件，包含Gazebo仿真等相关配置
- rosmaster_nav2:配置机器人导航运行所需的文件，包含Navigation2等导航配置文件
- rosmaster_app：机器人巡检应用，包含到点播报、目标检测，拍照保存等功能

## 2.使用说明

本项目的开发平台信息如下：

- 操作系统：Ubuntu22.04
- ROS版本：ROS2-Humble 

### 2.1 安装

本项目采用slam-toolbox，导航采用Navigation2，仿真采用Gazebo，运动控制采用ros2-control实现，在使用colcon build构建前请先安装依赖，指令如下：

1.安装slam-toolbox和Navigation2
```bash
sudo apt install ros-$ROS_DISTRO-slam-toolbox ros-$ROS_DISTRO-nav2-bringup
```
2.安装仿真相关功能包
```bash
sudo apt install ros-$ROS_DISTRO-robot-state-publisher ros-$ROS_DISTRO-joint-state-publisher ros-$ROS_DISTRO-gazebo-ros-pkgs ros-$ROS_DISTRO-gazebo-ros-controllers
```


1.第一次使用要在auto_parking目录下用colcon build编译一下，每次使用前要cd到auto_parking目录下source
2.编写了两个.launch.py，分别用于启动rviz2和建立了世界的gazebo.可以通过下命令启动导入了无人机的rviz2和gazebo。
```bash
ros2 launch rosmaster_x3 display_gazebo.launch.py
ros2 launch rosmaster_x3 display_rviz2.launch.py
```
2.无人车的urdf描述文件和仿真世界的world文件位于位于
```text
/auto_parking/src/rosmaster_x3/urdf/rosmaster_x3.urdf
/auto_parking/src/rosmaster_x3/world/auto_parking.world
```
3.安装语言合成和图像相关功能包

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