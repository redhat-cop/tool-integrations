FROM registry.access.redhat.com/ubi8/go-toolset:latest

USER 1001

WORKDIR /opt/app-root/src

COPY  . /opt/app-root/src

RUN go get
RUN go build

EXPOSE 8080 8443

CMD ["./alertmanager-telegram-gateway"]
