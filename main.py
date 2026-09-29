import json
import platform
import os
import shutil
from pathlib import Path

def bytes_to_gb(value):
    return round(value / (1024 ** 3), 2)

operating_system = platform.system()

if operating_system == "Windows":
    print("Программа запущена на Windows")
elif operating_system == "Linux":
    print("Программа запущена на Linux")
elif operating_system == "Darwin":
    print("Программа запущена на macOS")

system = platform.uname()

print("Version: ", system.version) #Версия операционной системы
print("Hostname: ", system.node) #Название хоста, имя компьютера
print("Architecture: ", system.machine) #Архитектура процессора

logical_cores = os.cpu_count()
print("Logical cores: ", logical_cores) #Количество логических ядер процессора

disk = shutil.disk_usage(Path.cwd().anchor)
print("Total disk space: ", bytes_to_gb(disk.total), "GB") #Общий размер диска
print("Used disk space: ", bytes_to_gb(disk.used), "GB") #Используемый размер диска
print("Free disk space: ", bytes_to_gb(disk.free), "GB") #Свободный размер диска

