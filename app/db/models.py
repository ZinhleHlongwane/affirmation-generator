from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AffirmationEvent(Base):
    __tablename__ = "affirmation_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String(80), nullable=True)
    mood: Mapped[str | None] = mapped_column(String(80), nullable=True)
    goal: Mapped[str | None] = mapped_column(String(300), nullable=True)
    category: Mapped[str] = mapped_column(String(50), index=True)
    tone: Mapped[str] = mapped_column(String(50))
    affirmation: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(30), index=True)
    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        index=True,
    )
