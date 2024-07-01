from fastapi import FastAPI
from src.router import router as bc_router

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.include_router(bc_router)





