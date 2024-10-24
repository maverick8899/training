FROM docker.elastic.co/elasticsearch/elasticsearch:7.16.0

COPY ca.crt  /usr/share/elasticsearch/config/ca.crt
COPY elasticsearch.crt /usr/share/elasticsearch/config/elasticsearch.crt
COPY elasticsearch.key /usr/share/elasticsearch/config/elasticsearch.key
COPY elasticsearch.yml  /usr/share/elasticsearch/config/elasticsearch.yml

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["eswrapper"]
