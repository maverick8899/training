from pathlib import Path

#"http://gitea.local/api/v1/repos/kimbang/script/tags"
GIT_KIOSK_TAG_API = "https://api.github.com/repos/GoTRUST-BangTK/kiosk/tags" 
KIOSK_REPO_URL = "https://github.com/GoTRUST-BangTK/kiosk.git"
TELEGRAM_API = 'https://api.telegram.org/bot7758334928:AAEM-PqCzWFn7M_11dcS5Xlev9PS1lgDJNo/sendDocument'

GIT_REPO_DIR = "script"
REGISTRY_PATH = r"SOFTWARE\AutoUpgrade"
TIME_INTERVAL = 5
SETUP_FOLDER_PATH = "C:/kiosk"
LOG_FILE_PATH = 'C:/app.log'

KIOSK_FOLDER_PATH = Path("C:/KIOSKService")
API_FOLDER_PATH = KIOSK_FOLDER_PATH / "API"
MEDIPAY_FOLDER_PATH = KIOSK_FOLDER_PATH / "MediPay"

API_LOCAL_FOLDER_PATH = SETUP_FOLDER_PATH / "API_HN212/API_HN212"
MEDIPAYAPP_FOLDER_PATH = SETUP_FOLDER_PATH / "MediPay_App/MediPay_App"
CCCD_SETUP_FOLDER_PATH = SETUP_FOLDER_PATH / "App_HN212/App_HN212"
CCCD_FOLDER_PATH = SETUP_FOLDER_PATH / str(Path.home()) / "AppData/Local/Programs/HN212 Plugin/"
REDIST_SETUP_PATH = SETUP_FOLDER_PATH / "Support_Exe/Support_Exe"
PRINTER_FOLDER_PATH = SETUP_FOLDER_PATH / "Printer_w80/Printer_w80"
REGEDIT_FILE_PATH = SETUP_FOLDER_PATH / "Regedit/config-kioskId.txt"
MEDIPAY_UPDATER_FOLDER_PATH = SETUP_FOLDER_PATH / "MediPay_Updater/MediPay_Updater"
