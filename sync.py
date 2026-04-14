import requests
import os
import sys
from sloth.core.config import Config
from sloth.core.metadata import Metadata

SERVER_URL = Config.REMOTE_URL 

def push_to_phone():
    print(f"📤 Вивантаження файлів на телефон: {SERVER_URL}")
    local_map = Metadata.scan_storage(Config.FILES_DIR)
    
    for filename in local_map:
        print(f"🚀 Відправляю: {filename}")
        file_path = Config.FILES_DIR / filename
        
        with open(file_path, "rb") as f:
            files = {"file": (filename, f)}
            try:
                res = requests.post(f"{SERVER_URL}/sync/push", files=files, timeout=15)
                res.raise_for_status()
            except Exception as e:
                print(f"❌ Помилка при відправці {filename}: {e}")

def pull_from_phone():
    print(f"📡 Синхронізація з телефоном (PULL)...")
    try:
        response = requests.get(f"{SERVER_URL}/sync/map", timeout=5)
        remote_map = response.json()
        local_map = Metadata.scan_storage(Config.FILES_DIR)
        
        for filename, remote_hash in remote_map.items():
            if filename not in local_map or local_map[filename] != remote_hash:
                print(f"📥 Тягну оновлення: {filename}")
                file_res = requests.get(f"{SERVER_URL}/sync/pull/{filename}")
                target_path = Config.FILES_DIR / filename
                target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(target_path, "wb") as f:
                    f.write(file_res.content)
    except Exception as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "push":
            push_to_phone()
        elif sys.argv[1] == "pull":
            pull_from_phone()
    else:
        print("💡 Використовуй: python sync.py push АБО python sync.py pull")
