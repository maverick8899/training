# https://github.com/elastic/kibana-docker/blob/master/.tedi/template/Dockerfile.j2
FROM docker.elastic.co/kibana/kibana:7.16.0

ENV CONFIG_DIR=/usr/share/kibana/config

COPY ca.crt /etc/pki/ca-trust/source/anchors/ca.crt
COPY ca.crt ${CONFIG_DIR}/ca.crt
COPY kibana.crt ${CONFIG_DIR}/kibana.crt
COPY kibana.key ${CONFIG_DIR}/kibana.key
COPY kibana.yml ${CONFIG_DIR}/kibana.yml

USER root
RUN update-ca-trust
USER kibana

CMD ["/usr/local/bin/kibana-docker"]
