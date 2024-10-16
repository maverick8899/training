#!/bin/bash

log_file="${WORKSPACE}/jenkins_server_check.log"

log() {
    echo -e "$1" | tee -a "$log_file"
}

# Check CPU usage
log "\n====== Checking CPU usage ======"
top -b -n1 | head -n 3 | tee -a "$log_file"

# Check Memory usage
log "\n====== Checking Memory usage ======"
free -m | tee -a "$log_file"

# Check Disk usage
log "\n====== Checking Disk usage ======"
df -h | tee -a "$log_file"

# Check Disk I/O for performance issues
log "\n====== Checking Disk I/O performance ======"
if ! command -v iostat &>/dev/null; then
    sudo apt update -y
    sudo apt install sysstat -y
fi
iostat -x | tee -a "$log_file"

# Check Network connectivity
log "\n====== Checking network connectivity ======"
ping -4 -c 4 google.com &>/dev/null
if [ $? -eq 0 ]; then
    log "Network is reachable"
else
    log "Network is NOT reachable"
fi

log "\n====== Running Services ======"
systemctl list-units --type=service --state=running

log "\n====== Firewall Status ======"
if ! command -v ufw &>/dev/null; then
    sudo apt update -y
    sudo apt install ufw -y
fi
if sudo ufw status | grep -q "Status: active"; then
    log "UFW is active. Here are the rules:"
    sudo ufw status verbose
else
    log "Firewall is inactive."
fi

echo "\n====== Ports Listening ======"
if ! command -v netstat &>/dev/null; then
    sudo apt update -y
    sudo apt install net-tools -y
fi
sudo netstat -tlpun
# Check Jenkins logs for recent errors
# log "\n====== Checking recent Jenkins logs for errors ======"
# jenkins_log_file="/var/log/jenkins/jenkins.log"
# log "Displaying the last 50 lines of Jenkins log:"
# if [ -f "$jenkins_log_file" ] && [ -s "$jenkins_log_file" ]; then
#     tail -n 50 "$jenkins_log_file" | tee -a "$log_file"
# else
#     journalctl -xeu jenkins | tail -n 50 | tee -a "$log_file"
# fi

log "\n====== Server Check Completed ======"
