#@ maverick0809/bitnami_elasticsearch_tls:8.15.3_cn[123]
FROM bitnami/elasticsearch:8.15.3

ENV ELASTIC_DIR=/opt/bitnami/elasticsearch

USER root
RUN groupadd -g 1001 elasticsearch && \
    useradd -u 1001 -g elasticsearch -m -d ${ELASTIC_DIR} -s /bin/bash elasticsearch && \
    chmod 0775 ${ELASTIC_DIR} -R

COPY secret/ca.crt  ${ELASTIC_DIR}/config/ca.crt   
COPY secret/ca.crt /usr/local/share/ca-certificates/ca.crt
COPY secret/elasticsearch.crt ${ELASTIC_DIR}/config/elasticsearch.crt
COPY secret/elasticsearch.key ${ELASTIC_DIR}/config/elasticsearch.key
COPY secret/elasticsearch.keystore ${ELASTIC_DIR}/config/elasticsearch.keystore

#@ Cluster config elasticsearch[123]
COPY config/elasticsearch3.yml ${ELASTIC_DIR}/config/elasticsearch.yml 

RUN update-ca-certificates
RUN chown 1001:0 ${ELASTIC_DIR} -R

USER 1001

ENTRYPOINT [ "/opt/bitnami/scripts/elasticsearch/entrypoint.sh" ]
CMD [ "/opt/bitnami/scripts/elasticsearch/run.sh" ]
