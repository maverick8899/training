FROM docker.elastic.co/kibana/kibana:7.16.0

COPY ca.crt /etc/pki/ca-trust/source/anchors/ca.crt
COPY ca.crt /usr/share/kibana/config/ca.crt
COPY kibana.crt /usr/share/kibana/config/kibana.crt
COPY kibana.key /usr/share/kibana/config/kibana.key
COPY kibana.yml /usr/share/kibana/config/kibana.yml

USER root
RUN update-ca-trust
USER kibana

CMD ["/usr/local/bin/kibana-docker"]    
