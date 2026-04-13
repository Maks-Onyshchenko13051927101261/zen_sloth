from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks, Header;
from fastapi.middleware.cors import CORSMiddleware;
import os, shutil;

from sloth.core import Metadata, Storage, PluginManager, JobManager;

app = FastAPI(title="ZenSloth Micro-PaaS");

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
);

BASE_DIR = os.path.abspath("./storage/files");
storage = Storage(BASE_DIR);
plugins = PluginManager("./plugins");
jobs = JobManager();

STORAGE_STRUCTURE = ["files", "projects", "logs", "db"];
for folder in STORAGE_STRUCTURE:
    os.makedirs(os.path.join("./storage", folder), exist_ok=True);

@app.get("/")
def root():
    return {"system": "ZenSloth OS", "status": "alive"};


@app.get("/files")
def list_files():
    return storage.list_files();


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    return storage.save(file);


@app.get("/file/{name}")
def get_file(name: str):
    return storage.get(name);


@app.delete("/file/{name}")
def delete_file(name: str):
    return storage.delete(name);


# 🧠 PLUGINS (серце системи)
@app.post("/run/{plugin_name}")
def run_plugin(plugin_name: str):
    return plugins.run(plugin_name);


# ⚙️ JOBS
@app.post("/jobs/{job_name}")
def run_job(job_name: str, background: BackgroundTasks):
    return jobs.run(job_name, background_tasks);

@app.get("/sync/map")
def get_sync_map():
    return Metadata.scan_storage(BASE_DIR)

@app.post("/sync/push")
async def sync_push(
    file: UploadFile = File(...), 
    rel_path: str = Header(...)
):
    from core.security import Security
    target_path = Security.get_safe_path(BASE_DIR, rel_path)
    
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    
    with open(target_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"status": "synced", "path": rel_path};

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000);

# Host	Що означає
# 0.0.0.0	сервер слухає всі IP
# 127.0.0.1	localhost
# 192.168.x.x	твій телефон у мережі