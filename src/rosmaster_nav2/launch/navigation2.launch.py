import os
from launch import LaunchDescription
from launch import substitutions, launch_description_sources
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    ld = LaunchDescription()
    rosmaster_nav2_dir = FindPackageShare('rosmaster_nav2').find('rosmaster_nav2')
    nav2_bringup_dir = FindPackageShare('nav2_bringup').find('nav2_bringup')
    rosmaster_urdf_dir = FindPackageShare('rosmaster_x3').find('rosmaster_x3') 

    rviz_config_path = os.path.join(nav2_bringup_dir, 'rviz', 'nav2_default_view.rviz')
    urdf_model_path = os.path.join(rosmaster_urdf_dir, 'urdf', 'yahboomcar_x3.urdf')

    use_sim_time = substitutions.LaunchConfiguration('use_sim_time', default='true')
    map_yaml_path = substitutions.LaunchConfiguration('map', default=os.path.join(rosmaster_nav2_dir, 'map', 'room.yaml'))
    nav2_para_path = substitutions.LaunchConfiguration('params_file', default=os.path.join(rosmaster_nav2_dir, 'config', 'nav2_params.yaml'))

    start_nav2_cmd = IncludeLaunchDescription(
        launch_description_sources.PythonLaunchDescriptionSource([nav2_bringup_dir, '/launch', '/bringup_launch.py']),
        launch_arguments={'map': map_yaml_path,
                          'use_sim_time': use_sim_time,
                          'params_file': nav2_para_path}.items()
    )

    spawn_entity_cmd = Node(
        package='rviz2', 
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path], 
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen')
    
    joint_state_publisher_node = Node(
    package='joint_state_publisher_gui',
    executable='joint_state_publisher_gui',
    name='joint_state_publisher_gui',
    arguments=[urdf_model_path]
    )
    
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        arguments=[urdf_model_path]
        )

    ld.add_action(start_nav2_cmd)
    ld.add_action(spawn_entity_cmd)
    ld.add_action(robot_state_publisher_node)
    ld.add_action(joint_state_publisher_node)

    return ld
