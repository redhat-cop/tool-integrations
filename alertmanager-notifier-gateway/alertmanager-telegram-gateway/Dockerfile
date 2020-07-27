FROM registry.access.redhat.com/ubi8/go-toolset:latest AS builder

USER 1001

WORKDIR /opt/app-root/src

COPY  . /opt/app-root/src

RUN go get
RUN go build

FROM registry.redhat.io/ubi8/ubi-minimal:latest

COPY --from=builder /opt/app-root/src/alertmanager-telegram-gateway .

EXPOSE 8080 8443

CMD ["./alertmanager-telegram-gateway"]
