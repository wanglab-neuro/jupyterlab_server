FROM jupyter/scipy-notebook 

# switch to root to be able to create directories 
USER root

# Install Matlab
RUN mkdir /tmp/matlab
COPY matlab/R2021b /tmp/matlab/R2021b
RUN cd /tmp/matlab/R2021b && \
    ./install -inputFile installer_input_jh.txt
RUN rm -rf /tmp/matlab/R2021b

# Add Openmind configuration scripts (makes it available for copy to `userpath` at a later stage)
RUN mkdir /usr/local/MATLAB/R2021b/openmind 
ADD /openmind/mit.nonshared.R2021b.tar.gz /usr/local/MATLAB/R2021b/openmind/ 
