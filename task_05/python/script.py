import os
import subprocess
import requests
import random
import string
import sys

print(os.getenv('MINIO_URL'))

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

accessKey=generate_random_string(20)
secretKey=generate_random_string(40)
bucket_name = sys.argv[1] if len(sys.argv) > 1 else "bucket"

def config_gitea_minio():
    session = requests.Session()
    
    cookies = { 
        '_csrf': os.getenv('CSRF_TOKEN'),
    }
    headers = { 
        'Content-Type': 'application/json'
    }
    json_data = {
        'accessKey': os.getenv('MINIO_ROOT_USER'),
        'secretKey': os.getenv('MINIO_ROOT_PASSWORD'),
    }

    #? store persistent cookie for the next request by remain alive session
    response = session.post(f"{os.getenv('MINIO_URL')}/api/v1/login", cookies=cookies, headers=headers, json=json_data, verify=False)
    print("Login: ",response.status_code, response.text) 
    json_data = {
        'policy': '',
        'accessKey': accessKey,
        'secretKey': secretKey,
        'description': 'demo',
        'comment': '',  
        'name': '',
        'expiry': None,
    }
    response = session.post(
        f"{os.getenv('MINIO_URL')}/api/v1/service-account-credentials",
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )
    print("Create token: ",response.status_code) 

    json_data = {
        'name': bucket_name,
        'versioning': {
            'enabled': True,
            'excludePrefixes': [],
            'excludeFolders': False,
        },
        'locking': False,
    }
    response = session.post(f"{os.getenv('MINIO_URL')}/api/v1/buckets", cookies=cookies, headers=headers, json=json_data)
    print("Create bucket: ",response.status_code, response.text) 

#? Create app.init for gitea
    content = f"""[storage]
STORAGE_TYPE = minio   
MINIO_ENDPOINT = {os.getenv('MINIO_ENDPOINT')}
MINIO_ACCESS_KEY_ID = {accessKey}
MINIO_SECRET_ACCESS_KEY = {secretKey}
MINIO_BUCKET = {bucket_name}
MINIO_USE_SSL = {os.getenv('MINIO_USE_SSL')} 

[server]
LFS_START_SERVER = true

[lfs]
PATH = /data/git/lfs
"""
    # os.makedirs(os.getenv('GITEA_CONFIG'), exist_ok=True)
    with open(f"{os.getenv('GITEA_CONFIG')}/app.ini", "w") as file:
        file.write(content)

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
os.makedirs("gitea/gitea/conf", exist_ok=True)

print("================Run Gitea and Minio================")
run_command("sudo docker network create gitea")
print("-------------start minio-------------")
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
print("wait for minio to be ready")
run_command("sleep 10")

print("================Setup Gitea - Minio================")
config_gitea_minio()

run_command("sudo chown git:git gitea -R")
print("-------------start gitea-------------")
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
