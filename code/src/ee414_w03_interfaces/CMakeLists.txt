cmake_minimum_required(VERSION 3.8)
project(ee414_w03_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/WheelState.msg"
  "srv/ResetOdom.srv"
  DEPENDENCIES std_msgs
)

ament_package()
