<<<<<<< HEAD
<<<<<<< HEAD
# Install script for directory: /home/pham/enph353_ws/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/pham/enph353_ws/install")
=======
# Install script for directory: /home/gabriel/ENPH353/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/gabriel/ENPH353/install")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
# Install script for directory: /home/gabriel/ENPH353/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/gabriel/ENPH353/install")
=======
# Install script for directory: /home/pham/enph353_ws/src

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
  
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
        file(MAKE_DIRECTORY "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
      endif()
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin")
        file(WRITE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin" "")
      endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
<<<<<<< HEAD
<<<<<<< HEAD
   "/home/pham/enph353_ws/install/_setup_util.py")
=======
   "/home/gabriel/ENPH353/install/_setup_util.py")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
   "/home/gabriel/ENPH353/install/_setup_util.py")
=======
   "/home/pham/enph353_ws/install/_setup_util.py")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
<<<<<<< HEAD
<<<<<<< HEAD
file(INSTALL DESTINATION "/home/pham/enph353_ws/install" TYPE PROGRAM FILES "/home/pham/enph353_ws/build/catkin_generated/installspace/_setup_util.py")
=======
file(INSTALL DESTINATION "/home/gabriel/ENPH353/install" TYPE PROGRAM FILES "/home/gabriel/ENPH353/build/catkin_generated/installspace/_setup_util.py")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
file(INSTALL DESTINATION "/home/gabriel/ENPH353/install" TYPE PROGRAM FILES "/home/gabriel/ENPH353/build/catkin_generated/installspace/_setup_util.py")
=======
file(INSTALL DESTINATION "/home/pham/enph353_ws/install" TYPE PROGRAM FILES "/home/pham/enph353_ws/build/catkin_generated/installspace/_setup_util.py")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
<<<<<<< HEAD
<<<<<<< HEAD
   "/home/pham/enph353_ws/install/env.sh")
=======
   "/home/gabriel/ENPH353/install/env.sh")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
   "/home/gabriel/ENPH353/install/env.sh")
=======
   "/home/pham/enph353_ws/install/env.sh")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
<<<<<<< HEAD
<<<<<<< HEAD
file(INSTALL DESTINATION "/home/pham/enph353_ws/install" TYPE PROGRAM FILES "/home/pham/enph353_ws/build/catkin_generated/installspace/env.sh")
=======
file(INSTALL DESTINATION "/home/gabriel/ENPH353/install" TYPE PROGRAM FILES "/home/gabriel/ENPH353/build/catkin_generated/installspace/env.sh")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
file(INSTALL DESTINATION "/home/gabriel/ENPH353/install" TYPE PROGRAM FILES "/home/gabriel/ENPH353/build/catkin_generated/installspace/env.sh")
=======
file(INSTALL DESTINATION "/home/pham/enph353_ws/install" TYPE PROGRAM FILES "/home/pham/enph353_ws/build/catkin_generated/installspace/env.sh")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
<<<<<<< HEAD
<<<<<<< HEAD
   "/home/pham/enph353_ws/install/setup.bash;/home/pham/enph353_ws/install/local_setup.bash")
=======
   "/home/gabriel/ENPH353/install/setup.bash;/home/gabriel/ENPH353/install/local_setup.bash")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
   "/home/gabriel/ENPH353/install/setup.bash;/home/gabriel/ENPH353/install/local_setup.bash")
=======
   "/home/pham/enph353_ws/install/setup.bash;/home/pham/enph353_ws/install/local_setup.bash")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
<<<<<<< HEAD
<<<<<<< HEAD
file(INSTALL DESTINATION "/home/pham/enph353_ws/install" TYPE FILE FILES
    "/home/pham/enph353_ws/build/catkin_generated/installspace/setup.bash"
    "/home/pham/enph353_ws/build/catkin_generated/installspace/local_setup.bash"
=======
file(INSTALL DESTINATION "/home/gabriel/ENPH353/install" TYPE FILE FILES
    "/home/gabriel/ENPH353/build/catkin_generated/installspace/setup.bash"
    "/home/gabriel/ENPH353/build/catkin_generated/installspace/local_setup.bash"
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
file(INSTALL DESTINATION "/home/gabriel/ENPH353/install" TYPE FILE FILES
    "/home/gabriel/ENPH353/build/catkin_generated/installspace/setup.bash"
    "/home/gabriel/ENPH353/build/catkin_generated/installspace/local_setup.bash"
=======
file(INSTALL DESTINATION "/home/pham/enph353_ws/install" TYPE FILE FILES
    "/home/pham/enph353_ws/build/catkin_generated/installspace/setup.bash"
    "/home/pham/enph353_ws/build/catkin_generated/installspace/local_setup.bash"
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
<<<<<<< HEAD
<<<<<<< HEAD
   "/home/pham/enph353_ws/install/setup.sh;/home/pham/enph353_ws/install/local_setup.sh")
=======
   "/home/gabriel/ENPH353/install/setup.sh;/home/gabriel/ENPH353/install/local_setup.sh")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
   "/home/gabriel/ENPH353/install/setup.sh;/home/gabriel/ENPH353/install/local_setup.sh")
=======
   "/home/pham/enph353_ws/install/setup.sh;/home/pham/enph353_ws/install/local_setup.sh")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
<<<<<<< HEAD
<<<<<<< HEAD
file(INSTALL DESTINATION "/home/pham/enph353_ws/install" TYPE FILE FILES
    "/home/pham/enph353_ws/build/catkin_generated/installspace/setup.sh"
    "/home/pham/enph353_ws/build/catkin_generated/installspace/local_setup.sh"
=======
file(INSTALL DESTINATION "/home/gabriel/ENPH353/install" TYPE FILE FILES
    "/home/gabriel/ENPH353/build/catkin_generated/installspace/setup.sh"
    "/home/gabriel/ENPH353/build/catkin_generated/installspace/local_setup.sh"
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
file(INSTALL DESTINATION "/home/gabriel/ENPH353/install" TYPE FILE FILES
    "/home/gabriel/ENPH353/build/catkin_generated/installspace/setup.sh"
    "/home/gabriel/ENPH353/build/catkin_generated/installspace/local_setup.sh"
=======
file(INSTALL DESTINATION "/home/pham/enph353_ws/install" TYPE FILE FILES
    "/home/pham/enph353_ws/build/catkin_generated/installspace/setup.sh"
    "/home/pham/enph353_ws/build/catkin_generated/installspace/local_setup.sh"
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
<<<<<<< HEAD
<<<<<<< HEAD
   "/home/pham/enph353_ws/install/setup.zsh;/home/pham/enph353_ws/install/local_setup.zsh")
=======
   "/home/gabriel/ENPH353/install/setup.zsh;/home/gabriel/ENPH353/install/local_setup.zsh")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
   "/home/gabriel/ENPH353/install/setup.zsh;/home/gabriel/ENPH353/install/local_setup.zsh")
=======
   "/home/pham/enph353_ws/install/setup.zsh;/home/pham/enph353_ws/install/local_setup.zsh")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
<<<<<<< HEAD
<<<<<<< HEAD
file(INSTALL DESTINATION "/home/pham/enph353_ws/install" TYPE FILE FILES
    "/home/pham/enph353_ws/build/catkin_generated/installspace/setup.zsh"
    "/home/pham/enph353_ws/build/catkin_generated/installspace/local_setup.zsh"
=======
file(INSTALL DESTINATION "/home/gabriel/ENPH353/install" TYPE FILE FILES
    "/home/gabriel/ENPH353/build/catkin_generated/installspace/setup.zsh"
    "/home/gabriel/ENPH353/build/catkin_generated/installspace/local_setup.zsh"
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
file(INSTALL DESTINATION "/home/gabriel/ENPH353/install" TYPE FILE FILES
    "/home/gabriel/ENPH353/build/catkin_generated/installspace/setup.zsh"
    "/home/gabriel/ENPH353/build/catkin_generated/installspace/local_setup.zsh"
=======
file(INSTALL DESTINATION "/home/pham/enph353_ws/install" TYPE FILE FILES
    "/home/pham/enph353_ws/build/catkin_generated/installspace/setup.zsh"
    "/home/pham/enph353_ws/build/catkin_generated/installspace/local_setup.zsh"
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
<<<<<<< HEAD
<<<<<<< HEAD
   "/home/pham/enph353_ws/install/.rosinstall")
=======
   "/home/gabriel/ENPH353/install/.rosinstall")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
   "/home/gabriel/ENPH353/install/.rosinstall")
=======
   "/home/pham/enph353_ws/install/.rosinstall")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
<<<<<<< HEAD
<<<<<<< HEAD
file(INSTALL DESTINATION "/home/pham/enph353_ws/install" TYPE FILE FILES "/home/pham/enph353_ws/build/catkin_generated/installspace/.rosinstall")
=======
file(INSTALL DESTINATION "/home/gabriel/ENPH353/install" TYPE FILE FILES "/home/gabriel/ENPH353/build/catkin_generated/installspace/.rosinstall")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
file(INSTALL DESTINATION "/home/gabriel/ENPH353/install" TYPE FILE FILES "/home/gabriel/ENPH353/build/catkin_generated/installspace/.rosinstall")
=======
file(INSTALL DESTINATION "/home/pham/enph353_ws/install" TYPE FILE FILES "/home/pham/enph353_ws/build/catkin_generated/installspace/.rosinstall")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
<<<<<<< HEAD
<<<<<<< HEAD
  include("/home/pham/enph353_ws/build/gtest/cmake_install.cmake")
  include("/home/pham/enph353_ws/build/enph353_ros_lab/cmake_install.cmake")
=======
  include("/home/gabriel/ENPH353/build/gtest/cmake_install.cmake")
  include("/home/gabriel/ENPH353/build/enph353_ros_lab/cmake_install.cmake")
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
  include("/home/gabriel/ENPH353/build/gtest/cmake_install.cmake")
  include("/home/gabriel/ENPH353/build/enph353_ros_lab/cmake_install.cmake")
=======
  include("/home/pham/enph353_ws/build/gtest/cmake_install.cmake")
  include("/home/pham/enph353_ws/build/enph353_ros_lab/cmake_install.cmake")
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
<<<<<<< HEAD
<<<<<<< HEAD
file(WRITE "/home/pham/enph353_ws/build/${CMAKE_INSTALL_MANIFEST}"
=======
file(WRITE "/home/gabriel/ENPH353/build/${CMAKE_INSTALL_MANIFEST}"
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
file(WRITE "/home/gabriel/ENPH353/build/${CMAKE_INSTALL_MANIFEST}"
=======
file(WRITE "/home/pham/enph353_ws/build/${CMAKE_INSTALL_MANIFEST}"
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
