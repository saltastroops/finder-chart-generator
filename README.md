# finder-chart-generator

Website for generating SALT finder charts

## Deploying to a dev server

Before you can run the pipeline script, a few requirements must be fulfilled:

* The [SAAO Shared Library](https://github.com/saltastroops/saao-shared-jenkins-library) must be installed. See its documentation for instructions.
* An environment variable `REGISTRY_URL` must be configured. Its value must be the URL of the container registry for hosting the Docker images. An example value would be `https://registry.example.com`.
* Credentials of the type "Username and password" must be defined with the username and password for the container registry.
* Credentials of the type "SSH username with private key". The username must be that for the deployment server, and the key must be the private key of the Jenkins user. The Jenkins server must be included in the `authorized_hosts` file of the user on the deployment server.
* The [SSH Pipeline Steps](https://plugins.jenkins.io/ssh-steps/) plugin must be installed.
