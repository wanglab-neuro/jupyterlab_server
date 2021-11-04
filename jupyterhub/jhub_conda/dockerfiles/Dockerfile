FROM jupyter/scipy-notebook

# Anaconda 4.10.3 installed in /opt/conda/

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

# Download script to automatically stop idle single-user servers
#RUN wget https://raw.githubusercontent.com/jupyterhub/jupyterhub/0.9.3/examples/cull-idle/cull_idle_servers.py

# Copy the JupyterHub configuration in the container
RUN mkdir /etc/jupyterhub
COPY jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py

CMD ["jupyterhub","-f","/etc/jupyterhub/jupyterhub_config.py"]