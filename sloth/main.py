import os;
import shutil;
from fastapi import FastAPI, HTTPException, File, UploadFile;
from fastapi.middleware.cors import CORSMiddleware;
from fastapi.responses import FileResponse;

app = FastAPI();
BASE_DIR = os.path.abspath("./storage");

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR);

def get_safe_path(filename: str):
    target_path = os.path.abspath(os.path.join(BASE_DIR, filename));
    if not target_path.startswith(BASE_DIR):
        raise HTTPException(status_code=403, detail="Доступ заборонено: спроба виходу за межі сховища");
    return target_path;

#Повертає список файлів у папці storage
@app.get("/files")
async def list_files():
    try:
        files = os.listdir(BASE_DIR);
        return {
            "count": len(files),
            "files": files
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e));

#Приймає файл і зберігає його в BASE_DIR
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = get_safe_path(file.filename);
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer);
    return {"message": f"Файл {file.filename} успішно завантажено", "status": "saved"};

#Знаходить файл і віддає його (для скачування або перегляду)
@app.get("/file/{filename}")
async def get_file(filename: str):
    file_path = get_safe_path(filename);
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не знайдено");
    return FileResponse(path=file_path, filename=filename);

# Дозволяємо PWA звертатися до сервера
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
);

@app.get("/")
async def root():
    return {
        "message": "Welcome to ZenSloth OS Server! 🦥", "status": "Vibing"
    };

# Статус-ендпоінт для терміналу
@app.get("/status")
async def get_status():
    return {
        "system": "ZEN_SLOTH",
        "version": "1.0.0",
        "environment": "WSL_DEVELOPMENT",
        "developer": "Python_Dev_Reserve"
    };

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True);