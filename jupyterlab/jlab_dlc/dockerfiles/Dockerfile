FROM jupyter/tensorflow-notebook

LABEL maintainer="Vincent Prevosto <prevosto@mit.edu>"

#COPY --from=tensorflow/tensorflow:latest-gpu-py3-jupyter /tf/tensorflow-tutorials ./tensorflow-tutorials
COPY --from=jupyter/base-notebook /usr/local/bin/fix-permissions /usr/local/bin/fix-permissions
COPY packages packages
COPY --from=deeplabcut/deeplabcut:latest-gui-jupyter /app/examples /media/examples

USER root
# APT packages
RUN apt update && \
    apt install -y --no-install-recommends \
    #wget \
    #gcc \
    fonts-dejavu && \
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
    conda install -y -c conda-forge \
    jupyterlab \
    nb_conda_kernels \
    jupyter_contrib_nbextensions \
    jupyterlab-git 

RUN conda config --set channel_priority strict && \
    conda install -y -c conda-forge \
    jupyterlab-nvdashboard && \
    conda clean -tipsy

# Install DLC with pip
# RUN pip install --no-cache-dir --upgrade "deeplabcut>=2.2.0.2"

# Create environment
#RUN wget http://www.mackenziemathislab.org/s/DEEPLABCUT.yaml
RUN conda env create -f packages/deeplabcut_env.yml
SHELL ["conda","run","-n","deeplabcut","/bin/bash","-c"]
RUN conda install --quiet --yes ipykernel && \
    python -m ipykernel install --user --name deeplabcut --display-name "DeepLabCut"
RUN pip install -U -r packages/deeplabcut_requirements.txt

#SHELL ["/bin/bash","-c"]
#RUN conda init
#RUN echo 'conda activate DEEPLABCUT' >> ~/.bashrc

#RUN rm -rf packages

# Make sure to switch back to user (avoid running ui containers as root)
#USER $NB_UID