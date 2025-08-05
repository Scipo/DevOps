#!/bin/bash

# worker_setup.sh
# This script makes a worker node join the Docker Swarm cluster

MASTER_IP=$1

echo " ----- Attemting to join Docker Swarm on worker  ----- "

# Wait for manager to create the join token and command file.
# The /vagrant directory is sync with the host machine, so master will create file here
ATTEMPTS=0
MAX_ATTEMPTS=60 # Wait up to 5 min (60 * 5 sec)
while [ ! -f "/vagrant/worker_join_command.sh" ] && [ $ATTEMPTS -lt $MAX_ATTEMPTS ]; do
    echo "Waiting for master to provide worker_join_command.sh.... (Attempt: $((ATTEMPTS+1))/${MAX_ATTEMPTS})"
    sleep 10 # wait 10 sec before retry
    ATTEMPTS=$((ATTEMPTS+1))
done

if [ ! -f "/vagrant/worker_join_command.sh" ]; then
    echo "ERROR: worker_join_command.sh not found after multiple tries. NOT POSSIBLE to join Docker Swarm"
    exit 1
fi

# Check if the file is executable
chmod +x /vagrant/worker_join_command.sh

# Execute the join command
sudo /vagrant/worker_join_command.sh

echo " ----- Worker node joinded the Docker Swarm ------" 


