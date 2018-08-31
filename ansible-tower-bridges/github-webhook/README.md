ansible-tower-bridges/github-webhook
====================================

This implementation is used to bridge GitHub webhooks to Ansible Tower. Ansible Tower expects any payload/input parameters to be passed in the `extra_vars` dictionary. Of course GitHub does not do this, and hence this "bridge" to provide that mapping for webhooks request configured on github to be sent to/through this bridge.

Requirements
------------

Although this can be run as a regular/standalone `node.js` app, it is recommended that this gets deployed on an OpenShift Container Platform for ease of maintaining it.


Running in OpenShift
--------------------

For example, use `oc new-app` to deploy the application:

```
> oc new-app openshift/nodejs:8~https://github.com/redhat-cop/tool-integrations.git --context-dir=ansible-tower-bridges/github-webhook
> oc expose service tool-integrations
```

Then add the environment variables below, and add a github webhook (with the `route` url) to test it out.

Configuration
-------------

| Variable | Description | Required | Defaults |
|:---------|:------------|:---------|:---------|
| ANSIBLE_TOWER_URL | The fqdn portion of Ansible Tower (or IP) - do not include 'http://' or 'https://' | yes | |
| ANSIBLE_TOWER_TEMPLATE_ID | The numeric template id for the job template to run | yes | |
| ANSIBLE_TOWER_USERNAME | An Ansible Tower username with the correct permissions to run the above template | yes | |
| ANSIBLE_TOWER_PASSWORD | Password for the above Ansible Tower username | yes | |
| HTTP_PORT | The http port for the application to listen on | no | 8080 |
| HTTPS_PORT | The httpd (SSL) port for the application listen on (choose this or HTTP_PORT above) | no | 8443 |
| HTTPS_SSL_CERTIFICATE | When HTTPS_PORT above is used, specify the certificate here | no | |
| HTTPS_SSL_KEY | When the HTTPS_PORT above is used, specify the certificate key here | no | |


License
-------

Apache License 2.0


Author Information
------------------

Red Hat Community of Practice & staff of the Red Hat Open Innovation Labs.
