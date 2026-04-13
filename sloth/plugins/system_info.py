import platform
import shutil

def run():
    total, used, free = shutil.disk_usage("/")
    return {
        "os": platform.system(),
        "node": platform.node(),
        "free_gb": free // (2**30)
    }