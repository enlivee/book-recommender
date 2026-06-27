from fastapi import FastAPI

app = FastAPI(title='Book Recommender')

@app.get("/health")
async def health():
    return {"status": "ok"}