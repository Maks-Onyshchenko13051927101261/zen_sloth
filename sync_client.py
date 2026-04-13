import os
import requests

SERVER_URL = "http://127.0.0.1:8000"
SOURCE_DIR = "./my_data"

def start_sync():
    if not os.path.exists(SOURCE_DIR):
        os.makedirs(SOURCE_DIR)
        print(f"📁 Папка {SOURCE_DIR} була порожня. Поклади туди файл!")
        return

    print("🛰️ Скануємо сервер...")
    try:
        map_res = requests.get(f"{SERVER_URL}/sync/map")
        server_map = map_res.json()
    except:
        print("❌ Сервер спить. Запусти uvicorn!")
        return

    for root, _, files in os.walk(SOURCE_DIR):
        for name in files:
            full_path = os.path.join(root, name)
            rel_path = os.path.relpath(full_path, SOURCE_DIR)

            # Пушимо тільки якщо файл новий
            if rel_path not in server_map:
                print(f"🚀 Пушимо: {rel_path}")
                with open(full_path, "rb") as f:
                    requests.post(
                        f"{SERVER_URL}/sync/push", 
                        files={"file": f},
                        headers={"rel-path": rel_path}
                    )
            else:
                print(f"✅ Вже є: {rel_path}")

if __name__ == "__main__":
    start_sync()