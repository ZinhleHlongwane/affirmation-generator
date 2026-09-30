from pathlib import Path
import sqlite3

import pandas as pd

from pipeline.quality import clean_events

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "affirmations.db"
LAKE = ROOT / "data" / "lake"
BRONZE = LAKE / "bronze"
SILVER = LAKE / "silver"
GOLD = LAKE / "gold"


def ensure_dirs() -> None:
    for path in (BRONZE, SILVER, GOLD):
        path.mkdir(parents=True, exist_ok=True)


def extract() -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame()

    with sqlite3.connect(DB_PATH) as connection:
        return pd.read_sql_query(
            """
            SELECT
                id,
                name,
                mood,
                goal,
                category,
                tone,
                affirmation,
                source,
                model_name,
                rating,
                created_at
            FROM affirmation_events
            ORDER BY id
            """,
            connection,
        )


def daily_metrics(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(
            columns=[
                "event_date",
                "generation_count",
                "ai_generation_count",
                "fallback_generation_count",
                "average_rating",
            ]
        )

    work = df.assign(
        ai_generation=(df["source"] == "openai").astype(int),
        fallback_generation=(df["source"] == "fallback").astype(int),
    )

    metrics = (
        work.groupby("event_date", as_index=False)
        .agg(
            generation_count=("id", "count"),
            ai_generation_count=("ai_generation", "sum"),
            fallback_generation_count=("fallback_generation", "sum"),
            average_rating=("rating", "mean"),
        )
    )
    metrics["average_rating"] = metrics["average_rating"].round(2)
    return metrics


def category_metrics(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(
            columns=[
                "category",
                "generation_count",
                "ai_generation_count",
                "average_rating",
            ]
        )

    work = df.assign(ai_generation=(df["source"] == "openai").astype(int))

    metrics = (
        work.groupby("category", as_index=False)
        .agg(
            generation_count=("id", "count"),
            ai_generation_count=("ai_generation", "sum"),
            average_rating=("rating", "mean"),
        )
        .sort_values("generation_count", ascending=False)
    )
    metrics["average_rating"] = metrics["average_rating"].round(2)
    return metrics


def run_pipeline() -> dict:
    ensure_dirs()

    raw = extract()
    raw.to_csv(BRONZE / "affirmation_events_raw.csv", index=False)

    clean = clean_events(raw)
    clean.to_csv(SILVER / "affirmation_events_clean.csv", index=False)

    daily = daily_metrics(clean)
    categories = category_metrics(clean)

    daily.to_csv(GOLD / "daily_metrics.csv", index=False)
    categories.to_csv(GOLD / "category_metrics.csv", index=False)

    return {
        "bronze_rows": len(raw),
        "silver_rows": len(clean),
        "gold_daily_rows": len(daily),
        "gold_category_rows": len(categories),
    }


if __name__ == "__main__":
    print(run_pipeline())
