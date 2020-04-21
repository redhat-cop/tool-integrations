# Line Notification Gateway #

Line Notification Gateway for OpenShift Prometheus Alertmanager.

## Installation ##


# S2I Stategy build

```
#oc new-build --name=line-notify-gateway golang~https://github.com/redhat-cop/tool-integrations#master --context-dir=alertmanager-notifier-gateway/alertmanager-line-gateway

#oc new-app line-notify-gateway

#oc set probe dc/line-notify-gateway --readiness --get-url=http://:8080/healthz

#oc expose dc/line-notify-gateway --port=8080
service/line-notify-gateway exposed

#oc get svc
NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
line-notify-gateway   ClusterIP   172.30.122.39   <none>        8080/TCP   4s

```


# Docker Strategy  build

```
oc new-build --strategy=docker --name=line-notify-gateway https://github.com/redhat-cop/tool-integrations#master --context-dir=alertmanager-notifier-gateway/alertmanager-line-gateway
```

# Deploying application with non-TLS
```
#oc new-app line-notify-gateway

#oc set probe dc/line-notify-gateway --readiness --get-url=http://:8080/healthz

#oc expose dc/line-notify-gateway --port=8080
service/line-notify-gateway exposed

#oc get svc
NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
line-notify-gateway   ClusterIP   172.30.122.39   <none>        8080/TCP   4s
```

# Deploying application with Serving Certificate TLS
```
#oc new-app line-notify-gateway

#oc set probe dc/line-notify-gateway --readiness --get-url=http://:8443/healthz

#oc set env dc line-notify-gateway insecure=false tlscert=/var/lib/secrets/tls.crt tlskey=/var/lib/secrets/tls.key

#oc set volume dc/line-notify-gateway --add --name=secrets -t secret  --secret-name=line-notify --mount-path=/var/lib/secrets --overwrite

#oc expose dc/line-notify-gateway --port=8443
service/line-notify-gateway exposed

#oc get svc
NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
line-notify-gateway   ClusterIP   172.30.112.45   <none>        8443/TCP   23s

# oc annotate service line-notify-gateway service.beta.openshift.io/serving-cert-secret-name=line-notify

NOTE: Once secret generated, restart pod.
```


## Usage ##

Create your Line token here:  https://notify-bot.line.me/en/  

Set receiver of generic webhook from Alertmanager.

```yaml
receivers:
  - name: 'line'
    webhook_configs:
      - url: 'http(s)://webhook_service_name:(8080|8443)/webhook'
        http_config:
          bearer_token: '« YOUR_LINE_API_TOKEN »'
          tls_config:
            insecure_skip_verify: true
```

<img src="/alertmanager-notifier-gateway/alertmanager-line-gateway/artefacts/line2.png">
<img src="/alertmanager-notifier-gateway/alertmanager-line-gateway/artefacts/line_rcv.jpg" width="250">
