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
import shutil

## Authenticator
# c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
c.Authenticator.admin_users = {'foo'}
# Use dummy for testing purposes
c.JupyterHub.authenticator_class = "dummy"
# c.Authenticator.admin_users = { 'test' }
c.DummyAuthenticator.password = "testpass"
## Generic
#c.JupyterHub.admin_access = True #give admins permission to log in to the single user notebook servers owned by other users
c.Spawner.default_url = '/lab'

c.DockerSpawner.extra_create_kwargs = {'user': 'root'}
c.DockerSpawner.environment = {
    "CHOWN_HOME": "yes",
    "CHOWN_EXTRA": "/home/jovyan",
    "CHOWN_HOME_OPTS": "-R",
    "NB_UID": 1000,
    "NB_GID": 1000,
}

# def create_dir_hook(spawner):
#     username = spawner.user.name # get the username
#     volume_path = os.path.join('/volumes/jupyterhub/', username) #path on the jupytherhub host, create a folder based on username if not exists
#     if not os.path.exists(volume_path):
#         os.mkdir(volume_path)
#         shutil.chown(volume_path, user=username, group='users')

# c.Spawner.pre_spawn_hook = create_dir_hook

def pre_spawn_hook(spawner):
    username = spawner.user.name
    # try:
    #     pwd.getpwnam(username)
    # except KeyError:
    #     print("Creating user") 
    #     subprocess.check_call(['useradd', '-ms', '/bin/bash', username])
        # subprocess.check_call(['usermod', '-aG', '/bin/bash', 'jhub_users'])  
    # volume_path = os.path.join('/home/', username) #path on the jupytherhub host, create a folder based on username if not exists
    # if not os.path.exists(volume_path):
    #     os.mkdir(volume_path)
    #     shutil.chown(volume_path, user=username, group='jhub_users')
    script = os.path.join(os.path.dirname(__file__), 'bootstrap.sh')
    subprocess.check_call([script, username])

# def pre_spawn_hook(spawner):
#     username = spawner.user.name # get the username
#     volume_path = os.path.join('/volumes/jupyterhub', username)
#     if not os.path.exists(volume_path):
#         # create a directory with umask 0765
#         # hub and container user must have the same UID to be writeable
#         # still readable by other users on the system
#         os.mkdir(volume_path, 0o765)
#         # now do whatever you think your user needs
#         # ...
#         pass

c.Spawner.pre_spawn_hook = pre_spawn_hook

## Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = os.environ['HUB_IP']

## Remove containers once they are stopped
c.DockerSpawner.remove_containers = True


# user data persistence
home_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
notebook_dir = home_dir + '/work'
c.DockerSpawner.notebook_dir = notebook_dir #home_dir
# c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }
c.DockerSpawner.volumes = {
        'jhub-user-{username}': home_dir,
#         # '/home/{username}': home_dir,
        '/volumes/jupyterhub/{username}/work': notebook_dir, #home_dir + '/work',   
#         '/volumes/jupyterhub/{username}': notebook_dir,
        '/home/wanglab/data/d': {"bind": '/data', "mode": "ro"},
        '/data/shared': notebook_dir + '/shared'
        }


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

