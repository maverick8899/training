import os
import subprocess
import requests
import random
import string
import sys

def is_installed(package_name):
    """ Check is installed."""
    try:
        subprocess.run(["which", package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False
    
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
PATH = {os.getenv('GITEA_LFS_PATH')}
"""
    
    print("================Creating configuration for Gitea================")
    os.makedirs(os.getenv('GITEA_CONFIG'), exist_ok=True)
    with open(f"{os.getenv('GITEA_CONFIG')}/app.ini", "w") as file:
        file.write(content)
    run_command(f"sudo chown git:git {os.getenv('GITEA_CONFIG')} -R")

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

if is_installed("docker"):
    print("Docker is already installed.")
else:
    print("================Install Docker================")
    run_command("curl -fsSL https://get.docker.com/ | sh")
    run_command("sudo systemctl start docker")
    run_command("sudo usermod -aG docker git")
    run_command("sudo usermod -aG docker $USER")

if is_installed("git"):
    print("Git is already installed.")
else:
    print("================Install Git LFS================")
    run_command("sudo apt update -y && sudo apt install -y git git-lfs && git lfs install")

print("================Run Gitea and Minio================")

print("-------------create network-------------")
run_command("sudo docker network create gitea")

print("-------------start minio-------------") 
run_command(f"sudo docker compose -f {os.getenv('COMPOSE_PATH')} up -d minio")
print("wait for minio to be ready")
run_command("sleep 5")

print("================Setup Gitea - Minio================")
config_gitea_minio()

print("-------------start gitea-------------") 
run_command(f"sudo docker compose -f {os.getenv('COMPOSE_PATH')} up -d gitea")

print("-------------start Nginx Proxy-------------") 
run_command(f"sudo docker compose -f {os.getenv('COMPOSE_PATH')} up -d npm db")

