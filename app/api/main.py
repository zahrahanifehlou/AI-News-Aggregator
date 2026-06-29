from fastapi import FastAPI
from app.services.pipeline import process_news, send_newsletter

app = FastAPI()
latest_news = []



@app.get("/")
def home():
    return {"status": "ok"}


@app.post("/run-pipeline")
def run_pipeline():
    global latest_news
    latest_news = process_news()
    return {"message": "Pipeline completed"}


@app.post("/send_newsletter")
def send_newsletter_endpoint():
    send_newsletter(latest_news)
    return {
        "count": len(latest_news),
        "articles": [
            {
                "title": a.title,
                "score": a.score,
                "categories": a.categories,
                "summary": a.summary
            }
            for a in  latest_news
        ]
    }


@app.get("/news")
def get_news():

    return [
        {
            "title": a.title,
            "score": a.score,
            "categories": a.categories,
            "summary": a.summary
        }
        for a in latest_news
    ]


@app.get("/news/top")
def get_top_news():
    top = latest_news[:5]

    return [
        {
            "title": a.title,
            "score": a.score,
            "summary": a.summary
        }
        for a in top
    ]


@app.get("/news/category/{category}")
def get_by_category(category: str):
    filtered = [
        a for a in latest_news
        if category.lower() in [c.lower() for c in a.categories]
    ]
    return [
        {
            "title": a.title,
            "score": a.score,
            "categories": a.categories,
            "summary": a.summary
        }
        for a in filtered
    ]