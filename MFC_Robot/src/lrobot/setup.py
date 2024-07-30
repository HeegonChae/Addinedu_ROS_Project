from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'lrobot'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # ('share/' + package_name + '/launch', ['launch/robot_controller_launch.py']),
        # ('share/' + package_name + '/launch', ['launch/jps_path_planner_launch.py']),
        # ('share/' + package_name + '/launch', ['launch/path_server_launch.py']),
        # ('share/' + package_name + '/launch', ['launch/robot_drive_launch.py']),
        # ('share/' + package_name + '/launch', ['launch/robot_launch.py']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
        (os.path.join('share', package_name, 'msg'), glob('msgs/*.msg')),
        ('share/' + package_name + '/maps', glob('maps/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ys',
    maintainer_email='ysu0415@gmail.com',
    description='lrobot package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_controller = lrobot.robot_controller:main',
            'jps_path_planner = lrobot.jps_path_planner:main',
            'robot_control = lrobot.robot_control:main',
            'target_pose_publisher = lrobot.target_pose_publisher:main',
            'robot_manager = lrobot.robot_manager:main',
            'path_server = lrobot.path_server:main',
            'robot_drive = lrobot.robot_drive:main',
            'a_star = lrobot.astar:main',
        ],
    },
)
