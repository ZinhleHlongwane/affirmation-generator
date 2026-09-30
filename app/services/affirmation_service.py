from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.db.models import AffirmationEvent
from app.events.factory import create_event_publisher
from app.events.models import AffirmationGeneratedEvent
from app.schemas import AffirmationRequest
from app.services.ai_service import AffirmationAIService


class AffirmationService:
    def __init__(self, db: Session, settings: Settings):
        self.db = db
        self.settings = settings
        self.ai = AffirmationAIService(settings)

    def generate(self, payload: AffirmationRequest) -> AffirmationEvent:
        result = self.ai.generate(
            name=payload.name,
            mood=payload.mood,
            goal=payload.goal,
            category=payload.category,
            tone=payload.tone,
        )

        record = AffirmationEvent(
            name=payload.name,
            mood=payload.mood,
            goal=payload.goal,
            category=payload.category,
            tone=payload.tone,
            affirmation=result.text,
            source=result.source,
            model_name=result.model_name,
        )

        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        event = AffirmationGeneratedEvent(
            affirmation_id=record.id,
            name=record.name,
            mood=record.mood,
            goal=record.goal,
            category=record.category,
            tone=record.tone,
            source=record.source,
            affirmation=record.affirmation,
            created_at=record.created_at,
        )

        try:
            publisher = create_event_publisher(self.settings)
            publisher.publish(event)
        except Exception:
            # Keep the synchronous API available if Kafka is temporarily down.
            # A production version would use a transactional outbox + retry worker.
            pass

        return record

    def history(self, limit: int = 20) -> list[AffirmationEvent]:
        stmt = (
            select(AffirmationEvent)
            .order_by(AffirmationEvent.created_at.desc())
            .limit(limit)
        )
        return list(self.db.scalars(stmt))

    def add_feedback(self, record_id: int, rating: float) -> AffirmationEvent | None:
        record = self.db.get(AffirmationEvent, record_id)
        if record is None:
            return None

        record.rating = rating
        self.db.commit()
        self.db.refresh(record)
        return record

    def analytics_summary(self) -> dict:
        total = self.db.scalar(select(func.count(AffirmationEvent.id))) or 0
        ai_count = self.db.scalar(
            select(func.count(AffirmationEvent.id)).where(AffirmationEvent.source == "openai")
        ) or 0
        fallback_count = self.db.scalar(
            select(func.count(AffirmationEvent.id)).where(AffirmationEvent.source == "fallback")
        ) or 0
        average_rating = self.db.scalar(select(func.avg(AffirmationEvent.rating)))

        top = self.db.execute(
            select(
                AffirmationEvent.category,
                func.count(AffirmationEvent.id).label("count"),
            )
            .group_by(AffirmationEvent.category)
            .order_by(func.count(AffirmationEvent.id).desc())
            .limit(1)
        ).first()

        return {
            "total_generations": int(total),
            "ai_generations": int(ai_count),
            "fallback_generations": int(fallback_count),
            "average_rating": round(float(average_rating), 2) if average_rating else None,
            "top_category": top[0] if top else None,
        }
