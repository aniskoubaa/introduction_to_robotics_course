#!/usr/bin/env python3
"""Open the minimal differential-drive model in RViz2.

Slide reference: "The Model Needs Two Numbers. Where Do They Live?"

    ros2 launch ee414_w04_demo view_model.launch.py

Three nodes, and it is worth naming what each one does:

  robot_state_publisher      reads the URDF, and publishes where every link is
  joint_state_publisher_gui  a slider per joint, so you can spin the wheels by
                             hand and watch the frames move with them
  rviz2                      draws it

The URDF cannot be passed on the command line with -p: it is multi-line XML,
and the argument parser rejects it. Reading the file here is the normal way,
and it is why launch files exist.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    path = LaunchConfiguration("model").perform(context)
    with open(path, "r") as handle:
        urdf = handle.read()

    pkg = get_package_share_directory("ee414_w04_demo")
    rviz_config = os.path.join(pkg, "rviz", "model.rviz")

    return [
        Node(package="robot_state_publisher",
             executable="robot_state_publisher",
             output="screen",
             parameters=[{"robot_description": urdf}]),
        Node(package="joint_state_publisher_gui",
             executable="joint_state_publisher_gui",
             output="screen"),
        Node(package="rviz2",
             executable="rviz2",
             output="screen",
             arguments=["-d", rviz_config] if os.path.exists(rviz_config) else []),
    ]


def generate_launch_description():
    pkg = get_package_share_directory("ee414_w04_demo")
    default_model = os.path.join(pkg, "urdf", "burger_min.urdf")

    return LaunchDescription([
        DeclareLaunchArgument(
            "model", default_value=default_model,
            description="Absolute path to the URDF to display"),
        OpaqueFunction(function=launch_setup),
    ])
