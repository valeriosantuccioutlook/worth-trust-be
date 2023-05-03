import uvicorn
from fastapi import FastAPI

from app.v1.main import app

worthtrust = FastAPI(
    title="Worth Trust APIs",
    description="Worth Trust",
    version="1.0.0",
)
worthtrust.mount("/v1", app)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, root_path="")
