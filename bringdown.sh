#!/bin/bash -v
docker-compose down
docker volume rm jupyterhub_jupyterhub_data
docker rmi jhub_ds
rm -rf /srv/jupyterhub/*

# docker rm -v jupyterhub
# docker network prune -f
