import requests
import config
import random
import string
import os
import sys

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

accessKey=generate_random_string(20)
secretKey=generate_random_string(40)
bucket_name = sys.argv[1] if len(sys.argv) > 1 else "bucket"

def execute():
    session = requests.Session()
    
    cookies = { 
        '_csrf': config.CSRF,
    }
    headers = { 
        'Content-Type': 'application/json'
    }
    json_data = {
        'accessKey': config.MINIO_ROOT_USER,
        'secretKey': config.MINIO_ROOT_PASSWORD,
    }

    #? store persistent cookie for the next request by remain alive session
    response = session.post(f"{config.MINIO_URL}/api/v1/login", cookies=cookies, headers=headers, json=json_data, verify=False)
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
        f"{config.MINIO_URL}/api/v1/service-account-credentials",
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
    response = session.post(f"{config.MINIO_URL}/api/v1/buckets", cookies=cookies, headers=headers, json=json_data)
    print("Create bucket: ",response.status_code, response.text) 

#? Create app.init
    content = f"""[storage]
STORAGE_TYPE = minio   
MINIO_ENDPOINT = {config.MINIO_ENDPOINT}
MINIO_ACCESS_KEY_ID = {accessKey}
MINIO_SECRET_ACCESS_KEY = {secretKey}
MINIO_BUCKET = {bucket_name}
MINIO_USE_SSL = {config.MINIO_USE_SSL} """
    
    os.makedirs(config.GITEA_CONFIG, exist_ok=True)
    with open(f"{config.GITEA_CONFIG}/app.ini", "w") as file:
        file.write(content)

execute()     
