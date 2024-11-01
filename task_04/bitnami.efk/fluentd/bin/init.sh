#!/bin/bash

while true; do
    if ! curl -k -s $ELASTIC_URL >/dev/null; then
        echo "Waiting for Elasticsearch to be ready..."
        sleep 5
    else
        echo "Elasticsearch is ready"
        break
    fi
done

touch /opt/bitnami/fluentd/logs/fluentd.log
# log_folder=$(cat /proc/self/cgroup | grep "docker" | sed 's/.*\///' | uniq)
log_folder=$(ls -1 /var/lib/docker/containers/ | grep $(cat /etc/hostname))
export LOG_PATH="/var/lib/docker/containers/$log_folder/$log_folder-json.log"
echo "$LOG_PATH"
tail -f "$LOG_PATH" >>/opt/bitnami/fluentd/logs/fluentd.log &

# ln -sf /dev/stdout /opt/bitnami/fluentd/logs/fluentd.log
# ln -sf /dev/stderr /opt/bitnami/fluentd/logs/fluentd_e.log
