from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(
    title="TikTok Video Generator API",
    description="API pour générer des vidéos TikTok à partir d'un concept",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")