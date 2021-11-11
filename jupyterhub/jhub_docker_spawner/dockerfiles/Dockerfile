FROM jupyterhub/jupyterhub:1.4.2

# update Anaconda and install pip 
#RUN conda update -y conda && \
#     conda install -y pip

COPY jupyterhub_config.py .

RUN pip install \
    dockerspawner==12.1.0 \
    oauthenticator==0.8.0 \
#    jhub_cas_authenticator==1.0.0 \
    jupyterhub-nativeauthenticator==1.0.5 \
    jupyterhub-idle-culler

# install native authenticator package
#RUN cd /home && \
#    git clone https://github.com/jupyterhub/nativeauthenticator.git && \
#    cd nativeauthenticator && \
#    pip install -e .

# install proxy
RUN npm install -g configurable-http-proxy