# quay/imagestream-sync

This implementation is used to synchronize images that are stored in [Quay](https://coreos.com/quay-enterprise/) and are referenced as ImageStreams within the OpenShift Container Platform from [Quay notifications](https://docs.quay.io/guides/notifications.html).


## Requirements

Although this can be run as a regular/standalone `node.js` app, it is recommended that this gets deployed on an OpenShift Container Platform for ease of maintenance. A minimum of NodeJS version 8 is required.

## Configuration Options

The following configuration items tune and control the behavior of the application.

| Variable | Description | Defaults |
|:---------|:------------|:---------|
| HTTP_PORT | The http port for the application to listen on | 8080 |
| HTTPS_PORT | The httpd (SSL) port for the application listen on (choose this or HTTP_PORT above) | 8443 |
| HTTPS_SSL_CERTIFICATE | When HTTPS_PORT above is used, specify the certificate here | |
| HTTPS_SSL_KEY | When the HTTPS_PORT above is used, specify the certificate key here | |
| TOKEN_FILE | Location of a file containing the contents of an OAuth token to authenticate to the OpenShift API | `/var/run/secrets/kubernetes.io/serviceaccount/token` |
| CA_FILE | Location of the certificate to communicate securely with the OpenShift API | `/var/run/secrets/kubernetes.io/serviceaccount/ca.crt` |
| AUTH_TOKEN | Value of the token used to communicate with the OpenShift API | |
| MASTER_URL | Address of the OpenShift Master  | `https://kubernetes.default.svc:443` |
| TLS_INSECURE | Allow insecure communication to the OpenShift API  | `false` |
| NAMESPACE | Single namespace to allow image synchronization (defaults to entire cluster)  | |

## Running in OpenShift

### Prerequisites

This application makes queries to the OpenShift API. The service account associated with the application must have sufficient rights to query for ImageStreams either at a cluster scope or namespace scope.

The following command can be added to grant access to a service account at a cluster level using the included `registry-editor` ClusterRole.

```
$ oc adm policy add-cluster-role-to-user registry-editor -z <service-account>
```

To limit to a single namespace, the following command can be used:

```
$ oc project <namespace>
$ oc policy add-role-to-user registry-editor -z <service-account>
```

### Application Deployment

The `oc new-app` command in combination with `oc expose` command can be used to deploy the application:

```
$ oc new-app --name=quay-imagestream-sync openshift/nodejs:8~https://github.com/redhat-cop/tool-integrations.git --context-dir=quay/imagestream-sync
$ oc expose service quay-imagestream-sync
```

Then add the environment variables below, and add a github webhook (with the `route` url) to test it out.

## Quay Configuration

The final step is to configure Quay to send webhook notifications to the application deployed in OpenShift. 

First, obtain the url of the application previously deployed.

```
$ oc get routes quay-imagestream-sync --template='{{ .spec.host }}'
```

Login to quay and locate the repository associated with the image that has been previously configured in OpenShift. 

Click on **Settings** and then **Create Notification**

Under _When this event occurs_ dropdown, select **Push to Repository**.

Under _Then issue a Notification_ dropdown, select **Webhook POST**

Enter the URL of the webhook based on the result from the route found previously (such as `http://quay-imagestream-sync.myproject.apps.ocp.example.com`)

Optionally, provide a _Notification title_ to easily identify the webhook.

Select **Create Notification**


License
-------

Apache License 2.0


Author Information
------------------

Red Hat Community of Practice
