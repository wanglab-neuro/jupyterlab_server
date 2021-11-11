# JupyterHub configuration
#
## If you update this file, do not forget to delete the `jupyterhub_data` volume before restarting the jupyterhub service:
##
##     docker volume rm jupyterhub_jupyterhub_data
##
## or, if you changed the COMPOSE_PROJECT_NAME to <name>:
##
##    docker volume rm <name>_jupyterhub_data
##

import os, sys, pwd, subprocess

## Authenticator
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'

c.Authenticator.admin_users = {'admin'}

def pre_spawn_hook(spawner):

    username = spawner.user.name

    try:

        pwd.getpwnam(username)

    except KeyError:

        subprocess.check_call(['useradd', '-ms', '/bin/bash', username])

c.Spawner.pre_spawn_hook = pre_spawn_hook


## Generic
#c.JupyterHub.admin_access = True #give admins permission to log in to the single user notebook servers owned by other users
c.Spawner.default_url = '/lab'

c.JupyterHub.ssl_key = '/etc/ssl/private/neuro-wang-15.mit.edu.key'
c.JupyterHub.ssl_cert = '/etc/ssl/certs/neuro-wang-15_mit_edu_cert.cer'

"""
## Authenticator

from oauthenticator.generic import GenericOAuthenticator

#c.Application.log_level = 'DEBUG'

c.JupyterHub.authenticator_class = GenericOAuthenticator
c.GenericOAuthenticator.client_id = os.environ['OAUTH2_CLIENT_ID']
c.GenericOAuthenticator.client_secret = os.environ['OAUTH2_CLIENT_SECRET']
c.GenericOAuthenticator.token_url = 'https://gymnasium-ditzingen.de/iserv/oauth/v2/token'
c.GenericOAuthenticator.userdata_url = os.environ['OAUTH2_USERDATA_URL']
c.GenericOAuthenticator.userdata_params = {'state': 'state'}
# the next can be a callable as well, e.g.: lambda t: t.get('complex').get('structure').get('username')
#c.GenericOAuthenticator.username_key = 'preferred_username'
c.GenericOAuthenticator.login_service = 'IServ'
c.GenericOAuthenticator.scope = ['openid', 'profile', 'email', 'groups']
c.GenericOAuthenticator.admin_groups = ['Admins', 'admins']
c.GenericOAuthenticator.oauth_callback_url = 'https://jupyter.gymnasium-ditzingen.de/hub/oauth_callback'
c.OAuthenticator.tls_verify = False
"""

## Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = os.environ['HUB_IP']

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan' 
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

# Other stuff
#c.Spawner.cpu_limit = 1
#c.Spawner.mem_limit = '10G'


## Services

c.JupyterHub.load_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "delete:servers",
            # "admin:users", # if using --cull-users
        ],
        # assignment of role's permissions to:
        "services": ["jupyterhub-idle-culler-service"],
    }
]
c.JupyterHub.services = [
    {
        "name": "jupyterhub-idle-culler-service",
        "command": [
            sys.executable,
            "-m", "jupyterhub_idle_culler",
            "--timeout=3600",
        ],
         "admin": True, # Has to be disabled version>2.0
    }
]

