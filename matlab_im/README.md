This is the matlab image that will be used to build the jupyterhub container with Matlab installed on it. 
These are two separate repos, for clarity, and because this image is super heavy and we don't need that context passed to the jupyterhub image.

On a related note: the Matlab ISO is needed for Matlab to be installed silently in Linux. 
Installation files available on the server in /Resources/matlab
See installer (installer_input_jh.txt) in `/matlab/R2021b/`
The Dockerfile will use it to install Matlab: 
	# Install Matlab
	```
	RUN mkdir /tmp/matlab
	COPY matlab/R2021b /tmp/matlab/R2021b
	RUN cd /tmp/matlab/R2021b && \
	    ./install -inputFile installer_input_jh.txt
	```

Note that Acquisition Toolbox, Spreadsheet Link are not available and need to be commented in the installer file

The image also contains configuration files for Openmind (see https://github.mit.edu/MGHPCC/OpenMind/wiki/Software:-Remote-MATLAB-Job-Submission)

### Build the image:
`docker build -t matlab_om:2021b -f dockerfiles/Dockerfile context`

### Test installation
`docker run -d --rm --name matlab_om matlab_om:2021b`
`docker exec -it matlab_om bash`
call Matlab with `/usr/local/MATLAB/R2021b/bin/matlab`

