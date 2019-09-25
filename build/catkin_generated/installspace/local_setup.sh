#!/usr/bin/env sh
# generated from catkin/cmake/template/local_setup.sh.in

# since this file is sourced either use the provided _CATKIN_SETUP_DIR
# or fall back to the destination set at configure time
<<<<<<< HEAD
: ${_CATKIN_SETUP_DIR:=/home/pham/enph353_ws/install}
=======
: ${_CATKIN_SETUP_DIR:=/home/gabriel/ENPH353/install}
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
CATKIN_SETUP_UTIL_ARGS="--extend --local"
. "$_CATKIN_SETUP_DIR/setup.sh"
unset CATKIN_SETUP_UTIL_ARGS
