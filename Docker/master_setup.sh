#!/bin/bash

echo "--- Initializing Docker Swarm on manager ---"

# Check if swarm is already initialized
if ! sudo docker info | grep -q "Swarm: active"; then
  # Initialize Docker Swarm
  # Use --advertise-addr to ensure other nodes can connect
  sudo docker swarm init --advertise-addr 192.168.100.201
  echo "Docker Swarm initialized."
else
  echo "Docker Swarm already initialized."
fi

# Join token for worker nodes
sudo docker swarm join-token worker -q > /vagrant/worker_join_token.txt

# Get the full join command for worker nodes
sudo docker swarm join-token worker | grep "docker swarm join" > /vagrant/worker_join_command.sh

# Make the join command script executable
chmod +x /vagrant/worker_join_command.sh

echo "--- Swarm manager setup complete. Join token and command saved to /vagrant/ ---"

# Deploy the application using docker-compose.yml
echo "--- Deploying application services on the Swarm manager ---"

# Ensure the docker-compose.yml file is present in the /vagrant directory.
if [ -f "/vagrant/docker-compose.yml" ]; then
  # Build and deploy the services
  # --with-registry-auth is needed if using private registries
  sudo docker stack deploy -c /vagrant/docker-compose.yml bgapp
  echo "Application services deployed'."
else
  echo "Error: docker-compose.yml not found at /vagrant/docker-compose.yml. Skipping application deployment."
fi

echo "--- Swarm application deployment initiated ---"
