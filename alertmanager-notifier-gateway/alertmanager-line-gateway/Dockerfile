FROM docker.io/library/golang:1.14

USER 1001

RUN mkdir -p /go/src/github.com/redhat-cop/alertmanager-line-gateway
WORKDIR /go/src/github.com/redhat-cop/alertmanager-line-gateway

COPY . /go/src/github.com/redhat-cop/alertmanager-line-gateway
ENV GOCACHE=on
ENV GO111MODULE=off
ENV GOCACHE=/go/src/github.com/redhat-cop/alertmanager-line-gateway
RUN go get
RUN go build

EXPOSE 8080 8443

CMD ["./alertmanager-line-gateway"]
