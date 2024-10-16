import os
import subprocess
import sys

# python3 remote_copy.py ip_ports.txt vagrant:192.168.33.12:/home/vagrant

if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <source_file> <inventory>")
    sys.exit(1)

workspace = os.getenv("WORKSPACE", ".")
build_number = os.getenv("BUILD_NUMBER", "")
log_file = f"{workspace}/remote_copy_{build_number}.log"
source_file = sys.argv[1]
inventory = sys.argv[2]

def log(message):
    """Append a message to the log file and print it."""
    try:
        with open(log_file, 'a') as f:
            print(message)
            f.write(f"{message}\n")
    except Exception as e:
        print(f"Failed to log message: {e}")

# Check if inventory is a file or a string and prepare inventory lines
try:
    if os.path.isfile(inventory):
        with open(inventory, 'r') as f:
            inventory_lines = f.read().replace(',', '\n')
    else:
        inventory_lines = inventory.replace(',', '\n')
except Exception as e:
    log(f"Failed to read inventory file: {e}")
    sys.exit(1)

# Write inventory lines to a new file
try:
    with open("inventory.txt", 'w') as f:
        f.write(inventory_lines)
except Exception as e:
    log(f"Failed to write to inventory.txt: {e}")
    sys.exit(1)

# Read from the inventory file and process each line
try:
    with open("inventory.txt", 'r') as f:
        for i, line in enumerate(f, start=1):  #? enumerate: insert index
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(':')
            if len(parts) != 3:
                log(f"Invalid line format in inventory: {line}")
                continue
            
            user, host, dest_path = parts

            log(f"\n [{i}] ====== Server IP: {host} ======")

            ping_cmd = f"ping -4 -c 1 {host}"
            try:
                ping_result = subprocess.run(ping_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                if ping_result.returncode == 0:
                    log(f"====== Copy {source_file} to {user}@{host}:{dest_path} ======")
                    
                    scp_cmd = f"scp {source_file} {user}@{host}:{dest_path}"
                    scp_result = subprocess.run(scp_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    if scp_result.returncode == 0:
                        log(f"Copy to {host} successful.")
                    else:
                        log(f"Copy to {host} failed. Error: {scp_result.stderr.strip()}")
                else:
                    log(f"Cannot connect to {host}. Ping failed.")
            except Exception as e:
                log(f"Failed to run ping command for {host}: {e}")
except FileNotFoundError:
    log("File inventory.txt not found.")
except Exception as e:
    log(f"An error occurred while processing inventory.txt: {e}")

log("\n====== Remote Copy Completed ======")
