
#!/bin/sh

# Manual backup script. User file folders can be pretty heavy so it is not recommended to run it as a CRON job. 

cd ../backups

# backup shared folders (move archive)
tar czvf jhub_shared.tar.gz /data/shared/*
mv -f jhub_shared.tar.gz /mnt/j/backups/jhub/jhub_shared.tar.gz

# backup user directories (move archive)
tar czvf jhub_userfiles.tar.gz /srv/jupyterhub/*
mv -f jhub_userfiles.tar.gz /mnt/j/backups/jhub/jhub_userfiles.tar.gz

# backup Jupyterhub db (leave a copy)
docker cp jupyterhub:/srv/jupyterhub/jupyterhub.sqlite jupyterhub-backup-$(date +%Y-%m-%d).sqlite
find . -name "jupyterhub-backup-*.sqlite" -exec cp '{}' /mnt/j/backups/jhub/ \;

touch backup_success