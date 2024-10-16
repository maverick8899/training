import sys
import os
import subprocess

#? <value_if_true> if <condition> else <value_if_false>
#? sys.argv = $0 + args = 1 + length(args)
ip_port = sys.argv[1] if len(sys.argv) == 2 and sys.argv[1] else None
if not ip_port:
    print("IP address is not provided")
    sys.exit(1)

workspace = os.getenv("WORKSPACE", ".")
build_number = os.getenv("BUILD_NUMBER", "")
log_file = f"{workspace}/autoping_{build_number}.log"

def log(message):
    """Append a message to the log file and print it."""
    try:
        with open(log_file, 'a') as f:
            print(message)
            f.write(f"{message}\n")
    except Exception as e:
        print(f"Failed to log message: {e}")

# Prepare IP ports and write to a file
ip_ports = ip_port.replace(',', '\n')
try:
    with open("ip_ports.txt", 'w') as f:
        f.write(ip_ports)
except Exception as e:
    log(f"Failed to write to ip_ports.txt: {e}")
    sys.exit(1)

try:
    with open("ip_ports.txt", 'r') as f:
        for i,line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            
            try:
                target, port = line.split(':')
            except ValueError as e:
                log(f"Invalid line format in ip_ports.txt: {line}. Error: {e}")
                continue
            
            log(f"\n[{i}] ====== Pinging {target} ======")
            ping_cmd = ["ping", "-4", "-c", "4", target]
            try:
                ping_result = subprocess.run(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if ping_result.returncode == 0:
                    log(f"Ping to {target} successful.")
                else:
                    log(f"Ping to {target} failed.")
            except Exception as e:
                log(f"Failed to run ping command for {target}: {e}")

            log(f"\n[{i}] ====== Checking port {port} on {target} ======")
            nc_cmd = ["nc", "-zv", "-w", "30", target, port]
            try:
                nc_result = subprocess.run(nc_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if nc_result.returncode == 0:
                    log(f"Port {port} on {target} is open.")
                else:
                    log(f"Port {port} on {target} is closed.")
            except Exception as e:
                log(f"Failed to run nc command for {target}:{port}: {e}")

            i += 1
except FileNotFoundError:
    log("File ip_ports.txt not found.")
except Exception as e:
    log(f"An error occurred while processing ip_ports.txt: {e}")

log("\n====== Auto Ping Completed ======")
