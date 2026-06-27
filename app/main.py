from fastapi import FastAPI
from app.tasks.celery_app import app as celery_app
from app.api.books import router as books_router

app = FastAPI(title="Book Recommender")

app.include_router(books_router)


@app.get("/health")
async def health():
    celery_status = celery_app.control.ping(timeout=1.0)
    return {
        "status": "ok",
        "celery": "up" if celery_status else "down"
    }