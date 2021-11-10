# jupyterlab_server
 jupyterlab served by jupyterhub 

**Build**
`docker-compose build`

**Start**
`docker-compose up -d`

## For Matlab enabled jupyterlab
Build Matlab image first:
`cd matlab_im`
`docker build -t matlab_om:2021b -f dockerfiles/Dockerfile context`



