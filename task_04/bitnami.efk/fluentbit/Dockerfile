FROM bitnami/fluent-bit:3.2.2-debian-12-r0

USER root 

COPY secret/client/* /opt/bitnami/fluent-bit/certs/
COPY config/fluentbit.conf /opt/bitnami/fluent-bit/conf/fluent-bit.conf

USER 1001

ENTRYPOINT [ "fluent-bit" ]
CMD [ "-c", "/opt/bitnami/fluent-bit/conf/fluent-bit.conf"]