from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'rosmaster_app'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'yolo_model'), glob('yolo_model/*.pt')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ica',
    maintainer_email='desprado233@163.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'speaker = rosmaster_app.speaker:main',
            'partol_node = rosmaster_app.partol_node:main',
            'car_control = rosmaster_app.car_control:main',
            'auto_car = rosmaster_app.auto_car:main',
            'topic_listener = rosmaster_app.topic_listener:main',
            'ros_to_cv = rosmaster_app.ros_to_cv:main',
            'object_detect = rosmaster_app.object_detect:main'
        ],
    },
)
