import os;
from fastapi import FastAPI;
from fastapi.middleware.cors import CORSMiddleware;
#test
from fastapi.responses import JSONResponse;

app = FastAPI();

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