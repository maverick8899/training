import time
import random
from pathlib import Path
from SMWinservice import SMWinservice
import subprocess
import win32service
import win32serviceutil
import sys

class PythonService(SMWinservice):
    _svc_name_ = "HN212PluginService"
    _svc_display_name_ = "HN212 Plugin Service"
    _svc_description_ = "HN212 Plugin Service"

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False 

    def main(self):
        if self.isrunning: 
            file_path = "D:/Setup/Máy đọc HN212/v1 2024110301/HN212Plugin.Setup.exe" 
            subprocess.run([file_path], check=True) 
            # subprocess.Popen([file_path]) 

    # @classmethod
    # def install(cls): 
    #     win32serviceutil.InstallService(
    #         cls.__class__,
    #         cls._svc_name_,
    #         cls._svc_display_name_,
    #         startType=win32service.SERVICE_AUTO_START
    #     )
    #     print(f"Service {cls._svc_name_} installed and set to auto start.")


if __name__ == '__main__':
    action = sys.argv[1] if len(sys.argv) > 1 else None
    
    # if action == "install":
    #     PythonService.install()
    # else:
    PythonService.parse_command_line()