# Install script for directory: /usr/src/googletest

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
<<<<<<< HEAD
<<<<<<< HEAD
  set(CMAKE_INSTALL_PREFIX "/home/pham/enph353_ws/install")
=======
  set(CMAKE_INSTALL_PREFIX "/home/gabriel/ENPH353/install")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
  set(CMAKE_INSTALL_PREFIX "/home/gabriel/ENPH353/install")
=======
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

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
<<<<<<< HEAD
<<<<<<< HEAD
  include("/home/pham/enph353_ws/build/gtest/googlemock/cmake_install.cmake")
=======
  include("/home/gabriel/ENPH353/build/gtest/googlemock/cmake_install.cmake")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
  include("/home/gabriel/ENPH353/build/gtest/googlemock/cmake_install.cmake")
=======
  include("/home/pham/enph353_ws/build/gtest/googlemock/cmake_install.cmake")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938

endif()

