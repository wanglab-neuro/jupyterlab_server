# Jupterlab server with JupyterHub 
# v2: starts jupyterhub with modified config file.

# Dockerfile created by Vincent Prevosto based on this tutorial: https://hatarilabs.com/ih-en/how-to-set-a-multiuser-jupyterlab-server-with-jupyterhub-in-windows-with-docker


FROM jupyterhub/jupyterhub

# install nodejs, python3, jupyterhub and jupyterlab
RUN apt-get update -y && \
	apt-get install -y npm nodejs python3 python3-pip git nano sudo && \
	python3 -m pip install jupyterhub notebook jupyterlab && \
	npm install -g configurable-http-proxy

# install native authenticator package
RUN cd /home && \
	git clone https://github.com/jupyterhub/nativeauthenticator.git && \
	cd nativeauthenticator && \
	pip3 install -e .

# create and modify jupyterconfig
RUN mkdir /etc/jupyterhub && \
	cd /etc/jupyterhub && \ 
	jupyterhub --generate-config -f jupyterhub_config.py

RUN appendJhubConf=`echo "import pwd, subprocess\n\
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'\n\
c.Authenticator.admin_users = {'admin'}\n\
def pre_spawn_hook(spawner):\n\
   username = spawner.user.name\n\
   try:\n\
      pwd.getpwnam(username)\n\
   except KeyError:\n\
      subprocess.check_call(['useradd', '-ms', '/bin/bash', username])\n\
c.Spawner.pre_spawn_hook = pre_spawn_hook\n\
c.Spawner.default_url = '/lab'"; cat /etc/jupyterhub/jupyterhub_config.py` && \
	echo "$appendJhubConf" > /etc/jupyterhub/jupyterhub_config.py

CMD ["jupyterhub","-f","/etc/jupyterhub/jupyterhub_config.py"]