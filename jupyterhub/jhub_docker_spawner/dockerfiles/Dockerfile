FROM jupyterhub/jupyterhub:1.4.2

COPY jupyterhub_config.py .

RUN pip install \
#    dockerspawner==12.1.0 \
    dockerspawner==0.11.1 \
    oauthenticator==0.8.0 \
#    jhub_cas_authenticator==1.0.0 \
    jupyterhub-nativeauthenticator==1.0.5 \
#    jupyterhub-kerberosauthenticator \
    jupyterhub-idle-culler
