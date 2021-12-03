### Use Jupyterlab

Intro video: https://www.youtube.com/watch?v=A5YyoCKxEOU  
  
Getting started: 
https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html  

### Add code from Github repository 

**Public repositories** 
1. Get the repository address. See [how to do that](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
3. Navigate to the directory where you want to put the code repository.
3. Click on the Git icon from the Left Sidebar
4. Select "Clone a repository"
5. Paste the repository address and click "Clone"

This can be done from the terminal following the same procedure as explained in the link above. 

**Private repositories** 
The procedure is explained here: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
It needs only to be done once. 
This works only for private repositories you have access to of course. 

1. Create a SSH Key. e.g.
 `ssh-keygen -t ed25519 -C "prevosto@mit.edu"`
2. Start the ssh agent	`eval "$(ssh-agent -s)"`  
3. Add Key to default location: `ssh-add ~/.ssh/id_ed25519`  
4. Add the public key to Github. e.g., copy output from `cat ~/.ssh/id_ed25519.pub` then go to the SSH Key section in your Github settings. (see https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).  
5. Finally, clone the private repo, with the same procedure as for public repositories, but using the SSH protected address (e.g., `git@github.com:wanglab-neuro/HighChannelCount-Ephys-Pipeline.git`). Or from the command line: `git clone git@github.com:wanglab-neuro/HighChannelCount-Ephys-Pipeline.git`

### Create a new environment and make it available to notebooks
 
### Use the Matlab server on the Openmind Cluster
