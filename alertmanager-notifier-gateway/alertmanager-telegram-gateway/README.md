# Telegram Notification Gateway #

Line Notification Gateway for OpenShift Prometheus Alertmanager.

## Installation ##

# Pre-req
To send alert to Telegram we need below items:  
a. API Token  
b. Chat ID  


1. Create telegram bot via [BotFather](https://core.telegram.org/bots#6-botfather).
2. Using BotFather get the [token](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token).
3. Get the chat ID ( you must send some test message to the bot before run this step). Fetch the chat ID using (note the "id" section):
```
#curl https://api.telegram.org/<BOT_TOKEN>/getUpdates

{"ok":true,"result":[{"update_id":502830325,
"message":{"message_id":3,"from":{"id":962xxxx,"is_bot":false,"first_name":"John","last_name":"Doe","language_code":"en"},"chat":{"id":962xxxx,"first_name":"John","last_name":"Doe","type":"private"},"date":1587444744,"text":"hello"}}]}
```

Hence, your API Token is the "BOT_TOKEN" and Chat ID is "id".

# S2I Stategy build

```
#oc new-build --name=telegram-notify-gateway golang~https://github.com/redhat-cop/tool-integrations#master --context-dir=alertmanager-notifier-gateway/alertmanager-telegram-gateway

#oc new-app telegram-notify-gateway

#oc set env dc telegram-notify-gateway chat_id=<Chat ID>

#oc set probe dc/telegram-notify-gateway --readiness --get-url=http://:8080/healthz

#oc expose dc/telegram-notify-gateway --port=8080
service/telegam-notify-gateway exposed

#oc get svc
NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
telegram-notify-gateway   ClusterIP   172.30.122.21   <none>        8080/TCP   4s

```


## Usage ##

Create all necessary pre-req as above.

Set receiver of generic webhook from Alertmanager.



```yaml
"receivers":
  - "name": "team-telegram"
    "webhook_configs":
    - "url": "<http://telegram-notify-gateway-service-url>:8080/webhook"
      "http_config":
         "basic_auth":
            "username" : "bot902xxxx"
            "password" : "AAHzxxxxxxxxx"
```
NOTE: The basic_auth are coming from auth token that has been splitted. E.g
```
bot902xxxx:AAHzxxxxxxxxx
```


<img src="/alertmanager-notifier-gateway/alertmanager-line-gateway/artefacts/line2.png">
<img src="/alertmanager-notifier-gateway/alertmanager-line-gateway/artefacts/line_rcv.jpg" width="250">
