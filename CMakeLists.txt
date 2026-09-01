cmake_minimum_required(VERSION 3.8)
project(create3_dock_challenge)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  launch
  worlds
  urdf
  rviz
  meshes
  materials
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  scripts/clean_sim.sh
  scripts/set_safety_override.py
  scripts/test_docker.sh
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
