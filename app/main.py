# app/main.py

from fastapi import FastAPI
from .api import router

app = FastAPI(
    title="AIModels API",
    version="1.0.0"
)

# API endpoint sotto /API
app.include_router(router, prefix="/api")