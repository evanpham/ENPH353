execute_process(COMMAND "/home/pham/enph353_gym-gazebo/gym_gazebo/envs/enph353/build/ros_control/controller_manager/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/pham/enph353_gym-gazebo/gym_gazebo/envs/enph353/build/ros_control/controller_manager/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
