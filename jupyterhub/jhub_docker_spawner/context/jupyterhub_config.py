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

## Authenticator
# c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
# c.Authenticator.admin_users = {'admin'}
# Use dummy for testing purposes
c.JupyterHub.authenticator_class = "dummy"
c.Authenticator.admin_users = { 'test' }
c.DummyAuthenticator.password = "testpass"

## Generic
# c.JupyterHub.admin_access = True #give admins permission to log in to the single user notebook servers owned by other users

## Docker spawner
c.Spawner.default_url = '/lab'

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

#  Adding a HowTo file and tutorials before spawning the container   
def pre_spawn_hook(spawner):
    username = spawner.user.name
    script = os.path.join(os.path.dirname(__file__), 'bootstrap.sh')
    howto_file = os.path.join(os.path.dirname(__file__), 'HowTo.md')
    with open(howto_file, 'r', newline='') as rf:
        contents = rf.read()
    subprocess.check_call([script, username, contents])

c.Spawner.pre_spawn_hook = pre_spawn_hook

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = os.environ['HUB_IP']

# Pick a docker image. 
# c.DockerSpawner.allowed_images (DockerSpawner version 12.0+)

c.JupyterHub.allow_named_servers=True
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.name_template = '{prefix}-{username}-{imagename}' #{servername}
c.DockerSpawner.image_whitelist = {
    'Data science':'jupyter/datascience-notebook',
    'Multi language':'wanglabneuro/jlab_base',
    'Matlab':'wanglabneuro/jlab_matlab',
    'DeepLabCut':'wanglabneuro/jlab_dlc',
    'CaImAn':'wanglabneuro/jlab_caiman',
    'Brain Render':'wanglabneuro/brainrender-wanglab',
    'Whisker Tracker':'paulmthompson/whiskertracker',
    'Tensorflow':'wanglabneuro/jlab_tf'}

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
c.DockerSpawner.remove_containers = True

# User data persistence
home_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
notebook_dir = home_dir + '/work'
c.DockerSpawner.notebook_dir = notebook_dir #home_dir
# c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }
c.DockerSpawner.volumes = {
        'jhub-user-{username}': home_dir,
#         # '/home/{username}': home_dir,
        '/srv/jupyterhub/{username}/work': notebook_dir, #home_dir + '/work',   
#         '/volumes/jupyterhub/{username}': notebook_dir,
        '/home/wanglab/data/d': {"bind": '/data', "mode": "ro"},
        '/data/shared': notebook_dir + '/shared'
        }


# Resource limits
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

