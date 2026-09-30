from app.events.models import AffirmationGeneratedEvent


def test_event_schema_serialises():
    event = AffirmationGeneratedEvent(
        affirmation_id=10,
        category="career",
        tone="encouraging",
        source="fallback",
        affirmation="I can keep learning.",
    )

    payload = event.model_dump(mode="json")

    assert payload["event_type"] == "affirmation.generated"
    assert payload["affirmation_id"] == 10
    assert payload["category"] == "career"
    assert payload["event_id"]
