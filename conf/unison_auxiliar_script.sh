#!/bin/bash
#
# This script is an auxiliar script to be used by the main script 
# to execute some functions in a remote server
#
###############################################################################

create_directory() {
  # this function will try to create a directory that was passed through
  # --directory argument
  DIRECTORY=$1
  if [ -d ${DIRECTORY} ]
  then
    exit 2
  else
    mkdir -p ${DIRECTORY}
    if [ "$?" = "0" ]
    then
      exit 0
    else
      exit 1
    fi
  fi
}

show_help() {
  echo -ne "--create-directory DIR\tCreates a directory to be synced"
}

case $1 in
  --create-directory)
    create_directory $2
    ;;
  *)
    show_help
    ;;
esac