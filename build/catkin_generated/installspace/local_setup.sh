#!/usr/bin/env sh
# generated from catkin/cmake/template/local_setup.sh.in

# since this file is sourced either use the provided _CATKIN_SETUP_DIR
# or fall back to the destination set at configure time
<<<<<<< HEAD
<<<<<<< HEAD
: ${_CATKIN_SETUP_DIR:=/home/pham/enph353_ws/install}
=======
: ${_CATKIN_SETUP_DIR:=/home/gabriel/ENPH353/install}
>>>>>>> cc9906bc7e8abb9ac618fd1f8b6235d2629eebb2
=======
: ${_CATKIN_SETUP_DIR:=/home/gabriel/ENPH353/install}
=======
: ${_CATKIN_SETUP_DIR:=/home/pham/enph353_ws/install}
>>>>>>> f88bb8e013b83310b4c210ccd19fd9b85fadc106
>>>>>>> e67f4e1086cfd9c4820dcf6ce86b0931c9d58938
CATKIN_SETUP_UTIL_ARGS="--extend --local"
. "$_CATKIN_SETUP_DIR/setup.sh"
unset CATKIN_SETUP_UTIL_ARGS
