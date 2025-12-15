FROM jupyterhub/jupyterhub:4.1.5

# APT packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    build-essential \
    # libssl-dev \
    # libffi-dev \
    # python3-dev \
    # libkrb5-dev krb5-kdc krb5-admin-server krb5-config \
    unzip \
    git \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Spawner, Authenticator and Idle culler
RUN python3 -m pip install --upgrade pip
RUN pip install \
    dockerspawner==13.0.0 \
    # For generic OAuthenticator:
    oauthenticator \
    # Native Authenticator 
    jupyterhub-nativeauthenticator==1.2.0 \
    # Idle culler
    jupyterhub-idle-culler

# Copy Jupyterhub's configuration script and files used for bootstrapping new user accounts
COPY jupyterhub/context/jupyterhub_bam_config.py.template ./jupyterhub_config.py
COPY jupyterhub/context/bootstrap.sh.template ./bootstrap.sh
COPY jupyterhub/context/HowTo.md ./HowTo.md
COPY jupyterhub/context/GetYourData.md ./GetYourData.md
COPY jupyterhub/context/thebe_service.py ./thebe_service.py
COPY jupyterhub/context/templates ./templates
COPY jupyterhub/context/content /usr/local/share/jupyterhub/static/custom/
RUN chmod +754 bootstrap.sh HowTo.md GetYourData.md
