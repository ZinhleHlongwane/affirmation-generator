import pandas as pd

from pipeline.batch_etl import category_metrics, daily_metrics
from pipeline.quality import clean_events


def sample_data():
    return pd.DataFrame(
        [
            {
                "id": 1,
                "category": " Career ",
                "source": "openai",
                "affirmation": "I can keep learning and growing.",
                "rating": 5,
                "created_at": "2026-09-29T10:00:00+00:00",
            },
            {
                "id": 2,
                "category": "UNKNOWN",
                "source": "fallback",
                "affirmation": "I can take the next step.",
                "rating": 4,
                "created_at": "2026-09-29T11:00:00+00:00",
            },
        ]
    )


def test_clean_events():
    clean = clean_events(sample_data())

    assert list(clean["category"]) == ["career", "general"]
    assert len(clean) == 2


def test_gold_metrics():
    clean = clean_events(sample_data())

    daily = daily_metrics(clean)
    categories = category_metrics(clean)

    assert int(daily.iloc[0]["generation_count"]) == 2
    assert int(categories["generation_count"].sum()) == 2
