# Argo CD GitLab Bridge

This repository provides a method to sync private GitLab repositories in a specific GitLab group with an Argo CD instance. It builds this repo using Python s2i, and sets up a CronJob which scans GitLab periodically. When it detects a new repository, it adds an Application instance to Argo CD, as well as configures Argo to use a certain SSH secret to pull that repository.

It is deployable using Helm 3.

## Example Deployment

```sh
cd .helm
helm install my-bridge . \
--set "gitLab.apiUrl=https://gitlab.your-domain.com" \
--set "gitLab.personalAccessToken=1234567890" \
--set "gitLab.parentRepositoryID=1234" \
--set "resourcePrefix=autodetected-repo" \
--set "chartPath=where/helm/charts/live" \
--set "sshSecretName=my-secret" \
--set "destinationNamespace=charts-get-deployed-here"
```
