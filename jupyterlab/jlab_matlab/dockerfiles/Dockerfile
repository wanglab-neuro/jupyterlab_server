FROM jupyter/scipy-notebook:latest

LABEL maintainer="Vincent Prevosto"

# update Anaconda and install pip 
RUN conda update -y conda && \
     conda install -y pip

USER root

# APT packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create shared user directories (mount shared as volume when running container)  
RUN mkdir -p /srv/shared_files && \
    mkdir -p /srv/shared_code && \
    groupadd jhub_users && \
    chown root:jhub_users /srv/shared_files && \
    chown root:jhub_users /srv/shared_code && \
    chmod 777 /srv/shared_files && \
    chmod g+s /srv/shared_code && \
    cd /etc/skel/ && \
    ln -s /srv/shared_files shared_files && \
    ln -s /srv/shared_code shared_code

USER $NB_UID

COPY --from=matlab_om:2021b /usr/local/MATLAB/R2021b /usr/local/MATLAB/R2021b
COPY packages packages

# Conda installs
RUN conda install --quiet --yes \
    jupyterhub \
    jupyterlab \
    'r-base' \
    'r-irkernel' && \
    conda install -y -c conda-forge nb_conda_kernels \
    jupyter_contrib_nbextensions \
    jupyterlab-git && \
    conda clean -tipsy

# Install Matlab kernel in dedicated environnement
RUN conda env create -f packages/jmatlab_env.yml
SHELL ["conda","run","-n","jmatlab","/bin/bash","-c"]
RUN conda install --quiet --yes ipykernel
RUN python -m ipykernel install --user --name jmatlab --display-name "jmatlab"
RUN pip install -U -r packages/jmatlab_requirements.txt
RUN cd /usr/local/MATLAB/R2021b/extern/engines/python && \
    python setup.py install

USER root
RUN rm -rf packages
