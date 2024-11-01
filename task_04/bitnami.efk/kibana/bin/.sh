
echo "Elasticsearch URL: $KIBANA_ELASTICSEARCH_URL"

max_wait=120
interval=5
elapsed_time=0
KIBANA_CONFIG=/opt/bitnami/kibana/config/kibana.yml

while true; do

    token_value=$(curl -k -s -X POST -u $ELASTIC_USERNAME:$ELASTIC_PASSWORD "$KIBANA_ELASTICSEARCH_URL/_security/service/elastic/kibana/credential/token/kibana_token?pretty" | grep value | cut -d ':' -f 2)

    if ! curl -k -s $KIBANA_ELASTICSEARCH_URL >/dev/null; then
        echo "Waiting for Elasticsearch to be ready..."
        sleep $interval
        elapsed_time=$((elapsed_time + interval))
        continue
    fi

    if [ -n "$token_value" ]; then
        echo "Token is not existing, Creating new token"
        sed -i "s|^\(elasticsearch.serviceAccountToken:\).*|\1 ${token_value}|g" ${KIBANA_CONFIG}
        echo "Token retrieved: $token_value"
        cat ${KIBANA_CONFIG}
        break
    else 
        echo "Token already exists, creating new token"
        curl -k -s -X DELETE -u $ELASTIC_USERNAME:$ELASTIC_PASSWORD "$KIBANA_ELASTICSEARCH_URL/_security/service/elastic/kibana/credential/token/kibana_token" > /dev/null
        token_value=$(curl -k -s -X POST -u $ELASTIC_USERNAME:$ELASTIC_PASSWORD "$KIBANA_ELASTICSEARCH_URL/_security/service/elastic/kibana/credential/token/kibana_token?pretty" | grep value | cut -d ':' -f 2)
        sed -i "s|^\(elasticsearch.serviceAccountToken:\).*|\1 ${token_value}|g" ${KIBANA_CONFIG}
        echo "Token retrieved: $token_value"
        cat ${KIBANA_CONFIG}
        break
    fi

    if [ "$elapsed_time" -ge "$max_wait" ]; then
        echo "Exceeded maximum wait time of ${max_wait} seconds."
        exit 1
    fi

    echo "Waiting for Elasticsearch to be ready..."
    sleep $interval
    elapsed_time=$((elapsed_time + interval))
done
