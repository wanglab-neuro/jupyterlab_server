FROM wanglabneuro/jlab_matlab:2021b

LABEL maintainer="Vincent Prevosto <prevosto@mit.edu>"

USER root

# switch to matlab environment
SHELL ["conda","run","-n","jmatlab","/bin/bash","-c"]

WORKDIR /srv
RUN git clone https://github.com/JinghaoLu/MIN1PIPE.git

USER $NB_UID
WORKDIR /home/$NB_USER
RUN ln -s /srv/MIN1PIPE ./MIN1PIPE