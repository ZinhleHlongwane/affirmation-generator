from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


Category = Literal[
    "career",
    "confidence",
    "learning",
    "focus",
    "wellbeing",
    "relationships",
    "general",
]

Tone = Literal[
    "encouraging",
    "calm",
    "bold",
    "gentle",
    "kawaii",
]


class AffirmationRequest(BaseModel):
    name: str | None = Field(default=None, max_length=80)
    mood: str | None = Field(default=None, max_length=80)
    goal: str | None = Field(default=None, max_length=300)
    category: Category = "general"
    tone: Tone = "encouraging"

    @field_validator("name", "mood", "goal")
    @classmethod
    def clean_text(cls, value: str | None):
        if value is None:
            return None
        value = value.strip()
        return value or None


class AffirmationResponse(BaseModel):
    id: int
    affirmation: str
    category: str
    tone: str
    source: str
    created_at: datetime

    model_config = {"from_attributes": True}


class FeedbackRequest(BaseModel):
    rating: float = Field(ge=1, le=5)


class AnalyticsSummary(BaseModel):
    total_generations: int
    ai_generations: int
    fallback_generations: int
    average_rating: float | None
    top_category: str | None
