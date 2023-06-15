import os
import xacro 
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    urdf_file_name = 'Crawler.xacro'
    urdf = os.path.join(
        get_package_share_directory('urdf_crawler'),
        urdf_file_name)
    doc = xacro.process_file(urdf)
    robot_desc = doc.toprettyxml(indent='  ')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true',),
        DeclareLaunchArgument(
            'rvizconfig',
            default_value='urdf/Crawler.rviz',
            description='Path to rviz config file',),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
            arguments=[urdf]),
        Node(
            package='urdf_crawler',
            executable='state_publisher',
            name='state_publisher',
            output='screen'),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', LaunchConfiguration('rvizconfig')])
    ])
