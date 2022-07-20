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

remove_unison_tmp_files() {
  # removes *.unison.tmp files
  DIRECTORY=$1
  if [ -d ${DIRECTORY} ]
  then
    find ${DIRECTORY} -name ".*.unison.tmp" -type f -delete
    if [ $? -eq 0 ]
    then
      exit 0
    else
      exit 1
    fi
  else
    exit 2
  fi
}

show_help() {
  echo -e "Usage: ${0} [OPTION]"
  echo -e "This script is used by unisonManager to execute actions on remote server\n"
  echo -e "--create-directory  DIR\tCreates a directory to be synced"
  echo -e "--remove-temp-files DIR\tRemoves all unison.tmp files\n"
}

case $1 in
  --create-directory)
    create_directory $2
    ;;
  --remove-temp-files)
    remove_unison_tmp_files $2
    ;;
  *)
    show_help
    ;;
esac