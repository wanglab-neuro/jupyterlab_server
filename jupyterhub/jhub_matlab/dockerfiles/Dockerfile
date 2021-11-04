FROM jupyter/scipy-notebook
# Anaconda 4.10.3 installed in /opt/conda/

COPY --from=matlab_om:2021b /usr/local/MATLAB/R2021b /usr/local/MATLAB/R2021b
COPY packages packages

# update Anaconda and install pip 
RUN conda update -y conda && \
     conda install -y pip

RUN conda install -y -c conda-forge jupyterhub \
   nb_conda_kernels \
   jupyter_contrib_nbextensions \
   jupyterlab-git

# Install R kernel
RUN conda install --quiet --yes \
    'r-base' \
    'r-irkernel' && \
    conda clean -tipsy

# switch to root to be able to create directories 
USER root

# install native authenticator package
RUN cd /home && \
    git clone https://github.com/jupyterhub/nativeauthenticator.git && \
    cd nativeauthenticator && \
    pip install -e .

# install proxy
RUN npm install -g configurable-http-proxy

# Copy the JupyterHub configuration in the container
RUN mkdir /etc/jupyterhub
COPY jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py

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

# Install Matlab kernel in dedicated environnement
RUN conda env create -f packages/jmatlab_env.yml
SHELL ["conda","run","-n","jmatlab","/bin/bash","-c"]
RUN python -m ipykernel install --name jmatlab --display-name "jmatlab"
RUN conda install -y -c conda-forge jupyterlab
RUN pip install -U -r packages/jmatlab_requirements.txt
RUN rm -rf packages
RUN cd /usr/local/MATLAB/R2021b/extern/engines/python && \
    python setup.py install

# Download script to automatically stop idle single-user servers
RUN wget https://raw.githubusercontent.com/jupyterhub/jupyterhub/0.9.3/examples/cull-idle/cull_idle_servers.py


# Go back to base env just in case
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]

CMD ["jupyterhub","-f","/etc/jupyterhub/jupyterhub_config.py"]
