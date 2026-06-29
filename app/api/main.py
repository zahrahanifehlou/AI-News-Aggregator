from fastapi import FastAPI
from app.services.pipeline import run_news_pipeline

app = FastAPI()


@app.get("/")
def home():
    return {"status": "ok"}


@app.get("/run-pipeline")
def run_pipeline():

    processed = run_news_pipeline()

    return {
        "count": len(processed),
        "articles": [
            {
                "title": a.title,
                "score": a.score,
                "categories": a.categories,
                "summary": a.summary
            }
            for a in processed
        ]
    }