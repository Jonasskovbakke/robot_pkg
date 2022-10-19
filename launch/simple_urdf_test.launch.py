import os
from glob import glob
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'robot_pkg'
    file_subpath = 'robot.urdf.xacro'


    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    print(xacro_file)
    robot_description_raw = xacro.process_file(xacro_file).toxml()


    # Configure the nodes
    # Define robot state publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw}] # add other parameters here if required
    )

    # Define joint state publisher gui node
    node_joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        output="screen",
    )

    # Find rviz config file 
    rviz_config = os.path.join(
      get_package_share_directory('robot_pkg'),
      'rviz_simple_urdf_test.rviz'
      )
    # Define rviz launch node
    rviz = Node(
         package='rviz2',
         executable='rviz2',
         name='rviz2',
         arguments=['-d', rviz_config]
      )
    

    # Run the node
    return LaunchDescription([
        node_robot_state_publisher,
        node_joint_state_publisher_gui,
        rviz,
    ])