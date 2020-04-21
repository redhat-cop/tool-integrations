
FROM golang:1.13

USER 1001

RUN mkdir -p /go/src/github.com/redhat-cop/alertmanager-telegram-gateway
WORKDIR /go/src/github.com/redhat-cop/alertmanager-telegram-gateway

COPY . /go/src/github.com/redhat-cop/alertmanager-telegram-gateway
ENV GOCACHE=on
ENV GO111MODULE=off
ENV GOCACHE=/go/src/github.com/redhat-cop/alertmanager-telegram-gateway
RUN go get
RUN go build

EXPOSE 8080

CMD ["./alertmanager-telegram-gateway"]