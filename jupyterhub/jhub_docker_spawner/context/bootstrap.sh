#!/bin/bash

# Bootstrap example script
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# - The first parameter for the Bootstrap Script is the USER.
USER=$1
if [ "$USER" == "" ]; then
    exit 1
fi
# ----------------------------------------------------------------------------


# This example script will do the following:
# - create one directory for the user $USER in a BASE_DIRECTORY (see below)
# - create a "tutorials" directory within and download and unzip
#   the PythonDataScienceHandbook from GitHub

# Start the Bootstrap Process
echo "bootstrap process running for user $USER ..."

# Base Directory: All Directories for the user will be below this point
BASE_DIRECTORY=/home

# User Directory: That's the private directory for the user to be created, if none exists
USER_DIRECTORY=$BASE_DIRECTORY/$USER

if [ ! -d "$USER_DIRECTORY" ]; then
    echo "...creating a directory for the user: $USER_DIRECTORY"
    mkdir $USER_DIRECTORY
fi
if [ ! -d "$USER_DIRECTORY/work" ]; then
    mkdir "$USER_DIRECTORY/work"
fi

TUTORIAL_DIRECTORY=$USER_DIRECTORY/work/tutorials

if [ -d "$TUTORIAL_DIRECTORY" ]; then
    echo " tutorial directory for user already exists. skipped"
    exit 0 # all good. nothing to do.
else
    echo "...creating a tutorials directory for the user: $TUTORIAL_DIRECTORY"
    mkdir $TUTORIAL_DIRECTORY

    echo "...initial content loading for user ..."
    cd $TUTORIAL_DIRECTORY
    wget https://github.com/jakevdp/PythonDataScienceHandbook/archive/HEAD.zip
    unzip -o HEAD.zip
    rm HEAD.zip
fi
exit 0