import os
from pathlib import Path

TEST_DB = Path("test_affirmations.db")

os.environ["DATABASE_URL"] = f"sqlite:///./{TEST_DB}"
os.environ["AI_ENABLED"] = "false"
os.environ["KAFKA_ENABLED"] = "false"
os.environ["OPENAI_API_KEY"] = ""

from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402


client = TestClient(app)


def teardown_module():
    from app.db.database import engine

    engine.dispose()

    if TEST_DB.exists():
        TEST_DB.unlink()


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_affirmation():
    response = client.post(
        "/api/v1/affirmations/generate",
        json={
            "name": "Zinhle",
            "mood": "nervous",
            "goal": "prepare for a data engineering interview",
            "category": "career",
            "tone": "encouraging",
        },
    )

    assert response.status_code == 201

    payload = response.json()

    assert payload["category"] == "career"
    assert payload["source"] == "fallback"
    assert payload["affirmation"]
