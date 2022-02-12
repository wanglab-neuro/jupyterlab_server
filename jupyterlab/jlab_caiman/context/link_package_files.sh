#!/bin/bash

WORK_DIRECTORY="/home/jovyan"

# See if there are supporting files in the media folder, and link them to the home directory
files=$(shopt -s nullglob dotglob; echo /media/*)
if (( ${#files} )); then
  #Create target folder if needed
  PACKAGE_DIRECTORY=$WORK_DIRECTORY/Packages
  if [ ! -d "$PACKAGE_DIRECTORY" ]; then
    mkdir -p $PACKAGE_DIRECTORY
  fi
  #Then link files
  for d in /media/*/ ; do
    [ -L "${d%/}" ] && continue
    echo "linking $d to home directory"
    ln -s $d $PACKAGE_DIRECTORY
  done
else 
  echo "Media directory is empty"
fi

# if WORK_DIRECTORY is different from USER_DIRECTORY, make terminal start from there:
# lastline="tail -1 $HOME/.profile"
# if [ "$lastline" != "$WORK_DIRECTORY" ]; then
#   echo "cd $HOME/work" >> ~/.bashrc
# fi
