# Deployment

This is fundamentally just a Python project that versions dependencies in `Pipenv` & `Pipenv.lock` files. Any system that can run projects using Pipenv should be able to run this application. If you are running this application standalone, you will need to set the environment variable `CONFIG_FILE` to the path of the config file to use. That said, there is a Helm chart available to get up and running quickly on OpenShift.

The Helm chart is available in `/helm` and has a few input parameters:

| Parameter | Description | Default |
|---|---|---|
| `setupConfigMap` | Create a ConfigMap which contains a workflow definition file. Requires `configFileContents` to also be set. | `false` |
| `configFileContents` | The contents of the config file for `setupConfigMap` to create. | `""` |
| `configMapName` | The pre-existing ConfigMap to use (if you don't use `setupConfigMap`) | `resource-dispatcher-config` |
| `giveClusterAdmin` | Setup a `ClusterRoleBinding` giving the deployment `cluster-admin` privileges if you would like to use it to manage cluster resources. | `false` |
| `specifyServiceAccount` | If you don't want to use `giveClusterAdmin` but you _do_ want to specify your own service account to run as, enable this option. | `false` |
| `serviceAccount` | The service account to use if you've enabled `specifyServiceAccount` | Not Set |
| `sshSecretConfigMap` | The name of a secret containing an SSH key to be mounted at `/sshSecret/ssh-privatekey` (ignored if not set) | Not Set |
| `exposeRoute` | Set to true to create an OCP route object | false |
| `routeHost` | If `exposeRoute` is true, set this to explicitly set the host | Not Set |

The Helm chart can be used as shown:

```shell script
cd helm
helm template my-deployment-name . | oc apply -f -
```
