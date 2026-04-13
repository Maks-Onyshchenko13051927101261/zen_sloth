from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks;
from fastapi.middleware.cors import CORSMiddleware;
import os, shutil;

from core.storage import Storage;
from core.plugins import PluginManager;
from core.jobs import JobManager; 

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