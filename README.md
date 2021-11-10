# jupyterlab_server
 jupyterlab served by jupyterhub 

**Build**  
`docker-compose build`

**Start**  
`docker-compose up -d`

## To use Matlab notebooks in jupyterlab  
Build Matlab image first:  
`cd matlab_im`  
`docker build -t matlab_om:2021b -f dockerfiles/Dockerfile context`



