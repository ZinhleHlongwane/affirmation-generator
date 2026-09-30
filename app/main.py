from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings
from app.db.database import Base, engine

settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version="3.0.0",
    description="AI affirmation API with Kafka, Spark and AWS data engineering.",
)

app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
        "kafka_enabled": settings.kafka_enabled,
    }
