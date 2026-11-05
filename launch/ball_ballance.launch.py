from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='screenpant',              # nombre de tu paquete
            executable='ball_ballance',              # ejecutable (el que pusiste en setup.py entry_points)
            name='touchscreen_node',
            parameters=[
                {"device_path": "/dev/input/event19"},
                {"frame_id": "touchscreen_frame"}
            ],
            output='screen'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', '/home/andre/ros2_ws/src/screenpant/config/touchscreen.rviz']  
            # ruta opcional a un config .rviz para cargar tu visualización automáticamente
        )
    ])
