from fastapi import FastAPI
from app.api.casts import router

app = FastAPI(title="Cast Service", version="1.0.0", docs_url="/api/v1/casts/docs", openapi_url="/api/v1/casts/openapi.json")

@app.get("/")
async def root():
    return {"service": "cast-service", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

app.include_router(router, prefix='/api/v1/casts', tags=['casts'])
