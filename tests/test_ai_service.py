from app.core.config import Settings
from app.services.ai_service import AffirmationAIService


def test_fallback_generation_without_api_key():
    settings = Settings(
        ai_enabled=True,
        openai_api_key=None,
        kafka_enabled=False,
    )

    service = AffirmationAIService(settings)

    result = service.generate(
        name="Zinhle",
        mood="focused",
        goal="grow as a data engineer",
        category="career",
        tone="encouraging",
    )

    assert result.source == "fallback"
    assert "Zinhle" in result.text
    assert "grow as a data engineer" in result.text
