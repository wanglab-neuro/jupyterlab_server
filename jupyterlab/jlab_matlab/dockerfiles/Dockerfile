FROM jupyter/scipy-notebook:hub-1.4.2

LABEL maintainer="Vincent Prevosto <prevosto@mit.edu>"

USER root

# APT packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    tzdata \
    scilab && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER $NB_UID

COPY --from=matlab_om:2021b /usr/local/MATLAB/R2021b /usr/local/MATLAB/R2021b
COPY packages packages

# Conda installs
RUN conda install --quiet --yes \
    'jupyterhub' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR

RUN conda config --set channel_priority flexible && \
    conda install -y -c conda-forge nb_conda_kernels \
    jupyter_contrib_nbextensions \
    jupyterlab-git && \
    conda clean -tipsy

ENV CPATH=$CONDA_DIR/include

# Install Matlab kernel in dedicated environnement
RUN conda env create -f packages/jmatlab_env.yml
SHELL ["conda","run","-n","jmatlab","/bin/bash","-c"]
RUN conda install --quiet --yes ipykernel
RUN python -m ipykernel install --user --name jmatlab --display-name "Matlab"
RUN pip install -U -r packages/jmatlab_requirements.txt
RUN cd /usr/local/MATLAB/R2021b/extern/engines/python && \
    python setup.py install

USER root
SHELL ["/bin/sh", "-c"]
RUN rm -rf packages

#Add user to jhub_users group, to get wr permissions to shared folder 
RUN groupadd jhub_users 
RUN usermod -aG jhub_users ${NB_USER}

# Switch back to jovyan to avoid container runs as root
USER $NB_UID