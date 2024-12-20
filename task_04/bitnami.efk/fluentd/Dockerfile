FROM docker.io/bitnami/fluentd:1.17.1

ENV FLUENTD_DIR=/opt/bitnami/fluentd

USER root 
RUN groupadd -g 1001 fluentd && \
    useradd -u 1001 -g root -m -d ${FLUENTD_DIR} -s /bin/bash fluentd && usermod -aG root fluentd 
    
RUN apt update -y ; apt install curl -y
RUN mkdir /docker-entrypoint-initdb.d ; mkdir -p /opt/bitnami/fluentd/buffer
RUN fluent-gem install fluent-plugin-script

COPY secret/ca.crt /usr/local/share/ca-certificates/ca.crt
COPY secret/server/* /opt/bitnami/fluentd/certs/
COPY bin/init.sh /docker-entrypoint-initdb.d/init.sh
COPY config/fluentd_aggregator_tls2.conf /opt/bitnami/fluentd/conf/fluentd.conf 

RUN update-ca-certificates
RUN chown 1001:0 ${FLUENTD_DIR} -R
RUN chmod 0775 ${FLUENTD_DIR} -R 
RUN chmod +x /docker-entrypoint-initdb.d/init.sh
USER 1001

ENTRYPOINT [ "/opt/bitnami/scripts/fluentd/entrypoint.sh" ]
CMD [ "/opt/bitnami/scripts/fluentd/run.sh" ]
