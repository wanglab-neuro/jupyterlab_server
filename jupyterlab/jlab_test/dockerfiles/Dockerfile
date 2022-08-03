FROM jupyter/tensorflow-notebook:hub-2.3.1

LABEL maintainer="Vincent Prevosto <prevosto@mit.edu>"

#COPY --from=tensorflow/tensorflow:latest-gpu-py3-jupyter /tf/tensorflow-tutorials ./tensorflow-tutorials
COPY --from=jupyter/base-notebook /usr/local/bin/fix-permissions /usr/local/bin/fix-permissions
COPY packages packages

USER root

RUN fix-permissions /home/$NB_USER/packages/

#Add user to jhub_users group, to get wr permissions to shared folder 
RUN groupadd jhub_users 
RUN usermod -aG jhub_users ${NB_USER}

#Switch to user
USER $NB_UID

RUN conda update --all --quiet --yes

# -- add packages available in conda
#    (relies on earlier-configured conda channels: first conda-forge, then defaults)
RUN conda install --quiet --yes \
    jupyter_contrib_nbextensions \
    jupyterlab \
    && conda clean -tipsy

# run with `docker run -it --rm --gpus all -p 8888:8888 jlab_test`