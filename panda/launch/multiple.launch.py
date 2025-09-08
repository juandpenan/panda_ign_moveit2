from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import TextSubstitution

import os

def generate_launch_description():

    bringup_dir = get_package_share_directory('panda')
    launch_dir = os.path.join(bringup_dir, 'launch')
    launch_file = os.path.join(launch_dir, 'ign.launch.py')

    is_public_sim = LaunchConfiguration('is_public_sim', default='True')
    world_name = LaunchConfiguration('world_name', default='manipulation')
    # x = LaunchConfiguration('x', default='-5.5')
    # y = LaunchConfiguration('y', default='-3.8')
    # Y = LaunchConfiguration('Y', default='1.5708')

    robots = [
        {
            'name': 'robot1',
            'x': '-5.5',
            'y': '-3.8',
            'z': '0.0',
            'R': '0.0',
            'P': '0.0',
            'Y': '1.5708'
        },
        # {
        #     'name': 'tiago2',
        #     'x': '-4.5',
        #     'y': '-3.8',
        #     'z': '0.0',
        #     'R': '0.0',
        #     'P': '0.0',
        #     'Y': '0.0'
        # },
    ]

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('br2_gazebo_worlds'),
                         'launch', 'br2_gazebo.launch.py')
        ),
        launch_arguments={
            'world_name': world_name,
            'debug': 'False'
        }.items()
    )

    actions = [gazebo_launch]
    for r in robots:
        actions.append(
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(launch_file),
                launch_arguments={
                    'name': TextSubstitution(text=r['name']),
                    'prefix': TextSubstitution(text=r['name'] + '_'),
                    'namespace': TextSubstitution(text=r['name']),
                    'use_simulator': TextSubstitution(text='false'),
                    'robot_x': TextSubstitution(text=r['x']),
                    'robot_y': TextSubstitution(text=r['y']),
                    'robot_z': TextSubstitution(text=r['z']),
                    'robot_R': TextSubstitution(text=r['R']),
                    'robot_P': TextSubstitution(text=r['P']),
                    'robot_Y': TextSubstitution(text=r['Y']),
                }.items()
            )
        )

    return LaunchDescription(actions)
