#!/bin/bash

# fluent-gem install fluent-plugin-script
# gem install fluent-plugin-dedup

while true; do
    if ! curl -k -s $ELASTIC_URL >/dev/null; then
        echo "Waiting for Elasticsearch to be ready..."
        sleep 5
    else
        echo "Elasticsearch is ready"
        break
    fi
done

echo "Creating new user $FLUENTD_USER..."
response=$(curl -k -s -o /tmp/curl_output -w "%{http_code}" -X POST -u $ELASTIC_USERNAME:$ELASTIC_PASSWORD "$ELASTIC_URL/_security/user/$FLUENTD_USER" \
-H "Content-Type: application/json" \
-d "{
  \"password\": \"$FLUENTD_PASSWORD\",
  \"roles\": [\"fluentd_writer\"]
}")

if [ "$response" -eq 200 ]; then
  echo "User '$FLUENTD_USER' successfully created."
else
  echo "Failed to create user. HTTP status: $response"
  echo "Response:"
  cat /tmp/curl_output
fi

# Cấp quyền cho người dùng mới
echo "Granting privileges to $FLUENTD_USER user..."
response=$(curl -k -s -o /tmp/curl_output -w "%{http_code}" -X PUT -u $ELASTIC_USERNAME:$ELASTIC_PASSWORD "$ELASTIC_URL/_security/role/fluentd_writer" \
-H "Content-Type: application/json" \
-d '{
  "cluster": ["all"],
  "indices": [
    {
      "names": ["*"],
      "privileges": ["create_doc", "create", "delete", "index", "write", "all"]
    }
  ]
}')

if [ "$response" -eq 200 ]; then
  echo "Role 'fluentd_writer' successfully created."
else
  echo "Failed to create role. HTTP status: $response"
  echo "Response:"
  cat /tmp/curl_output
fi



# fluent-gem install fluent-plugin-tail-multiline
# touch /opt/bitnami/fluentd/logs/fluentd.log
# # log_folder=$(cat /proc/self/cgroup | grep "docker" | sed 's/.*\///' | uniq)
# log_folder=$(ls -1 /var/lib/docker/containers/ | grep $(cat /etc/hostname))
# export LOG_PATH="/var/lib/docker/containers/$log_folder/$log_folder-json.log"
# echo "$LOG_PATH"
# tail -f "$LOG_PATH" >>/opt/bitnami/fluentd/logs/fluentd.log &

# ln -sf /dev/stdout /opt/bitnami/fluentd/logs/fluentd.log
# ln -sf /dev/stderr /opt/bitnami/fluentd/logs/fluentd_e.log
