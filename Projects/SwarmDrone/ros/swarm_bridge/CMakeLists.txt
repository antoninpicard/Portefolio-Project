cmake_minimum_required(VERSION 3.0.2)
project(swarm_bridge)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  geometry_msgs
  nav_msgs
  swarm_msgs
)

catkin_package(
  CATKIN_DEPENDS rospy std_msgs geometry_msgs nav_msgs swarm_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  scripts/bridge_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
