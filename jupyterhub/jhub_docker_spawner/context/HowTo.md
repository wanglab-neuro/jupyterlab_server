### Use Jupyterlab

Intro video: https://www.youtube.com/watch?v=A5YyoCKxEOU  
  
Getting started: 
https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html  

### Connect to your data directory on the server 
Create a directory with your data as follow
1. Open a terminal 
2. Connect through sftp: 
`sftp username@server-node.mit.edu:/path/to/wanglab/data/directory/USERFOLDER ~/my-nese-data`
3. Download your data:   
   For a file `get mydatafile`  
   For a folder `get -r mydatafolder`  
 See [Essential sftp commands](https://docs.oracle.com/cd/E26502_01/html/E29001/remotehowtoaccess-14.html)

To avoid having to enter your password every time, copy a SSH key to the server
1. Create a SSH key if none exists. e.g.
    `ssh-keygen -t ed25519 -C "username@mit.edu"`
2. Copy key to the server  
    `ssh-copy-id username@server-node.mit.edu`

### Add code from Github repository 

**Public repositories**  
1. Get the repository address. ([how to do that ?](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository))
3. Navigate to the directory where you want to put the code repository.
3. Click on the Git icon from the Left Sidebar
4. Select "Clone a repository"
5. Paste the repository address and click "Clone"

This can be done from the terminal following the same procedure as explained in the link above. 

**Private repositories**  
This works only for private repositories you have access to, of course. You need to add a SSH key as follow:  
1. Create a SSH Key. e.g.
 `ssh-keygen -t ed25519 -C "username@mit.edu"`
2. Start the ssh agent	`eval "$(ssh-agent -s)"`  
4. Add the public key to Github. e.g., copy output from `cat ~/.ssh/id_ed25519.pub` then go to the SSH Key section in your Github settings. (see https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).  
5. Finally, clone the private repo, with the same procedure as for public repositories, but using the SSH protected address (e.g., `git@github.com:wanglab-neuro/HighChannelCount-Ephys-Pipeline.git`). 
Do the first one from the command line to add Github's key fingerprint to the list of known hosts. e.g.: `git clone git@github.com:wanglab-neuro/HighChannelCount-Ephys-Pipeline.git`
6. Thereafter, you can use the Git icon shortcut on the left sidebar.

See also the documentation [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh). 

### Start the Matlab GUI
1. Click the Matlab icon (if available in that environment)
2. Log in with personal or network license (MIT Matlab 2021b license: 
https://downloads.mit.edu/released/matlab/R2021b/short-license-file.txt)
Enter license info with this formatting: 01234@server-address


<!--### Create a new environment and make it available to notebooks -->
 
<!--### Use the Matlab server on the Openmind Cluster -->
