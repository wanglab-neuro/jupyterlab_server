## jupyterlab_server  
single-user jupyterlab served by jupyterhub 

**Start**  
`docker-compose up -d`

**For Matlab enabled jupyterlab**  
Build Matlab image first:  
```
cd matlab_im
docker build -t matlab_om:2021b -f dockerfiles/Dockerfile context
```  
See README file in `matlab_im` directory


