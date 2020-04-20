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

## Usage ##

Create your Line token here:  https://notify-bot.line.me/en/  

Set receiver of generic webhook from Alertmanager.

```yaml
receivers:
  - name: 'line'
    webhook_configs:
      - url: 'http://webhook_service_name:5000/webhook'
        http_config:
          bearer_token: '« YOUR_LINE_API_TOKEN »'
```

<img src="/alertmanager-notifier-gateway/alertmanager-line-gateway/artefacts/line2.png">
<img src="/alertmanager-notifier-gateway/alertmanager-line-gateway/artefacts/line_rcv.jpg" width="250">
