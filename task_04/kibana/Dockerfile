ARG ELK_VERSION

FROM docker.elastic.co/kibana/kibana:${ELK_VERSION}

COPY ./ca.crt /etc/pki/ca-trust/source/anchors/ca.crt
USER root
RUN update-ca-trust
USER kibana
 
CMD ["/usr/local/bin/kibana-docker"]