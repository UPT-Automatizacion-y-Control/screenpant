from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'screenpant'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='andre',
    maintainer_email='andre@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'touch = screenpant.touch:main',
            'touch_2 = screenpant.touch_2:main',
            'touch_3 = screenpant.touch_3:main',
            'touch_timer = screenpant.touch_timer:main',
            'ball_ballance = screenpant.ball_ballance:main',
            'ball_plate = screenpant.ball_plate:main'
        ],
    },
)
