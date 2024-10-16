#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_file> <inventory>"
    exit 1
fi

log_file="${WORKSPACE}/remote_copy_${BUILD_NUMBER}.log"

log() {
    echo -e "$1" | tee -a "$log_file"
}

SOURCE_FILE="$1"
INVENTORY="$2"

if [ -f "$INVENTORY" ]; then
    cat "$INVENTORY" | sed 's/,/\n/g' >"inventory.txt"
else
    # echo "Inventory file not found!"
    echo "$INVENTORY" | sed 's/,/\n/g' >"inventory.txt"
fi
cat inventory.txt

while IFS= read -r line || [ -n "$line" ]; do
    echo "$line"
    USER=$(echo "$line" | cut -d ':' -f 1)
    HOST=$(echo "$line" | cut -d ':' -f 2)
    DEST_PATH=$(echo "$line" | cut -d ':' -f 3)

    log "\n====== Server IP: $HOST ======"
    if [ -n "$HOST" ] && ping -4 -c 1 "$HOST" &>/dev/null; then

        log "====== Copy $SOURCE_FILE to $USER@$HOST:$DEST_PATH ======"
        scp "$SOURCE_FILE" "$USER"@"$HOST":"$DEST_PATH"

        [ $? -eq 0 ] && log "Copy to $HOST successful." || log "Copy to $HOST failed."

    else
        log "Can not connect to $HOST"
    fi
done <"inventory.txt"
