Create image from repository 
jupyter-repo2docker
https://repo2docker.readthedocs.io/en/latest/usage.html
https://zero-to-jupyterhub.readthedocs.io/en/latest/repo2docker.html

Directly from the online repository 
jupyter-repo2docker \
    --no-run \
    --user-name=jovyan \
    --image=deeplabcut:r2d \
    <a-git-repository-url>

From local repo (modify local files if needed).   
jupyter-repo2docker \
    --no-run \
    --user-name=jovyan \
    --image=deeplabcut:r2d \
    $PWD
