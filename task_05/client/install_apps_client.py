import os
import shutil
from pathlib import Path
import subprocess
import re
import glob 
import threading
import win32com.client
import win32serviceutil
import win32service
import win32event
import win32api
import win32con
import zipfile
import sys
import requests
import logging

file_exe_pattern = r".*\.exe$"
repo_url = "http://gitea.local/kimbang/new_kiosk"
setup_folder_path = "C:/new_kiosk_"
log_file_path = 'C:/app.log'
telegram_api = 'https://api.telegram.org/bot7758334928:AAEM-PqCzWFn7M_11dcS5Xlev9PS1lgDJNo/sendDocument'

kiosk_folder_path = Path("C:/KIOSKService")
api_folder_path = kiosk_folder_path / "API"
medipay_folder_path = kiosk_folder_path / "MediPay"

setup_folder_path = Path("C:/new_kiosk_")
api_local_folder_path = setup_folder_path / "API_HN212/API_HN212"
medipayApp_folder_path = setup_folder_path / "MediPay_App/MediPay_App"
cccd_setup_folder_path = setup_folder_path / "App_HN212/App_HN212"
cccd_folder_path = setup_folder_path / str(Path.home()) / "AppData/Local/Programs/HN212 Plugin/"
redist_setup_path = setup_folder_path / "Support_Exe/Support_Exe"
printer_folder_path = setup_folder_path / "Printer_w80/Printer_w80"
regedit_file_path = setup_folder_path / "Regedit/config-kioskId.txt"
medipay_updater_folder_path = setup_folder_path / "MediPay_Updater/MediPay_Updater"

# setup_folder_path = Path("C:/Setup")
# api_local_folder_path = setup_folder_path / "API HN212/final/API v1.1.20241104"
# medipayApp_folder_path = setup_folder_path / "MediPay App/Bệnh viện final public/v0.1.202411141 (UAT)"
# cccd_setup_folder_path = setup_folder_path / "HN212 reader machine/v1 2024110301"
# redist_setup_path = setup_folder_path / "Support Exe"
# printer_folder_path = setup_folder_path / "Printer w80/v1 20240830"
# regedit_file_path = setup_folder_path / "Regedit/config-kioskId.txt"
# medipay_updater_folder_path = setup_folder_path / "MediPay Updater"

paths = [api_local_folder_path, medipayApp_folder_path, cccd_setup_folder_path, redist_setup_path, printer_folder_path, regedit_file_path]

def setup_logger(log_file, log_level=logging.INFO):
    """
    Set up a logger to write logs to a file.
    
    :param log_file: The path to the log file.
    :param log_level: The log level (default is logging.INFO).
    :return: Configured logger.
    """
    # Define log format
    log_format = '%(asctime)s - %(levelname)s - %(message)s'

    # Configure the logger
    logging.basicConfig(
        filename=log_file,       # Log file path
        level=log_level,         # Log level (e.g., INFO, WARNING, ERROR)
        format=log_format,       # Log format
        filemode='a',
        datefmt='%D-%H:%M:%S'             # File mode (a: append, w: overwrite)
    )

    return logging.getLogger()

logger = setup_logger(log_file_path)

def run_command(command, daemon=False, return_output=False):
    """Run a shell command and log the output."""
    try:
        if daemon:
            logger.info("Run in daemon mode")
            print("Run in daemon mode")
            result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if return_output :
            return result.stdout.strip()
        else:
            logger.info(result.stdout.strip())
            print(result.stdout.strip())

        if result.returncode != 0:
            logger.info(f"Error: {result.stderr.strip()}")
            print(f"Error: {result.stderr.strip()}")
        return result.returncode
    except Exception as e:
        logger.info(f"Failed to run command '{command}': {e}")
        print(f"Failed to run command '{command}': {e}")
        return 1 
def check_files_in_folder(folder_path, filenames): 
    result = {}
    for filename in filenames:
        file_path = os.path.join(folder_path, filename)
        result[filename] = os.path.isfile(file_path)  # Check if it's a file
    return result

def fetch_extract_repo(repo_url,setup_folder_path):
    logger.info(f"Cloning repository from {repo_url} into {setup_folder_path}...")
    print(f"Cloning repository from {repo_url} into {setup_folder_path}...")
    if os.path.exists(setup_folder_path):
        os.chdir(setup_folder_path)
        logger.info(f"Current working directory: {os.getcwd()}")
        print(f"Current working directory: {os.getcwd()}")
        output = run_command("git pull",return_output=True) 
        if "Already up to date." == output:
            logger.info("Repository is already up to date. Exiting script.")
            print("Repository is already up to date. Exiting script.")
    else:
        run_command(f"git clone {repo_url} {setup_folder_path}") 

    logger.info("Extracting ZIP files in the directory...")
    print("Extracting ZIP files in the directory...")
    for root, _, files in os.walk(setup_folder_path):
        for file in files:
            if file.endswith(".zip"):
                zip_path = os.path.join(root, file)
                extract_to = os.path.join(root, os.path.splitext(file)[0])
                os.makedirs(extract_to, exist_ok=True)
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_to)
                        logger.info(f"Extracted: {zip_path} -> {extract_to}")
                        print(f"Extracted: {zip_path} -> {extract_to}")
                except zipfile.BadZipFile:
                    logger.info(f"Error: {zip_path} is not a valid ZIP file.")
                    print(f"Error: {zip_path} is not a valid ZIP file.")
    logger.info("Done.")
    print("Done.")

fetch_extract_repo(repo_url,setup_folder_path)

def find_file(parent_path="C:/Setup/Support Exe", pattern="*"):
    for file in glob.glob(os.path.join(parent_path, '*')):
        if re.search(pattern, os.path.basename(file)):   
            file = os.path.normpath(file) 
            return file
 
logger.info("=============== Check path is existing =================")
print("=============== Check path is existing =================")
for path in paths:
    logger.info(f"Path '{path}' {'--- EXISTS' if os.path.exists(path) else '--- DOES NOT EXIST'}.")
    print(f"Path '{path}' {'--- EXISTS' if os.path.exists(path) else '--- DOES NOT EXIST'}.")

logger.info("=============== Create folders 'KIOSKService', 'API', and 'MediPay' =================")
print("=============== Create folders 'KIOSKService', 'API', and 'MediPay' =================")
kiosk_folder_path.mkdir(parents=True, exist_ok=True)
api_folder_path.mkdir(exist_ok=True)
medipay_folder_path.mkdir(exist_ok=True)

logger.info("=============== copy API files to the 'API' folder. =================")
print("=============== copy API files to the 'API' folder. =================")
api_source_folder = setup_folder_path / api_local_folder_path
shutil.copytree(api_source_folder, api_folder_path, dirs_exist_ok=True)

logger.info("=============== copy MediPay App files to the 'MediPay' folder. =================")
print("=============== copy MediPay App files to the 'MediPay' folder. =================")
medipay_source_folder = setup_folder_path / medipayApp_folder_path  
shutil.copytree(medipay_source_folder, medipay_folder_path, dirs_exist_ok=True)

cccd_setup_bin_path = find_file(cccd_setup_folder_path,file_exe_pattern)
logger.info(f"\n=============== Install CCCD Reader App: {cccd_setup_bin_path} =================")
print(f"\n=============== Install CCCD Reader App: {cccd_setup_bin_path} =================")
# threading.Thread(target=run_command  , args=(str(cccd_setup_bin_path),)).start() #>
run_command(str(cccd_setup_bin_path))

redist_setup_bin_path = find_file(redist_setup_path,file_exe_pattern)
logger.info(f"\n=============== Install VC_redist: {redist_setup_bin_path} =================")
print(f"\n=============== Install VC_redist: {redist_setup_bin_path} =================")
# threading.Thread(target=run_command  , args=(str(redist_setup_bin_path),)).start() #>
run_command(str(redist_setup_bin_path))

medipay_updater_bin_path = find_file(medipay_updater_folder_path,file_exe_pattern)
logger.info(f"\n=============== Install medipay updater: {medipay_updater_folder_path} =================")
print(f"\n=============== Install medipay updater: {medipay_updater_folder_path} =================")
# threading.Thread(target=run_command  , args=(str(medipay_updater_bin_path), True,)).start() #>
run_command(str(medipay_updater_bin_path))

logger.info("=============== Check if printer w80 is already installed or not =================")
print("=============== Check if printer w80 is already installed or not =================")
printer_name = "w80" 
printers = subprocess.run(["wmic", "printer", "get", "name"], capture_output=True, text=True)
if printer_name not in printers.stdout:
    logger.info(" Printer w80 is not installed yet. Installing...")
    print(" Printer w80 is not installed yet. Installing...")
    run_command([str(printer_folder_path / "Uninstaller.exe")]) #>
    run_command([str(printer_folder_path / "PrinterInstall.exe")]) #>
else:
    logger.info("Printer w80 is already installed. ")
    print("Printer w80 is already installed. ")

logger.info("================= Config KioskId. =================")
print("================= Config KioskId. =================")
with open(regedit_file_path) as file:
    kioskId_command = file.read()
    # print(kioskId_command)
try:
    result = subprocess.run(["powershell", "-Command", kioskId_command], capture_output=True, text=True, check=True) #>
    print("Output:")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("Error:", e.stderr)

#? Enable auto-start for MediPay, HN212 and API
startup_folder = Path(os.getenv("APPDATA")) / "Microsoft/Windows/Start Menu/Programs/Startup" 
def create_shortcut(target, shortcut_name):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(str(startup_folder / f"{shortcut_name}.lnk"))
    shortcut.TargetPath = str(target)
    shortcut.save()

logger.info("================= Config auto-start configuration for MediPay, HN212 and API ================= ")
print("================= Config auto-start configuration for MediPay, HN212 and API ================= ")
medipay_bin_path = find_file(medipay_folder_path, file_exe_pattern)
api_bin_path = find_file(api_folder_path, file_exe_pattern)
cccd_bin_path = find_file(cccd_folder_path, file_exe_pattern)

create_shortcut(medipay_bin_path, "MediPay")
create_shortcut(api_bin_path, "API")
create_shortcut(cccd_bin_path, "HN212")

filenames = ["MediPay.lnk", "API.lnk", "HN212.lnk"] 
check_result = check_files_in_folder(startup_folder, filenames)

for filename, exists in check_result.items():
    if exists:
        logger.info(f"Create {filename} shortcut successfully.")
        print(f"Create {filename} shortcut successfully.")
    else:
        logger.info(f"Creating {filename} shortcut failed.")
        print(f"Create {filename} shortcut failed.")

#@ Send log to telegram
files = {
    'chat_id': (None, '-4583989930'),
    'document': open(log_file_path, 'rb'),
}
response = requests.post(telegram_api,
    files=files,
)
print("Send log to telegram: ",response.status_code, response.text) 