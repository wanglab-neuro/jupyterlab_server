#!/bin/bash

# Adapted from Bootstrap example script
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# - The first parameter for the Bootstrap Script is the USER.
USER=$1
if [ "$USER" == "" ]; then
    exit 1
fi

# Start the Bootstrap Process
echo "bootstrap process running for user $USER ..."

# Base Directory: All Directories for the user will be below this point. 
# This home directory is in the Jupyterhub container, and will be mounted to the spawned user container
BASE_DIRECTORY=/home

# User Directory: That's the private directory for the user to be created, if none exists
USER_DIRECTORY=$BASE_DIRECTORY/$USER
WORK_DIRECTORY=$USER_DIRECTORY/work
if [ ! -d "$WORK_DIRECTORY" ]; then
    mkdir -p $WORK_DIRECTORY
fi

# Create How-to file if it doesn't exist 
if [ ! -f "$WORK_DIRECTORY/HowTo.md" ]; then
    echo $2 > "$WORK_DIRECTORY/HowTo.md"
fi

# Create Tutorial directory if none exists
TUTORIAL_DIRECTORY=$WORK_DIRECTORY/tutorials

if [ -d "$TUTORIAL_DIRECTORY" ]; then
    echo "Tutorial directory for user already exists. Skipped"
else
    echo "Creating a tutorials directory for the user: $TUTORIAL_DIRECTORY"
    mkdir $TUTORIAL_DIRECTORY

    echo "Initial content loading for user"
    cd $TUTORIAL_DIRECTORY
    
    {
        echo "### Wang lab Github repositories"
        echo "https://github.com/wanglab-neuro"
        echo "### Neurodata Without Borders "
        echo "https://github.com/NeurodataWithoutBorders"
        echo "### Spike Interface"
        echo "https://spikeinterface.readthedocs.io/"
        echo "### KiloSort"
        echo "https://github.com/MouseLand/Kilosort"
        echo "### suite2p"
        echo "https://github.com/MouseLand/suite2p"
        echo "### CaImAn"
        echo "https://caiman.readthedocs.io/en/master/"
        echo "### MIN1PIPE"
        echo "https://github.com/JinghaoLu/MIN1PIPE"
        echo "### DeepLabCut"
        echo "https://deeplabcut.github.io/DeepLabCut"
    }> Resources.md

    # wget https://github.com/jakevdp/PythonDataScienceHandbook/archive/HEAD.zip
    # unzip -o HEAD.zip #-d "PythonDataScienceHandbook/"
    # rm HEAD.zip
    git clone "https://github.com/jakevdp/PythonDataScienceHandbook.git" "Python-Data-Science-Handbook"
    git clone "https://github.com/patrickmineault/research_code" "Writing-Good-Research-Code"
    git clone "https://github.com/NeurodataWithoutBorders/nwb_tutorial.git" "Neurodata-Without-Borders"
    git clone "https://github.com/LorenFrankLab/nwb_datajoint.git" "Frank-lab-NWB-Datajoint-pipeline"

    NEUROPIXELS_DIR="Visual-Coding-Neuropixels"
    mkdir $NEUROPIXELS_DIR && cd "$_"
    wget https://allensdk.readthedocs.io/en/latest/_static/examples/nb/ecephys_quickstart.ipynb
    wget https://allensdk.readthedocs.io/en/latest/_static/examples/nb/ecephys_session.ipynb
fi

exit 0