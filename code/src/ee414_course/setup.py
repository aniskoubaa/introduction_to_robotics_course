from glob import glob

from setuptools import find_packages, setup

package_name = 'ee414_course'

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
    description='EE 414 — Introduction to Robotics: every program the course runs, in one package.',
    license='CC BY-NC-SA 4.0',
    entry_points={
        'console_scripts': [
            # ---- the LECTURE programs (were ee414_w04_demo until 2026-09-13) ----
            # Each one exists to make a slide's claim visible on a projector.
            'wheels_to_body  = ee414_course.wheels_to_body:main',
            'body_to_wheels  = ee414_course.body_to_wheels:main',
            'quaternion_demo = ee414_course.quaternion_demo:main',
            'pose_watch      = ee414_course.pose_watch:main',
            'drive           = ee414_course.drive:main',
            'dead_reckoning  = ee414_course.dead_reckoning:main',

            # ---- the STUDENT programs: the shape they write themselves ----
            # No simulator needed — the model as arithmetic
            'kinematics   = ee414_course.kinematics:main',
            'angle_wrap   = ee414_course.angle_wrap:main',
            # Needs a simulator
            'pose_monitor = ee414_course.pose_monitor:main',
            'nonholonomic = ee414_course.nonholonomic:main',
            'turtle_mover = ee414_course.turtle_mover:main',
            'move_rotate  = ee414_course.move_rotate:main',
            'go_to_goal   = ee414_course.go_to_goal:main',

            # Beginner versions: the same seven ideas, each in about forty
            # lines with nothing clever in them. These are what goes on the
            # projector during the explanation; the full versions above are
            # what students read afterwards.
            'simple_kinematics   = ee414_course.beginner_student_freindly.simple_kinematics:main',
            'simple_angle_wrap   = ee414_course.beginner_student_freindly.simple_angle_wrap:main',
            'simple_pose_reader  = ee414_course.beginner_student_freindly.simple_pose_reader:main',
            'simple_nonholonomic = ee414_course.beginner_student_freindly.simple_nonholonomic:main',
            'simple_move         = ee414_course.beginner_student_freindly.simple_move:main',
            'simple_square       = ee414_course.beginner_student_freindly.simple_square:main',
            'simple_go_to_goal   = ee414_course.beginner_student_freindly.simple_go_to_goal:main',
        ],
    },
)
