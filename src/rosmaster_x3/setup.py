from setuptools import setup
from glob import glob
import os

package_name = 'rosmaster_x3'

def ls_r(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            relative_path = os.path.join(dir, os.path.relpath(os.path.join(root, file), dir))
            return relative_path

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/**')),
        (os.path.join('share', package_name, 'world'), glob('world/**')),
        (os.path.join('share', package_name, 'meshes/mecanum'), glob('meshes/mecanum/*.STL')),
        (os.path.join('share', package_name, 'meshes/sensor'), glob('meshes/sensor/*.STL')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'model'), [ls_r('model')]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ica_l',
    maintainer_email='ica_l@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
