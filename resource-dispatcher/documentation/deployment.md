# Deployment

This is fundamentally just a Python project that versions dependencies in `Pipenv` & `Pipenv.lock` files. Any system that can run projects using Pipenv should be able to run this application.

## Configuration Modes

This application can be run in two modes:

### File Mode

In file mode, one single file is used to configure all tasks and repositories. The environment variable `CONFIG_FILE` must be set to the path of a `.yml` or `.yaml` configuration file.

### Directory Mode

In directory mode, any number of configuration files can be used simultaneously to configure the application's behavior. The environment variable `CONFIG_DIR` must be set to a path containing one or more `.yml` or `.yaml` files. Any other files in the directory are ignored (with a log message), and the directory is not traversed recursively. Individual file exclusions are not supported, so this directory must contain _only_ YAML files intended for configuration of this application.

There is no isolation between resources defined across configuration files; so repositories defined in one file are available for use by tasks in other, and name collisions (in tasks or repositories) will cause errors across config files. Additionally, multiple tasks (including across configuration files) are not allowed to bind to the same webhook trigger route.

If any top-level objects other than `repositories` and `tasks` are defined in any YAML files, a warning will be written to the console, but execution will proceed if there are no other errors.

## Kubernetes/OpenShift Deployment

There is also a Helm chart available to get up and running quickly on a container platform.

The Helm chart is available in `/helm` and has a few input parameters:

| Parameter | Description | Default |
|---|---|---|
| `setupConfigMap` | Create a ConfigMap which contains a workflow definition file. Requires `configFileContents` to also be set. | `false` |
| `configFileContents` | The contents of the config file for `setupConfigMap` to create. | `""` |
| `configMapName` | The pre-existing ConfigMap to use (if you don't use `setupConfigMap`) | `resource-dispatcher-config` |
| `useConfigDir` | If true, will attempt to load all key-value pairs in the ConfigMap as configuration data. If false, will only load a key named `config.yml`. | `false` |
| `configMapAsEnvVars` | Mounts a ConfigMap's key-value pairs as environment variables so that they can be templated into config files. Nothing mounted if set to `false`. | `false` |
| `setupClusterRoleBinding` | Setup a `ClusterRoleBinding` to give the deployment privileges if you would like to use it to manage cluster resources. | `false` |
| `clusterRole` | `ClusterRole` to bind to if `setupClusterRoleBinding` is `true`. | `cluster-admin` |
| `useServiceAccount` | If you don't want to use `setupClusterRoleBinding` but you _do_ want to specify your own service account to run as, set this flag to the service account name. | `false` |
| `sshSecretConfigMap` | The name of a secret containing an SSH key to be mounted at `/sshSecret/ssh-privatekey` (ignored if not set). | Not Set |
| `exposeRoute` | Set to true to create an OCP route object. | `false` |
| `routeHost` | If `exposeRoute` is true, set this to explicitly set the host. | Not Set |
| `enableTriggeringConfigMap` | Name of a `ConfigMap` which contains a key `enable_triggering` set to `true` or `false`. If `false`, triggering via webook or the scheduler is disabled and the Resource Dispatcher will be "dormant". The dispatcher will restart every five minutes to recheck if this is set. | Not Set (all triggering runs) |

The Helm chart can be used as shown:

```shell script
cd helm
helm template my-deployment-name . | oc apply -f -
```
