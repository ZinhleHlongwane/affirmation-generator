from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class AffirmationGeneratedEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str = "affirmation.generated"
    affirmation_id: int
    name: str | None = None
    mood: str | None = None
    goal: str | None = None
    category: str
    tone: str
    source: str
    affirmation: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
