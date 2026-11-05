from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([

        # Nodo publicador: lee del touchscreen y publica en /touch_coords
        Node(package='screenpant', executable='touch_3', name='touchscreen_publisher', output='screen',
            parameters=[{"device_path": "/dev/input/event18"}, {"frame_id": "touchscreen_frame"}]),

        # Nodo suscriptor → transforma a TF
        Node(package='screenpant', executable='touch_2', name='touch_to_tf_subscriber', output='screen'),

        # RViz2 con tu configuración
        Node(package='rviz2', executable='rviz2', name='rviz2',
             arguments=['-d', '/home/andre/ros2_ws/src/screenpant/config/touchscreen.rviz']),
             
        Node(package='rqt_graph', executable='rqt_graph', name='rqt_graph'),

        Node(package='rqt_plot', executable='rqt_plot', name='rqt_plot')
    ])
