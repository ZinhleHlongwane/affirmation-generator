from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db.database import get_db
from app.schemas import (
    AffirmationRequest,
    AffirmationResponse,
    AnalyticsSummary,
    FeedbackRequest,
)
from app.services.affirmation_service import AffirmationService

router = APIRouter(prefix="/api/v1")


def get_service(
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> AffirmationService:
    return AffirmationService(db, settings)


@router.post(
    "/affirmations/generate",
    response_model=AffirmationResponse,
    status_code=201,
)
def generate_affirmation(
    payload: AffirmationRequest,
    service: AffirmationService = Depends(get_service),
):
    return service.generate(payload)


@router.get(
    "/affirmations/history",
    response_model=list[AffirmationResponse],
)
def affirmation_history(
    limit: int = Query(default=20, ge=1, le=100),
    service: AffirmationService = Depends(get_service),
):
    return service.history(limit)


@router.post(
    "/affirmations/{record_id}/feedback",
    response_model=AffirmationResponse,
)
def add_feedback(
    record_id: int,
    payload: FeedbackRequest,
    service: AffirmationService = Depends(get_service),
):
    record = service.add_feedback(record_id, payload.rating)
    if record is None:
        raise HTTPException(status_code=404, detail="Affirmation not found.")
    return record


@router.get(
    "/analytics/summary",
    response_model=AnalyticsSummary,
)
def analytics_summary(
    service: AffirmationService = Depends(get_service),
):
    return service.analytics_summary()
