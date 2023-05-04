# Deployment to a development server

Running the Jenkinsfile requires ssh credentials, a secret file, and some environment variables.

## Jenkins credentials

You need to define the following credentials under Dashboard > Manage Jenkins > Manage Credentials.

| Secret ID                   | Type                          | Explanation                                                               |
|-----------------------------|-------------------------------|---------------------------------------------------------------------------|
| docker-registry-credentials | Username with password        | Username and password for the container registry hosting the Docker image |
| fcg-dev-server-credentials  | SSH username with private key | Username and private SSH key for the development server                   |

## Environment variables

The following environment variables need to be defined. You can set them under Dashboard > Manage Jenkins > Configure System in the section "Global properties".

| Variable        | Description                                                | Example                      |
|-----------------|------------------------------------------------------------|------------------------------|
| DOCKER_REGISTRY | URL of the container registry for hosting the Docker image | https://registry.example.com |
| FCG_DEV_HOST    | Hostname of the Finder Chart Generator development server  | dev.example.com              |


