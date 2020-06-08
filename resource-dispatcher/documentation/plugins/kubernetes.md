# Kubernetes Plugin

This plugin interacts with Kubernetes clusters, either in-cluster or remotely via kubeconfig.
## Parameters

| Parameter | Description | Required | Default |
|---|---|---|---|
| `mode` | API connection mode - either `in-cluster` or `kubeconfig` | True | N/A |
| `kubeconfig` | Path to a `kubeconfig` file if `mode` is set to `kubeconfig` | False | N/A |
| `insecure` | Disable Kube API server certificate validation | False | False |
| `apply_objects.from_dir` | Path to a directory of objects to apply to a cluster | False | N/A |
| `apply_objects.namespace` | Namespace to apply objects to | False | N/A |

Note: It is intended to support actions other than `apply_objects` in the future.

## How Context Is Used

Context is not used by this plugin.

## Example Usages

```yaml
repositories:
  - name: repo
    url: https://github.com/jacobsee/stuff.git

tasks:
  - name: kubernetes-example
    description: Kubernetes plugin example
    triggers:
      - type: webhook
        route: /do_stuff
    steps:
      - plugin: kubernetes
        repository: repo
        path: objects
        params:
          mode: kubeconfig
          kubeconfig: ~/.kube/config
          insecure: true
          apply_objects:
            from_dir: "."
            namespace: "my-namespace"
```
