FROM jupyter/scipy-notebook:hub-1.4.2

LABEL maintainer="Vincent Prevosto <prevosto@mit.edu>"

USER root

# Copy installation files
COPY --from=matlab_om:2021b /usr/local/MATLAB/R2021b /usr/local/MATLAB/R2021b
COPY packages packages

# APT packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    tzdata \
    python3-dev \
    scilab && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# update Anaconda and install pip 
RUN conda update -y conda && \
     conda install -y pip

# Create environments
# Matlab kernel 
RUN conda env create -f packages/jmatlab_env.yml

# AllenSDK environnement
RUN conda env create -f packages/allensdk_env.yml

# NWB/Datajoint environnement
RUN conda env create -f packages/nwb_datajoint_env.yml

#Switch to user
USER $NB_UID

# Conda installs
RUN conda install --quiet --yes \
    'r-base' \
    'r-irkernel' \
    'r-plyr' \
    'r-devtools' \
    'r-tidyverse' \
    'r-shiny' \
    'r-rmarkdown' \
    'r-rsqlite' \
    'r-reshape2' \
    'r-caret' \
    'r-rcurl' \
    'r-crayon' \
    'r-randomforest' \
    'r-htmltools' \
    'r-sparklyr' \
    'r-htmlwidgets' \
    'r-hexbin' \
    'jupyterhub' \
    'julia' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR
    #fix-permissions /home/$NB_USER

RUN conda config --set channel_priority flexible && \
    conda install -y -c conda-forge nb_conda_kernels \
    jupyter_contrib_nbextensions \
    jupyterlab-git \
    pynwb && \
    conda clean -tipsy

ENV CPATH=$CONDA_DIR/include

# Make kernels available
SHELL ["conda","run","-n","jmatlab","/bin/bash","-c"]
RUN conda install --quiet --yes ipykernel && \
    python -m ipykernel install --user --name jmatlab --display-name "Matlab" && \
    pip install -U -r packages/jmatlab_requirements.txt && \
    cd /usr/local/MATLAB/R2021b/extern/engines/python && \
    python setup.py install

SHELL ["conda","run","-n","allensdk","/bin/bash","-c"]
RUN conda install --quiet --yes ipykernel && \
    python -m ipykernel install --user --name allensdk --display-name "AllenSDK" && \
    pip install -U -r packages/allensdk_requirements.txt

SHELL ["conda","run","-n","nwb_datajoint","/bin/bash","-c"]
RUN conda install --quiet --yes ipykernel && \
    python -m ipykernel install --user --name nwb_datajoint --display-name "NWB Datajoint" && \
    pip install -U -r packages/nwb_datajoint_requirements.txt

USER root
SHELL ["/bin/sh", "-c"]
RUN rm -rf packages

#Add user to jhub_users group, to get wr permissions to shared folder 
RUN groupadd jhub_users 
RUN usermod -aG jhub_users ${NB_USER}
#RUN useradd -u ${NB_UID} -g jhub_users -s /bin/sh ${NB_USER}

# Switch back to user (avoid running ui containers as root)
USER $NB_UID