# Argo CD GitLab Bridge

This repository provides a method to sync private GitLab repositories in a specific GitLab group with an Argo CD instance.

When deployed, this repo builds an image using Python s2i, and sets up a CronJob which scans GitLab periodically. When it detects a new repository, it adds an Application instance to Argo CD, as well as configures Argo to use a certain SSH secret to pull that repository.

It is deployable using Helm 3, and all options can be seen in the chart's [values file](.helm/values.yaml).

## Typical Deployment

```sh
cd .helm
helm install my-bridge . \
--set "gitLab.apiUrl=https://gitlab.your-domain.com" \
--set "gitLab.personalAccessToken=1234567890" \
--set "gitLab.parentRepositoryID=1234" \
--set "resourcePrefix=autodetected-repo" \
--set "chartPath=where/helm/charts/live/in/new/repos" \
--set "sshSecretName=my-private-key-secret-name" \
--set "destinationNamespace=charts-get-deployed-here"
```
