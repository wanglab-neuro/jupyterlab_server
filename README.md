## jupyterlab server
This [Jupyterlab](https://jupyterlab.readthedocs.io/en/latest/) server is designed to run on local data analysis computers, using Docker containers and [Jupyterhub](https://jupyterhub.readthedocs.io/en/stable/).
It is OS independent (using WSL2 for Windows machines).

**Main features**
- allows concurrent access to data analysis computers (i.e., unlike Windows Remote Desktop Connection) 
- simplifies access and use of local computing resources, without having to know anything about setting up data analysis environments.  
- enables sharing code and tutorials for easier training, and reuse of code developed by others.
- provides a simple deployment with limited maintenance, that requires little sys admin knowledge.

**Configuration**
1. Install Docker (https://www.docker.com/get-started)
For Windows and MacOS machine, use Docker Desktop.  
*Additional instruction for Windows:*  
    - Set up WSL if it's not installed already  
https://docs.microsoft.com/en-us/windows/wsl/setup/environment. 
    - [optional but advisable] Move WSL and Docker to a dedicated disk. Exemple below to move them to the "J" disk.  
    -- WSL --   
      * Open PowerShell  
      * List installed distributions `wsl -l` 
      * Create target directory and move there  
      `cd J:\` `mkdir WSL` `cd WSL` `mkdir Ubuntu2004` `cd Ubuntu2004`  
      * Shutdown WSL `wsl --shutdown`  
      * Export default distro, e.g. `wsl --export Ubuntu-20.04 Ubuntu-20.04-LTS.tar`  
      * Unregister it `wsl --unregister Ubuntu-20.04`  
      * Import WSL in the current directory `wsl --import Ubuntu-20.04 J:\Docker\ .\Ubuntu-20.04-LTS.tar`  
      * Make it the default user distro `wsl -s Ubuntu-20.04`  
      * Check that import worked `wsl -l`
      
      -- Same procedure for Docker --
      ```
      cd J:\
      mkdir Docker
      cd Docker
      wsl --shutdown
      wsl --export docker-desktop-data docker-desktop-data.tar
      wsl --unregister docker-desktop-data
      wsl --import docker-desktop-data J:\Docker\ docker-desktop-data.tar --version 2
      ```
    - In Docker settings, enable the WSL2 based engine. Run Docker commands from WSL terminal (e.g., Start Menu > Ubuntu).  

2. Clone or download this repository  
For best performance on Windows machines, do that in WSL, not a Windows directory. 

3. Create a shared folder on the host computer (for Windows machine, on WSL).   
Create group and make this folder writable for anyone in that group.
	```
	mkdir -p /data/shared
	sudo groupadd jhub_users
	sudo chown root:jhub_users /data/shared
	sudo chmod g+s /data/shared
	sudo setfacl -d -m g::rwx /data/shared/
	```

4. Adjust Jupyterhub settings  
Open `jupyterhub_config.py` (found in folder `jupyterhub\jhub_docker_spawner\context`) 
Modify the volumes in `c.DockerSpawner.volumes`
	* `/home/wanglab/data/d` is the where the user data are located on the local computer. For example, if data are on the D drive, write `/mnt/d/`.  
	The target can also be a symlink made to the location. e.g., as follow:
	`ln -s /home/wanglab/data/d /mnt/d`   
	* `/data/shared` is the shared directory created on step 3. 

5. [optional but recommended] Request an SSL certificate to serve the notebooks over a secure HTTPS connection  
See request instructions for MIT [here](http://kb.mit.edu/confluence/x/x487).  
Once you get the certificate, place it with the key in a `secret` folder at the root of the repository.  
Once the SSL Connection is enable, the unsecure address will not work. E.g., 
http://lab-jhub-serv:8000/hub/login should now be:   
https://lab-jhub-serv.mit.edu:8000/hub/login  
In the default configuration (using the proxy), the server is accessible without specifying the port: https://lab-jhub-serv.mit.edu/hub/.  

6. Add content (e.g., for new user on-boarding)  
Three places to add user content:  
* `HowTo.md` file in `jhub_docker_spawner > context`. This file will be added to the user startup directory (`home/$USER/work`) by the bootstrap script.  
* The bootstrap script (also in `jhub_docker_spawner > context`) will create a `tutorials` directory and add a few helpful resources for data analysis, as well as a `Resources.md` file. Modify the section below `echo "Initial content loading for user"` to change the tutorials content. This content will only be generated once, the first time a new user logs in (which makes that first connection longer).  
* The shared directory. All files there will be available and modifiable by all users. A good place to start is to add the test notebooks from the notebooks folder.   


**Start the server**  
`docker-compose up -d`

**For Matlab enabled jupyterlab**  
Build Matlab image first:  
```
cd matlab_im
docker build -t matlab_om:2021b -f dockerfiles/Dockerfile context
```  
See README file in `matlab_im` directory


