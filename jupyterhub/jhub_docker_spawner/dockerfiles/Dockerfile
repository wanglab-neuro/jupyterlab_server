FROM jupyterhub/jupyterhub:1.5.0

# APT packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    unzip \
    git \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Spawner, Authenticator and Idle culler
RUN pip install \
    dockerspawner==12.1.0 \
    # For generic OAuthenticator:
    oauthenticator \
    # MIT OIDC oauthenticator: 
    git+git://github.com/matted/mit-oidc-authenticator \ 
    # Native Authenticator 
    jupyterhub-nativeauthenticator==1.0.5 \
#    jupyterhub-kerberosauthenticator \
    jupyterhub-idle-culler

# Copy Jupyterhub's configuration script and files used for bootstrapping new user accounts
COPY jupyterhub_config.py bootstrap.sh HowTo.md ./
RUN chmod +754 bootstrap.sh HowTo.md
