
#!/bin/sh

cd ../backups

# get Jupyterhub db
docker cp jupyterhub:/srv/jupyterhub/jupyterhub.sqlite jupyterhub-backup-$(date +%Y-%m-%d).sqlite
# move file to backup location
find . -name "jupyterhub-backup-*.sqlite" -exec mv '{}' /mnt/j/backups/jhub/ \;
