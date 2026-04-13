import os
import shutil
from fastapi import HTTPException

class Storage:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def safe_path(self, name):
        path = os.path.abspath(os.path.join(self.base_dir, name))
        if not path.startswith(self.base_dir):
            raise HTTPException(403, "Forbidden path")
        return path

    def list_files(self):
        return os.listdir(self.base_dir)

    def save(self, file):
        path = self.safe_path(file.filename)
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        return {"saved": file.filename}

    def get(self, name):
        path = self.safe_path(name)
        if not os.path.exists(path):
            raise HTTPException(404, "Not found")
        return {"file": name, "path": path}

    def delete(self, name):
        path = self.safe_path(name)
        os.remove(path)
        return {"deleted": name}