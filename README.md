# 基于ROS2机器人操控系统和Navigation2导航框架的自动巡检机器人

## 1.项目介绍
本项目基于ROS2、Navigation2和Yolo设计了一个自动巡检机器人，该机器人在Gazebo仿真环境中运行。机器人可以依照设定的路点进行巡检，每到达一个路点时播放到达的目标点信息，同时车载的摄像头会实时检测是否发现目标物体，并在发现目标物体时进行数量统计、发音警告并拍照保存。小车具备静态和动态避障功能，且能够在受困时发音播报并脱困。

各功能包的功能如下:
- patrol_interfaces:巡检机器人相关消息接口
- rosmaster_x3:机器人描述文件，包含Gazebo仿真等相关配置
- rosmaster_nav2:配置机器人导航运行所需的文件，包含Navigation2等导航配置文件
- rosmaster_app：机器人巡检应用，包含到点播报、目标检测，拍照保存等功能

## 2.使用说明

本项目的开发平台信息如下：

- 操作系统：Ubuntu22.04
- ROS版本：ROS2-Humble 

### 2.1 安装

本项目采用slam-toolbox实现同步定位与地图构建，导航采用Navigation2，仿真采用Gazebo，运动控制采用ros2-control实现，在使用colcon build构建前请先安装依赖，指令如下：

1.安装slam-toolbox和Navigation2
```bash
sudo apt install ros-$ROS_DISTRO-slam-toolbox ros-$ROS_DISTRO-nav2-bringup
```
2.安装仿真相关功能包
```bash
sudo apt install ros-$ROS_DISTRO-robot-state-publisher ros-$ROS_DISTRO-joint-state-publisher ros-$ROS_DISTRO-gazebo-ros-pkgs ros-$ROS_DISTRO-gazebo-ros-controllers
```
3、安装语音合成和图象相关功能包
```bash
sudo apt install espeak-ng
sudo pip install espeakng
sudo apt install ros-$ROS_DISTRO-tf-transformations
```
4、安装配置环境
```bash
conda create -n rose python=3.8
pip install -r requirements.txt
```

### 2.2运行

安装完依赖后，可以使用colcon工具进行编译和运行。

1.构建功能包和激活环境
```bash
colcon build
source install/setup.bash
```
2.运行仿真
```bash
ros2 launch rosmaster_x3 display_gazebo.launch.py
```
3.运行导航
```bash
ros2 launch rosmaster_nav2 navigation2.launch.py
```
4.进行目标检测
```bash
ros2 run rosmaster_app object_detection.py
```
5.进行巡检
```bash
ros2 launch rosmaster_app autopatrol.launch.py
```

### 3.实机部署

使用docker容器部署到亚博智能小车rosmaster_x3

正在开发中...

### 3.作者
- [Ica](desprado233@163.com)
