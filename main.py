import json
import platform
import os
import shutil
from pathlib import Path

def bytes_to_gb(value):
    return round(value / (1024 ** 3), 2)

def collect_common_info():
    system = platform.uname()
    logical_cores = os.cpu_count()

    if logical_cores is None:
        raise RuntimeError("Unable to determine the number of logical cores.")

    disk = shutil.disk_usage(Path.cwd().anchor)

    return {
        "system": {
            "name": system.system,
            "hostname":system.node,
            "kernel_release": system.release,
            "kernel_version": system.version,
            "architexture": system.machine,
        },

        "processor": {
            "logical_cores": logical_cores,
        },

        "disk": {
            "total_gb": bytes_to_gb(disk.total),
            "free_gb": bytes_to_gb(disk.free),
        },

    }

def collect_memory_unix():
    page_size = os.sysconf("SC_PAGE_SIZE")
    page_count = os.sysconf("SC_PHYS_PAGES")
    return page_size * page_count


def collect_memory_windows():
    # Здесь используется Windows API через ctypes.
    pass


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