<<<<<<< HEAD
<<<<<<< HEAD
# Install script for directory: /home/pham/enph353_ws/src/enph353_ros_lab

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/pham/enph353_ws/install")
=======
# Install script for directory: /home/gabriel/ENPH353/src/enph353_ros_lab

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/gabriel/ENPH353/install")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
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
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
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
<<<<<<< HEAD
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/pham/enph353_ws/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_lab.pc")
=======
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/gabriel/ENPH353/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_lab.pc")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/gabriel/ENPH353/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_lab.pc")
=======
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/pham/enph353_ws/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_lab.pc")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/enph353_ros_lab/cmake" TYPE FILE FILES
<<<<<<< HEAD
<<<<<<< HEAD
    "/home/pham/enph353_ws/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_labConfig.cmake"
    "/home/pham/enph353_ws/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_labConfig-version.cmake"
=======
    "/home/gabriel/ENPH353/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_labConfig.cmake"
    "/home/gabriel/ENPH353/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_labConfig-version.cmake"
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
    "/home/gabriel/ENPH353/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_labConfig.cmake"
    "/home/gabriel/ENPH353/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_labConfig-version.cmake"
=======
    "/home/pham/enph353_ws/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_labConfig.cmake"
    "/home/pham/enph353_ws/build/enph353_ros_lab/catkin_generated/installspace/enph353_ros_labConfig-version.cmake"
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
<<<<<<< HEAD
<<<<<<< HEAD
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/enph353_ros_lab" TYPE FILE FILES "/home/pham/enph353_ws/src/enph353_ros_lab/package.xml")
=======
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/enph353_ros_lab" TYPE FILE FILES "/home/gabriel/ENPH353/src/enph353_ros_lab/package.xml")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/enph353_ros_lab" TYPE FILE FILES "/home/gabriel/ENPH353/src/enph353_ros_lab/package.xml")
=======
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/enph353_ros_lab" TYPE FILE FILES "/home/pham/enph353_ws/src/enph353_ros_lab/package.xml")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
endif()

