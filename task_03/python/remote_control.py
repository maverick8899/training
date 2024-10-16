import os
import subprocess
import sys

# python3 remote_control.py <inventory> [<command>]

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print(f"Usage: python3 {sys.argv[0]} <inventory>")
    sys.exit(1)

workspace = os.getenv("WORKSPACE", ".")
build_number = os.getenv("BUILD_NUMBER", "")
log_file = f"{workspace}/remote_control_{build_number}.log"
inventory = sys.argv[1]
command = sys.argv[2] if len(sys.argv) == 3 else None

def log(message):
    """Log a message to the log file and print it."""
    try:
        with open(log_file, 'a') as f:
            print(message)  # Print to console
            f.write(f"{message}\n")  # Write to log file
    except Exception as e:
        print(f"Failed to log message: {e}")

def run_command(command, log_output=True):
    """Run a shell command and log the output."""
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if log_output:
            log(result.stdout.strip())
        if result.returncode != 0:
            log(f"Error: {result.stderr.strip()}")
        return result.returncode
    except Exception as e:
        log(f"Failed to run command '{command}': {e}")
        return 1

# Read inventory
try:
    if os.path.isfile(inventory):
        with open(inventory, 'r') as f:
            inventory_lines = f.read().replace(',', '\n')
    else:
        inventory_lines = inventory.replace(',', '\n')
        
    with open("inventory.txt", 'w') as f:
        f.write(inventory_lines)
except Exception as e:
    log(f"Failed to read inventory file: {e}")
    sys.exit(1)

# Read from inventory and connect to hosts
try:
    with open("inventory.txt", 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            user, host = line.split(':', 1)
            log(f"\n====== Connecting to {user}@{host} to run script")
            print(f"Connecting to {user}@{host}")  # Print to console
            
            ping_result = subprocess.run(f"ping -4 -c 1 {host}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            ping_return_code = ping_result.returncode

            if ping_return_code == 0:
                if command:
                    ssh_cmd = f"ssh -o StrictHostKeyChecking=no {user}@{host} {command}"
                    run_command(ssh_cmd)
                else:
                    functions_script = '''
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
    '''
                    ssh_cmd = f"ssh -o StrictHostKeyChecking=no {user}@{host} 'bash -s'"
                    subprocess.run(ssh_cmd, input=functions_script,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    scp_cmd = f"scp {user}@{host}:/home/{user}/remote_control.log {log_file}"
                    run_command(scp_cmd)
            else:
                log(f"Cannot connect to {host}. Ping failed with return code {ping_return_code}.")
except FileNotFoundError:
    log("File inventory.txt not found.")
except Exception as e:
    log(f"An error occurred while processing inventory.txt: {e}")

log("\n====== Remote Control Completed ======")
