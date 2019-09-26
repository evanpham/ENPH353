<<<<<<< HEAD
# Install script for directory: /home/gabriel/ENPH353/src/enph353_ros_lab

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/gabriel/ENPH353/install")
=======
# Install script for directory: /home/pham/enph353_ws/src/enph353_ros_lab

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/pham/enph353_ws/install")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
<<<<<<< HEAD
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/gabriel/ENPH353/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_lab.pc")
=======
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/pham/enph353_ws/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_lab.pc")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/enph353_ros_lab/cmake" TYPE FILE FILES
<<<<<<< HEAD
    "/home/gabriel/ENPH353/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_labConfig.cmake"
    "/home/gabriel/ENPH353/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_labConfig-version.cmake"
=======
    "/home/pham/enph353_ws/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_labConfig.cmake"
    "/home/pham/enph353_ws/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_labConfig-version.cmake"
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
<<<<<<< HEAD
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/enph353_ros_lab" TYPE FILE FILES "/home/gabriel/ENPH353/src/enph353_ros_lab/package.xml")
=======
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/enph353_ros_lab" TYPE FILE FILES "/home/pham/enph353_ws/src/enph353_ros_lab/package.xml")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
endif()

