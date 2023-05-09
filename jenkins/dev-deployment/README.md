# Deployment to a server

You can deploy the Finder Chart Generator to a server by means of the Jenkinsfile `jenkins/deployment/Jenkinsfile`.

## Parameters

The Jenkinsfile is using several parameters. When configuring a pipeline with this file, tick the "This project is parameterized" checkbox and add all the required parameters with the correct default values. If the pipeline is run as an SCM pipeline, the default values will be used; so they should be the correct values for the deployment.

The following parameters are used by the script.

| Parameter name            | Type                                        | Explanation                                                                                                                                                                                                                             | Example value                |
|---------------------------|---------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|
| dockerRegistryCredentials | Credentials (username with password)        | Username and password for the container registry hosting the Docker image                                                                                                                                                               |                              |
| dockerRegistryUrl         | String                                      | URL of the container registry for hosting the Docker image                                                                                                                                                                              | https://registry.example.com |
| host                      | String                                      | Hostname of the server on which to deploy                                                                                                                                                                                               | dev.example.com              |
| sshCredentials            | Credentials (SSH username with private key) | Username and private SSH key for connecting to the host. The username must be that of a user on the host, the SSH key must be that of the Jenkins user. The corresponding public key must be in the `authorized_keys` file on the host. |                              |
