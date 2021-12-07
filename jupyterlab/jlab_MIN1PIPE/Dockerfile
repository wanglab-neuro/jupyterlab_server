FROM wanglabneuro/jlab_matlab:2021b

LABEL maintainer="Vincent Prevosto <prevosto@mit.edu>"

COPY --from=jupyter/base-notebook /usr/local/bin/fix-permissions /usr/local/bin/fix-permissions

USER root

# switch to matlab environment
SHELL ["conda","run","-n","jmatlab","/bin/bash","-c"]

WORKDIR /srv
RUN git clone https://github.com/JinghaoLu/MIN1PIPE.git

RUN fix-permissions /home/$NB_USER && \
	fix-permissions /srv/MIN1PIPE

RUN ln -s /srv/MIN1PIPE /home/

USER $NB_UID
WORKDIR /home/MIN1PIPE
