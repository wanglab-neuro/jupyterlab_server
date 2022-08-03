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
import docker


############################# Authentication ########################
######################### Choose one of the options below ############

### Native authentication ###
### user create login / password, admin authorizes

# c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
# c.Authenticator.admin_users = {'admin'}

### Dummy authentication ###
### Use dummy for testing purposes
# c.JupyterHub.authenticator_class = "dummy"
# c.Authenticator.admin_users = { 'test' }
# c.DummyAuthenticator.password = "testpass"
## Also available (Hub 2.0): c.JupyterHub.authenticator_class = 'null'

### GitHub OAuth authentication
from oauthenticator.github import GitHubOAuthenticator
c.JupyterHub.authenticator_class = GitHubOAuthenticator
c.GitHubOAuthenticator.oauth_callback_url = os.environ['GITHUB_CLIENT_ID']
c.GitHubOAuthenticator.oauth_callback_url = os.environ['GITHUB_CLIENT_SECRET']
c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
# c.GitHubOAuthenticator.allowed_organizations = os.environ['GITHUB_ORG']

### OAuth 2.0 authentication with OAuth2/OpenID ###
### Use this service if you have access to an OIDC server (e.g., https://oidc.mit.edu/)

# from oauthenticator.generic import GenericOAuthenticator

# # c.Application.log_level = 'DEBUG'

# c.JupyterHub.authenticator_class = GenericOAuthenticator
# c.GenericOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
# c.GenericOAuthenticator.client_id = os.environ['OAUTH_CLIENT_ID']
# c.GenericOAuthenticator.client_secret = os.environ['OAUTH_CLIENT_SECRET']

# c.GenericOAuthenticator.authorize_url = os.environ['OAUTH2_AUTHORIZE_URL']
# c.GenericOAuthenticator.token_url = os.environ['OAUTH2_TOKEN_URL']

# c.GenericOAuthenticator.userdata_url = os.environ['OAUTH2_USERDATA_URL']
# c.GenericOAuthenticator.userdata_method = 'GET'
# c.GenericOAuthenticator.userdata_params = {"state": "state"}

# c.LocalAuthenticator.create_system_users = True
# c.GenericOAuthenticator.username_key = 'preferred_username'

# #c.GenericOAuthenticator.scope = ['openid', 'profile', 'email', 'groups']
# #c.GenericOAuthenticator.admin_groups = ['Admins', 'admins']
# #c.OAuthenticator.tls_verify = False

# #Set user role and whitelist
# #c.Authenticator.admin_users = {'mal', 'zoe'}
# #c.Authenticator.allowed_users = {'mal', 'zoe', 'inara', 'kaylee'}

############################# Generic ########################
## Admin access: give admins permission to log in to the single user notebook servers owned by other users
c.JupyterHub.admin_access = True 

## Docker spawner default URL 
c.Spawner.default_url = '/lab'
# c.Spawner.cmd=["jupyter-labhub"]

############################# Permissions ########################
# Updating permissions for volumes mounted from host
# See comment from Min RK in this thread:
# https://github.com/jupyterhub/dockerspawner/issues/160#issuecomment-330162308
# And fix below from here: https://discourse.jupyter.org/t/dockerspawner-and-volumes-from-host/7008/6
c.DockerSpawner.extra_create_kwargs = {'user': 'root'}
c.DockerSpawner.environment = {
    "CHOWN_HOME": "yes",
    "CHOWN_EXTRA": "/home/jovyan",
    "CHOWN_HOME_OPTS": "-R",
    "NB_UID": 1000,
    "NB_GID": 1000,
}

############################# Pre-spawn Hook ########################
#  Adding a HowTo file and tutorials before spawning the container   
def pre_spawn_hook(spawner):
    username = spawner.user.name
    script = os.path.join(os.path.dirname(__file__), 'bootstrap.sh')
    howto_mdfile = os.path.join(os.path.dirname(__file__), 'HowTo.md')
    with open(howto_mdfile, 'r', newline='') as rf:
        howto_contents = rf.read()
    getdata_mdfile = os.path.join(os.path.dirname(__file__), 'GetYourData.md')
    with open(getdata_mdfile, 'r', newline='') as rf:
        getdata_contents = rf.read()
    subprocess.check_call([script, username, howto_contents, getdata_contents])

c.Spawner.pre_spawn_hook = pre_spawn_hook

#c.DockerSpawner.post_start_cmd = 'sh -c "ln -s /media/caiman_data /home/jovyan/work"'
c.DockerSpawner.post_start_cmd = 'bash -c "/media/link_package_files.sh"'

############################# Docker Spawner Configuration ########################
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = os.environ['HUB_IP']

# Pick a docker image. 
# c.DockerSpawner.allowed_images (DockerSpawner version 12.0+)

c.JupyterHub.allow_named_servers=True

# get image name without tag -> not working 

#imagename = list(imagename.values())[0]
#imagename = 'wanglabneuro/jlab_base:multilanguage'
# imagename_notag = imagename.partition(':')
# imagename_notag = ('wanglabneuro/jlab_base', ':', 'multilanguage')
# imagename_notag = imagename_notag[0]

c.DockerSpawner.name_template = "{prefix}-{username}--{servername}" #{imagename} bugs with image tags :/
c.DockerSpawner.allowed_images = {
    'SpikeInterface' : 'wanglabneuro/spikeinterface-jupyterlab',
    'CaImAn':'wanglabneuro/jlab_caiman',
    'MIN1PIPE' : 'wanglabneuro/jlab_min1pipe',
    'Data science':'jupyter/datascience-notebook',
    'Multi language':'wanglabneuro/jlab_base:multilanguage',
    'Matlab':'wanglabneuro/jlab_matlab:2021b'
    }

    # 'Brain Render':'wanglabneuro/brainrender-wanglab',
    # 'DeepLabCut':'wanglabneuro/jlab_dlc',
    # 'Whisker Tracker':'paulmthompson/whiskertracker',
    # 'Tensorflow':'wanglabneuro/jlab_tf'
# DockerSpawner.image_whitelist is deprecated in DockerSpawner 12.0, use DockerSpawner.allowed_images instead

## access GPU
c.DockerSpawner.extra_host_config = {
    "device_requests": [
        docker.types.DeviceRequest(
            count=-1,
            capabilities=[["gpu"]],
        ),
    ],
}

## Remove containers once they are stopped
c.DockerSpawner.remove = True
# DockerSpawner.remove_containers is deprecated in DockerSpawner 0.10.0, use DockerSpawner.remove instead

# User data persistence
home_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
notebook_dir = home_dir # this is the root directory for the Jupyterlab sidebar
data_dir = home_dir + '/data'
c.DockerSpawner.notebook_dir = notebook_dir #home_dir
# c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }
c.DockerSpawner.volumes = {
        # 'jhub-user-{username}': home_dir,
        # '/home/{username}': home_dir,
        # '/srv/jupyterhub/{username}/work': notebook_dir, #home_dir + '/work',   
        # '/volumes/jupyterhub/{username}': notebook_dir,
        # '/home/wanglab/my-nese-data': notebook_dir + '/data/NESE'
        '/srv/jupyterhub/{username}': home_dir,
        # '/data/d': {"bind": data_dir + '/WindowsData', "mode": "rw"},
        '/data/d': {"bind": '/data', "mode": "rw"},
        '/data/shared': home_dir + '/shared'
        }

# home_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
# notebook_dir = home_dir
# data_dir = notebook_dir + '/data'
# c.DockerSpawner.notebook_dir = notebook_dir 
# c.DockerSpawner.volumes = {
#         '/srv/jupyterhub/{username}': home_dir,
#         '/data/d': {"bind": '/data', "mode": "ro"},
#         '/data/shared': data_dir + '/shared'
#         }

# Resource limits
#c.Spawner.cpu_limit = 1
#c.Spawner.mem_limit = '10G'


############################# Services ########################
 
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

