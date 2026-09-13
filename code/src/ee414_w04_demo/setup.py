from glob import glob

from setuptools import find_packages, setup

package_name = 'ee414_w04_demo'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/urdf', glob('urdf/*')),
        ('share/' + package_name + '/worlds', glob('worlds/*')),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/rviz', glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Anis Koubaa',
    maintainer_email='akoubaa@alfaisal.edu',
    description='EE 414 Week 4 — differential-drive kinematics, demonstrated by running.',
    license='TODO',
    entry_points={
        'console_scripts': [
            'wheels_to_body  = ee414_w04_demo.wheels_to_body:main',
            'body_to_wheels  = ee414_w04_demo.body_to_wheels:main',
            'quaternion_demo = ee414_w04_demo.quaternion_demo:main',
            'pose_watch      = ee414_w04_demo.pose_watch:main',
            'drive           = ee414_w04_demo.drive:main',
            'dead_reckoning  = ee414_w04_demo.dead_reckoning:main',
        ],
    },
)
