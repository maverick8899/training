# https://hub.docker.com/r/bitnami/kibana
# https://github.com/bitnami/containers/blob/main/bitnami/kibana/8/debian-12/Dockerfile
FROM bitnami/kibana:8.15.3

ENV KIBANA_DIR=/opt/bitnami/kibana
ENV CONFIG_DIR=/opt/bitnami/kibana/config

USER root
RUN groupadd -g 1001 kibana && \
    useradd -u 1001 -g kibana -m -d ${CONFIG_DIR} -s /bin/bash kibana && \
    chgrp 0 ${CONFIG_DIR} 

COPY secret/ca.crt /usr/local/share/ca-certificates/ca.crt
COPY secret/ca.crt ${CONFIG_DIR}/ca.crt
COPY secret/kibana.crt ${CONFIG_DIR}/kibana.crt
COPY secret/kibana.key ${CONFIG_DIR}/kibana.key
    
COPY config/kibana.yml ${CONFIG_DIR}/kibana.yml
COPY bin/entrypoint.sh /opt/bitnami/scripts/kibana/entrypoint.sh
RUN update-ca-certificates

RUN chmod ug+x /opt/bitnami/scripts/kibana/entrypoint.sh
RUN chown 1001:0 ${KIBANA_DIR} -R && chown 1001:0 /bitnami/kibana/data
USER 1001

ENTRYPOINT [ "/opt/bitnami/scripts/kibana/entrypoint.sh" ]
CMD [ "/opt/bitnami/scripts/kibana/run.sh" ]
