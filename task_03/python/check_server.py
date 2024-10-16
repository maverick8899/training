import os
import subprocess
import shutil

log_file = os.path.join(os.getenv('WORKSPACE', '.'), 'jenkins_server_check.log')

def log(message):
    """Append a message to the log file and print it."""
    try:
        with open(log_file, 'a') as f:  #? a:append
            print(message)
            f.write(f"{message}\n")
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
        return 1  # Return a non-zero exit code to indicate failure

log("\n====== Checking CPU usage ======")
run_command("top -b -n1 | head -n 3")

log("\n====== Checking Memory usage ======")
run_command("free -m")

log("\n====== Checking Disk usage ======")
run_command("df -h")

log("\n====== Checking Disk I/O performance ======")
try:
    if not shutil.which("iostat"):
        log("iostat not found, installing sysstat...")
        run_command("sudo apt install sysstat -y")
    run_command("iostat -x")
except Exception as e:
    log(f"Failed to check Disk I/O performance: {e}")

log("\n====== Checking network connectivity ======")
try:
    if run_command("ping -4 -c 4 google.com", log_output=False) == 0:
        log("Network is reachable")
    else:
        log("Network is NOT reachable")
except Exception as e:
    log(f"Failed to check network connectivity: {e}")

log("\n====== Running Services ======")
run_command("systemctl list-units --type=service --state=running")

log("\n====== Firewall Status ======")
if subprocess.run("command -v ufw", shell=True).returncode != 0:
    log("ufw not found, installing ufw..")
    run_command("sudo apt update -y")
    run_command("sudo apt install ufw -y")
firewall_status = subprocess.run("sudo ufw status", shell=True, stdout=subprocess.PIPE, text=True)
if "Status: active" in firewall_status.stdout.strip():
    log("UFW is active. Here are the rules:")
    run_command("sudo ufw status verbose")
else:
    log("Firewall is inactive.")

log("\n====== Ports Listening ======")
if subprocess.run("command -v netstat", shell=True).returncode != 0:
    log("netstat not found, installing net-tools...")
    run_command("sudo apt update -y")
    run_command("sudo apt install net-tools -y")
run_command("sudo netstat -tlpun")

# log("\n====== Checking recent Jenkins logs for errors ======")
# log("Displaying the last 50 lines of Jenkins log:")

# jenkins_log_file = "/var/log/jenkins/jenkins.log"

# try:
#     if os.path.isfile(jenkins_log_file) and os.path.getsize(jenkins_log_file) > 0:
#         run_command(f"tail -n 50 {jenkins_log_file}")
#     else:
#         run_command("journalctl -xeu jenkins | tail -n 50")
# except Exception as e:
#     log(f"Failed to read Jenkins logs: {e}")

log("\n====== Jenkins Server Check Completed ======")
