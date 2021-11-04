import pwd, subprocess

c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'

c.Authenticator.admin_users = {'admin'}

def pre_spawn_hook(spawner):

    username = spawner.user.name

    try:

        pwd.getpwnam(username)

    except KeyError:

        subprocess.check_call(['useradd', '-ms', '/bin/bash', username])

c.Spawner.pre_spawn_hook = pre_spawn_hook

c.Spawner.default_url = '/lab'

c.JupyterHub.ssl_key = '/etc/ssl/private/neuro-wang-15.mit.edu.key'
c.JupyterHub.ssl_cert = '/etc/ssl/certs/neuro-wang-15_mit_edu_cert.cer'

"""
# Untested / may not be needed
c.JupyterHub.services = [
    {
        'name': 'cull_idle',
        'admin': True,
        'command': 'python /srv/jupyterhub/cull_idle_servers.py --timeout=3600'.split(),
    },
]
"""
