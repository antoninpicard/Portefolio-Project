cmake_minimum_required(VERSION 3.0.2)
project(swarm_controller)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  geometry_msgs
  sensor_msgs
  nav_msgs
  swarm_msgs
)

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES swarm_controller
  CATKIN_DEPENDS roscpp rospy std_msgs geometry_msgs sensor_msgs nav_msgs swarm_msgs
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_executable(swarm_controller_node src/swarm_controller_node.cpp)
target_link_libraries(swarm_controller_node ${catkin_LIBRARIES})

add_executable(path_planner_node src/path_planner_node.cpp)
target_link_libraries(path_planner_node ${catkin_LIBRARIES})

add_executable(collision_avoidance_node src/collision_avoidance_node.cpp)
target_link_libraries(collision_avoidance_node ${catkin_LIBRARIES})

catkin_install_python(PROGRAMS
  scripts/drone_simulator.py
  scripts/swarm_intelligence.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
