FROM bitnami/elasticsearch:8.15.3

ENV ELASTIC_DIR=/opt/bitnami/elasticsearch

USER root
RUN groupadd -g 1001 elasticsearch && \
    useradd -u 1001 -g elasticsearch -m -d ${ELASTIC_DIR} -s /bin/bash elasticsearch && \
    chmod 0775 ${ELASTIC_DIR} -R

COPY ca.crt  ${ELASTIC_DIR}/config/ca.crt
COPY elasticsearch.crt ${ELASTIC_DIR}/config/elasticsearch.crt
COPY elasticsearch.key ${ELASTIC_DIR}/config/elasticsearch.key
COPY elasticsearch.yml  ${ELASTIC_DIR}/config/elasticsearch.yml
COPY elasticsearch.keystore ${ELASTIC_DIR}/config/elasticsearch.keystore
 
RUN chown 1001:0 ${ELASTIC_DIR} -R
USER 1001

ENTRYPOINT [ "/opt/bitnami/scripts/elasticsearch/entrypoint.sh" ]
CMD [ "/opt/bitnami/scripts/elasticsearch/run.sh" ]
