import os
import subprocess

def run_command(command):
    """Helper function to run shell commands."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing: {command}\n{stderr.decode()}")
    else:
        print(stdout.decode())

print("================Create git user-group================")
def ensure_git_group_and_user(gid, uid, username="git", groupname="git"):
    check_group = f"getent group {groupname}"
    if subprocess.run(check_group, shell=True, stdout=subprocess.PIPE).returncode == 0:
        print(f"Group '{groupname}' exists. Modifying GID to {gid}.")
        run_command(f"sudo groupmod -g {gid} {groupname}")
    else:
        print(f"Group '{groupname}' does not exist. Creating with GID {gid}.")
        run_command(f"sudo groupadd -g {gid} {groupname}")

    check_user = f"id -u {username}"
    if subprocess.run(check_user, shell=True, stdout=subprocess.PIPE).returncode == 0:
        print(f"User '{username}' already exists. Ensuring they are part of group '{groupname}'.")
        run_command(f"sudo usermod -aG {groupname} {username}")
    else:
        print(f"User '{username}' does not exist. Creating with UID {uid} and adding to group '{groupname}'.")
        run_command(f"sudo useradd -m -u {uid} -g {groupname} {username}")

ensure_git_group_and_user(gid=1500, uid=1500)

print("================Install Docker================")
run_command("curl -fsSL https://get.docker.com/ | sh")
run_command("sudo systemctl start docker")
run_command("sudo usermod -aG docker git")
run_command("sudo usermod -aG docker $USER")
# run_command("sudo newgrp docker")

print("================Install Git LFS================")
run_command("sudo apt update -y && sudo apt install -y git git-lfs && git lfs install")

print("================Creating directories for Gitea and setting permissions================")
os.makedirs("gitea", exist_ok=True)
run_command("sudo chown git:git gitea")

print("================Run Gitea and Minio================")
run_command("sudo docker network create gitea")

run_command(
    "sudo docker run -d "
    "--name gitea "
    "--network gitea "
    "--restart always "
    "-e USER_UID=1500 "
    "-e USER_GID=1500 "
    f"-v {os.getcwd()}/gitea:/data "
    "-v /home/git/.ssh:/data/git/.ssh "
    "-v /etc/timezone:/etc/timezone:ro "
    "-v /etc/localtime:/etc/localtime:ro "
    "-p 3000:3000 "
    "-p 2222:22 "
    "gitea/gitea"
)

run_command(
    "sudo docker run -d "
    "--name minio "
    "--network gitea "
    f"-v {os.getcwd()}/storage:/data "
    "-p 9000:9000 "
    "-p 9001:9001 "
    "maverick0809/minio "
    "server --console-address ':9001' /data"
)
