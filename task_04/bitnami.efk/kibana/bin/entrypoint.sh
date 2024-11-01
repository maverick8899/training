#!/bin/bash
# Copyright Broadcom, Inc. All Rights Reserved.
# SPDX-License-Identifier: APACHE-2.0

# shellcheck disable=SC1091

#@ custom get service account token =================================================================

echo "Elasticsearch URL: $KIBANA_ELASTICSEARCH_URL"

max_wait=120
interval=5
elapsed_time=0
KIBANA_CONFIG=/opt/bitnami/kibana/config/kibana.yml
# KIBANA_CONFIG=/usr/share/kibana/kibana.yml

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

#@ ===============================================================================================

set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace

# Load libraries
. /opt/bitnami/scripts/libkibana.sh
. /opt/bitnami/scripts/libbitnami.sh
. /opt/bitnami/scripts/liblog.sh

# Load environment
. /opt/bitnami/scripts/kibana-env.sh

print_welcome_page

# We add the copy from default config in the entrypoint to not break users 
# bypassing the setup.sh logic. If the file already exists do not overwrite (in
# case someone mounts a configuration file in /opt/bitnami/elasticsearch/conf)
debug "Copying files from $SERVER_DEFAULT_CONF_DIR to $SERVER_CONF_DIR"
cp -nr "$SERVER_DEFAULT_CONF_DIR"/. "$SERVER_CONF_DIR"

if ! is_dir_empty "$SERVER_DEFAULT_PLUGINS_DIR"; then
    debug "Copying plugins from $SERVER_DEFAULT_PLUGINS_DIR to $SERVER_PLUGINS_DIR"
    # Copy the plugins installed by default to the plugins directory
    # If there is already a plugin with the same name in the plugins folder do nothing
    for plugin_path in "${SERVER_DEFAULT_PLUGINS_DIR}"/*; do
        plugin_name="$(basename "$plugin_path")"
        plugin_moved_path="${SERVER_PLUGINS_DIR}/${plugin_name}"
        if ! [[ -d "$plugin_moved_path" ]]; then
            cp -r "$plugin_path" "$plugin_moved_path" 
        fi
    done
fi

if [[ "$1" = "/opt/bitnami/scripts/kibana/run.sh" ]]; then
    info "** Starting Kibana setup **"
    /opt/bitnami/scripts/kibana/setup.sh
    info "** Kibana setup finished! **"
fi

echo ""
exec "$@"