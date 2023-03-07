FROM jupyterhub/jupyterhub:3.1.1

# APT packages
RUN apt update && \
    apt install -y --no-install-recommends \
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
    dockerspawner==12.1.0 \
    # For generic OAuthenticator:
    oauthenticator \
    # Native Authenticator 
    jupyterhub-nativeauthenticator \
    # Idle culler
    jupyterhub-idle-culler

# Copy Jupyterhub's configuration script and files used for bootstrapping new user accounts
COPY jupyterhub_config.py bootstrap.sh HowTo.md GetYourData.md ./
RUN chmod +754 bootstrap.sh HowTo.md GetYourData.md
