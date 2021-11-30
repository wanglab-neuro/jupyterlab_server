### Build Matlab image
cd matlab_im
docker build -t matlab_om:2021b -f dockerfiles/Dockerfile context # matlab_om is the Matlab installation with Openmind configuration scripts

### Build image:
cd jupyterhub/jhub_matlab
docker build -t jhub_matlab:latest -f dockerfiles/Dockerfile context

**optional: make soft link in WSL to data directory on Windows:**
e.g., `ln -s /mnt/d/ ~/data/`
(to remove link: `cd data` then `unlink d`)
	Important note: it is recommended to store source code and other data that is bind-mounted into Linux containers (i.e., with docker run -v <host-path>:<container-path>) in the Linux file system, rather than the Windows file system. See: https://docs.docker.com/desktop/windows/wsl/#best-practices

### Start container - with a few volumes 
docker run \
-d \
--restart unless-stopped \
--name jhub_matlab \
-v /etc/ssl/:/etc/ssl/ \
-v ~/data/d:/data \
-v ~/data/shared_files:/srv/shared_files \
-v ~/data/shared_code:/srv/shared_code \
-p 8000:8000 \
jhub_matlab:latest

### Data access:
* The shared folder will be added automatically to all new users.
* Admin can add user to group
e.g. (in container bash):
	sudo usermod -a -G jhub_users vincent
* Admin can add user data to its home directory 
e.g. (in container bash):
	mkdir /home/vincent/data
	ln -s /data/Vincent/* /home/vincent/data  
	 
### Access container:
docker exec -it jhub_matlab bash

### Connect to server: 
https://neuro-wang-15.mit.edu:8000/hub/login

