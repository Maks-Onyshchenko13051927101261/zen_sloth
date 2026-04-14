import os
import shutil
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sloth.core.config import Config
from sloth.core.metadata import Metadata 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ZenSloth Storage Node")

@app.get("/sync/map")
def get_map():
    return Metadata.scan_storage(Config.FILES_DIR)

@app.get("/sync/pull/{filename}")
def pull_file(filename: str):
    file_path = Config.FILES_DIR / filename
    if file_path.exists():
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Файл заблукав у цифровій пустці")

@app.post("/sync/push")
async def push_file(file: UploadFile = File(...)):
    file_path = Config.FILES_DIR / file.filename
    try:
        with file_path.open("wb") as buffer:
            content = await file.read()
            buffer.write(content)
        return {"status": "success", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ping")
def ping():
    return {"status": "alive", "node": os.getenv("ZEN_ENV", "dev")};

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
async def get_status():
    return {"status": "online", "system": "sloth"}

@app.get("/system/storage")
async def get_storage():
    total, used, free = shutil.disk_usage("/") 
    
    percent = round((used / total) * 100)
    return {
        "total": round(total / (1024**3), 1), # в ГБ
        "free": round(free / (1024**3), 1),   # в ГБ
        "percent": percent
    }