import os
from pathlib import Path

class Config:
    BASE_PATH = Path(__file__).parent.parent.parent
    
    STORAGE_DIR = BASE_PATH / "storage"
    FILES_DIR = STORAGE_DIR / "files"
    LOGS_DIR = STORAGE_DIR / "logs"
    DB_DIR = STORAGE_DIR / "db"
    PROJECTS_DIR = STORAGE_DIR / "projects"
    PLUGINS_DIR = BASE_PATH / "plugins"

    HOST = os.getenv("SLOTH_HOST", "0.0.0.0")
    PORT = int(os.getenv("SLOTH_PORT", 8000))
    
    # IP сервера (телефона), куди комп буде стукати
    REMOTE_URL = os.getenv("SLOTH_REMOTE", "http://192.168.137.110:8000")

    @classmethod
    def init_dirs(cls):
        for folder in [cls.FILES_DIR, cls.LOGS_DIR, cls.DB_DIR, cls.PROJECTS_DIR, cls.PLUGINS_DIR]:
            folder.mkdir(parents=True, exist_ok=True)

Config.init_dirs()