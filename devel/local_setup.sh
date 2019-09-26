#!/usr/bin/env sh
# generated from catkin/cmake/template/local_setup.sh.in

# since this file is sourced either use the provided _CATKIN_SETUP_DIR
# or fall back to the destination set at configure time
<<<<<<< HEAD
: ${_CATKIN_SETUP_DIR:=/home/gabriel/ENPH353/devel}
=======
: ${_CATKIN_SETUP_DIR:=/home/pham/enph353_ws/devel}
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
CATKIN_SETUP_UTIL_ARGS="--extend --local"
. "$_CATKIN_SETUP_DIR/setup.sh"
unset CATKIN_SETUP_UTIL_ARGS
