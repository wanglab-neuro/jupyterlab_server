FROM jupyter/base-notebook:hub-1.5.0

LABEL maintainer="Vincent Prevosto <prevosto@mit.edu>"

# Copy installation files
COPY packages packages
COPY --from=wanglabneuro/matlab_om:2021b /usr/local/MATLAB/R2021b /usr/local/MATLAB/R2021b

USER root
# APT packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    tzdata \
    scilab && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN fix-permissions $CONDA_DIR && \
fix-permissions /home/$NB_USER && \
fix-permissions /home/$NB_USER/packages/

#Add user to jhub_users group, to get wr permissions to shared folder 
RUN groupadd jhub_users 
RUN usermod -aG jhub_users ${NB_USER}

#Switch to user
USER $NB_UID

# update Anaconda and install pip 
RUN conda update -y conda && \
     conda install -y pip

# Conda installs

RUN conda config --set channel_priority flexible && \
    conda install -y -c conda-forge nb_conda_kernels \
    jupyter_contrib_nbextensions \
    jupyterlab-git \
    pynwb && \
    conda clean -tipsy

# Create Matlab kernel environment
RUN conda env create -f packages/jmatlab_env.yml
SHELL ["conda","run","-n","jmatlab","/bin/bash","-c"]
RUN conda install --quiet --yes ipykernel && \
    python -m ipykernel install --user --name jmatlab --display-name "Matlab" && \
    pip install -U -r packages/jmatlab_requirements.txt && \
    cd /usr/local/MATLAB/R2021b/extern/engines/python && \
    python setup.py install

RUN rm -rf packages

# Make sue to switch back to user (avoid running ui containers as root)
USER $NB_UID
