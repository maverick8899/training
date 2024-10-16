#!/bin/bash

if [ "$#" -lt 1 ] && [ "$#" -gt 2 ]; then
    echo "Usage: $0 <inventory>"
    exit 1
fi

log_file="${WORKSPACE}/remote_control_${BUILD_NUMBER}.log"
log() {
    echo -e "$1" | tee -a "$log_file"
}
INVENTORY="$1"
COMMAND="$2"
if [ -f "$INVENTORY" ]; then
    cat "$INVENTORY" | sed 's/,/\n/g' >"inventory.txt"
else
    # echo "Inventory file not found!"
    echo "$INVENTORY" | sed 's/,/\n/g' >"inventory.txt"
fi
cat inventory.txt

functions_script='
log_file="/home/$USER/remote_control.log"
log() {
    echo -e "$1" | tee -a "$log_file"
}

install_nginx() {
    log "===== Updating package list ====="
    sudo apt update -y | tee -a "$log_file"

    log "===== Installing Nginx ====="
    sudo apt install -y nginx | tee -a "$log_file"

    if [ $? -eq 0 ]; then
        log "===== Nginx installed successfully. ====="
    else
        log "===== Nginx installation failed. ====="
        exit 1
    fi
}

start_nginx() {
    log "===== Starting & Enabling Nginx ====="
    sudo systemctl start nginx | tee -a "$log_file"
    sudo systemctl enable nginx | tee -a "$log_file"
}

check_nginx_status() {
    log "===== Checking Nginx status ====="
    sudo systemctl status nginx --no-pager | tee -a "$log_file"
}

load_sample_data() {
    log "===== Creating sample HTML page ====="
    local nginx_root="/var/www/html"
    echo "<h1>Hello world!</h1>" | sudo tee "$nginx_root/index.html" > /dev/null

    if [ -f "$nginx_root/index.html" ]; then
        log "Sample HTML page created successfully at $nginx_root/index.html"
    else
        log "Failed to create sample HTML page."
        exit 1
    fi
}

main() {
    install_nginx
    load_sample_data
    start_nginx
    check_nginx_status
}

# Call the main function
main
'

while IFS= read -r line || [ -n "$line" ]; do
    echo "$line"
    USER=$(echo "$line" | cut -d ':' -f 1)
    HOST=$(echo "$line" | cut -d ':' -f 2)

    log "\n====== Connecting to $USER@$HOST to run script"
    if [ -n "$HOST" ] && ping -4 -c 1 "$HOST" &>/dev/null; then
        if [ -n "$COMMAND" ]; then
            ssh -o StrictHostKeyChecking=no "$USER"@"$HOST" "$COMMAND"
        else
            ssh -o StrictHostKeyChecking=no "$USER"@"$HOST" "bash -s" <<<"$functions_script"
            scp "$USER"@"$HOST":/home/$USER/remote_control.log "$log_file"
        fi
    else
        log "Can not connect to $HOST."
    fi

done <"inventory.txt"

# --no-pager, lệnh sẽ xuất toàn bộ đầu ra trực tiếp ra terminal mà không qua pager, nghĩa là bạn sẽ thấy tất cả thông tin ngay lập tức mà không cần phải cuộn lên xuống.
