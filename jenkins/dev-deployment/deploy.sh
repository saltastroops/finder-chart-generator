#!/bin/bash

# Pull the latest docker image and restart the service defined in the docker compose
# file.

cd finder-chart-generator

# Log into the docker registry
cat registry-password.txt | docker login --password-stdin -u ${DOCKER_REGISTRY_USERNAME} ${DOCKER_REGISTRY}

# Pull the docker image for the service, but don't restart the service
docker compose pull fcg

# Log out from the Docker registry again
docker logout ${DOCKER_REGISTRY}

# Restart the service
docker compose down || true
docker compose up -d

# Clean up
docker image prune
