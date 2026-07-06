# app/api/main.py

from fastapi import FastAPI
from app.api.routes import news, pipeline

app = FastAPI(
    title="AI News Pipeline API",
    version="2.0.0"
)

app.include_router(news.router)
app.include_router(pipeline.router)


@app.get("/")
def home():
    return {"status": "ok"}