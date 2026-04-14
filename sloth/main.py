import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sloth.core.config import Config
from sloth.core.metadata import Metadata 

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
    return {"status": "alive", "node": os.getenv("ZEN_ENV", "dev")}