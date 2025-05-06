import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    ld = LaunchDescription()
    package_name = 'rosmaster_app'
    autopartol_dir = FindPackageShare(package=package_name).find(package_name)
    autopartol_path = os.path.join(autopartol_dir, 'config', 'partol_config.yaml')

    action_node_partol = Node(
        package='rosmaster_app',
        executable='partol_node',
        parameters=[autopartol_path])
    
    action_node_speaker = Node(
        package='rosmaster_app',
        executable='speaker')

    ld.add_action(action_node_partol)
    ld.add_action(action_node_speaker)


    return ld
