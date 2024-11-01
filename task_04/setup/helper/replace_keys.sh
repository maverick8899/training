#!/bin/bash

ES_SECRET_DIR=../../bitnami.efk/elasticsearch/secret/
KIBANA_SECRET_DIR=../../bitnami.efk/kibana/secret/
FLUENTD_SECRET_DIR=../../bitnami.efk/fluentd/secret/
target_dirs=($ES_SECRET_DIR $KIBANA_SECRET_DIR $FLUENTD_SECRET_DIR)

echo -e "====== Replace root CA ======\n"
for dir in ${target_dirs[@]}; do
    cp ../secrets/certificate_authority/ca/ca.crt "$dir"
done

echo -e "\n====== Replace ELASTICSEARCH Secrets ======"
cp ../secrets/elasticsearch.keystore $ES_SECRET_DIR
cp ../secrets/certificates/elasticsearch/elasticsearch.crt $ES_SECRET_DIR
cp ../secrets/certificates/elasticsearch/elasticsearch.key $ES_SECRET_DIR

echo -e "\n====== Replace KIBANA Secrets ======"
cp ../secrets/certificates/kibana/kibana.crt $KIBANA_SECRET_DIR
cp ../secrets/certificates/kibana/kibana.key $KIBANA_SECRET_DIR

echo -e "\n====== Replace Secrets Successfully ======"
