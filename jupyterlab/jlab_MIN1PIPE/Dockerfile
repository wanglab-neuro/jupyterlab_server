FROM wanglabneuro/jlab_matlab:2021b

LABEL maintainer="Vincent Prevosto <prevosto@mit.edu>"

COPY --from=jupyter/base-notebook /usr/local/bin/fix-permissions /usr/local/bin/fix-permissions
COPY link_package_files.sh /media/link_package_files.sh
COPY startup.m 	/usr/local/MATLAB/R2021b/toolbox/local/
USER root

# switch to matlab environment
SHELL ["conda","run","-n","jmatlab","/bin/bash","-c"]

WORKDIR /srv
RUN git clone https://github.com/wanglab-neuro/MIN1PIPE.git 
#Original repo: https://github.com/JinghaoLu/MIN1PIPE.git

RUN fix-permissions /home/$NB_USER && \
	fix-permissions /srv/MIN1PIPE
RUN ["chmod", "+x", "/media/link_package_files.sh"]

RUN ln -s /srv/MIN1PIPE /home/
# RUN echo "addpath /srv/MIN1PIPE" > /usr/local/MATLAB/R2021b/bin/startup.m

USER $NB_UID
WORKDIR /home/$NB_USER
