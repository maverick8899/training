import os
import win32serviceutil
import win32service
import win32event
import win32api
import win32con
import subprocess
import sys

class PythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = "HN212PluginService"  # Tên service
    _svc_display_name_ = "HN212 Plugin Service"  # Tên hiển thị của service
    _svc_description_ = "Service to run the HN212 Plugin "  # Mô tả service

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args or [])
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        # Khi service dừng, gọi hàm này
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        # Hàm chạy khi service bắt đầu
        # Thực thi file .exe của bạn (HN212Plugin.Setup.exe)
        file_path = "D:/Setup/Máy đọc HN212/v1 2024110301/HN212Plugin.Setup.exe"
        
        # Chạy file .exe với subprocess
        subprocess.run([file_path], check=True)
        
        # Khi service bắt đầu, sẽ chạy file .exe
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)


def install_service():
    win32serviceutil.InstallService(
        "PythonService",  # Class service
        "HN212PluginService",  # Tên service
        "HN212 Plugin Service",  # Tên hiển thị
        startType=win32service.SERVICE_DEMAND_START  # Chế độ manual (chạy khi gọi)
    )
    print("Service installed successfully.")

# Gỡ bỏ service
def remove_service():
    win32serviceutil.RemoveService("HN212PluginService")
    print("Service removed successfully.")

# Khởi chạy service
def start_service():
    win32serviceutil.StartService("HN212PluginService")
    print("Service started.")

# Dừng service
def stop_service():
    win32serviceutil.StopService("HN212PluginService")
    print("Service stopped.")

# Chạy script
if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else None
    
    if action == "install":
        install_service()
    elif action == "remove":
        remove_service()
    elif action == "start":
        start_service()
    elif action == "stop":
        stop_service()
    else:
        print("Usage: python create_service.py [install|remove|start|stop]")
