import json
import platform
import os
import shutil
import ctypes
from ctypes import wintypes
from pathlib import Path
from datetime import datetime

def bytes_to_gb(value):
    return round(value / (1024 ** 3), 2)

def collect_common_info():
    collected_at = datetime.now().astimezone()
    system = platform.uname()
    logical_cores = os.cpu_count()

    if logical_cores is None:
        raise RuntimeError("Unable to determine the number of logical cores.")

    disk = shutil.disk_usage(Path.cwd().anchor)

    return {
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation()
        },
        "system": {
            "name": system.system,
            "hostname":system.node,
            "kernel_release": system.release,
            "kernel_version": system.version,
            "architecture": system.machine,
        },
        "processor": {
            "logical_cores": logical_cores,
        },
        "disk": {
            "total_gb": bytes_to_gb(disk.total),
            "free_gb": bytes_to_gb(disk.free),
        },
        "collection": {
            "date": collected_at.date().isoformat(),
            "time": collected_at.time().isoformat(timespec="seconds"),
            "datetime": collected_at.isoformat(timespec="seconds"),
        }
    }

def collect_memory_unix():
    page_size = os.sysconf("SC_PAGE_SIZE")
    page_count = os.sysconf("SC_PHYS_PAGES")
    return page_size * page_count


def collect_memory_windows():
    class MemoryStatusEx(ctypes.Structure):
        _fields_ = [
            ("dwLength", wintypes.DWORD),
            ("dwMemoryLoad", wintypes.DWORD),
            # DWORDLONG is an unsigned 64-bit integer in the WinAPI.
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    memory_status = MemoryStatusEx()
    memory_status.dwLength = ctypes.sizeof(memory_status)

    global_memory_status_ex = ctypes.windll.kernel32.GlobalMemoryStatusEx
    global_memory_status_ex.argtypes = [ctypes.POINTER(MemoryStatusEx)]
    global_memory_status_ex.restype = wintypes.BOOL

    if not global_memory_status_ex(ctypes.byref(memory_status)):
        raise ctypes.WinError()

    return memory_status.ullTotalPhys


def collect_memory():
    system_name = platform.system()

    if system_name == "Windows":
        return collect_memory_windows()

    if system_name in ("Darwin", "Linux"):
        return collect_memory_unix()

    raise RuntimeError(f"ОС {system_name} не поддерживается")


def main():
    configuration = collect_common_info()
    configuration["memory"] = {
        "total_gb": bytes_to_gb(collect_memory()),
    }

    with open("system_configuration.json", "w", encoding="utf-8") as file:
        json.dump(configuration, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()