from fastapi import FastAPI

from app import models
from app.auth.routes import router as auth_router
from app.chat.routes import router as chat_router
from app.database import Base, engine
from app.metrics import router as metrics_router


app = FastAPI(
    title="AI/LLM Platform API",
    version="1.0.0",
)


Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(metrics_router)


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }