# https://github.com/elastic/elasticsearch-docker/blob/master/.tedi/template/Dockerfile.j2
FROM docker.elastic.co/elasticsearch/elasticsearch:7.16.0

ENV CONFIG_DIR=/usr/share/elasticsearch/config

COPY ca.crt  ${CONFIG_DIR}/ca.crt
COPY elasticsearch.crt ${CONFIG_DIR}/elasticsearch.crt
COPY elasticsearch.key ${CONFIG_DIR}/elasticsearch.key
COPY elasticsearch.yml  ${CONFIG_DIR}/elasticsearch.yml
COPY elasticsearch.keystore ${CONFIG_DIR}/elasticsearch.keystore

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["eswrapper"]
