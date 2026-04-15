from fastapi import FastAPI
from app.api.movies import router

app = FastAPI(title="Movie Service", version="1.0.0", docs_url="/api/v1/movies/docs", openapi_url="/api/v1/movies/openapi.json")

@app.get("/")
async def root():
    return {"service": "movie-service", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

app.include_router(router, prefix='/api/v1/movies', tags=['movies'])
