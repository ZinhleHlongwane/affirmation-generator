import pandas as pd

VALID_CATEGORIES = {
    "career",
    "confidence",
    "learning",
    "focus",
    "wellbeing",
    "relationships",
    "general",
}


def clean_events(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    clean = df.copy()

    clean["category"] = (
        clean["category"]
        .fillna("general")
        .astype(str)
        .str.strip()
        .str.lower()
    )
    clean.loc[~clean["category"].isin(VALID_CATEGORIES), "category"] = "general"

    clean["source"] = (
        clean["source"]
        .fillna("fallback")
        .astype(str)
        .str.strip()
        .str.lower()
    )
    clean.loc[~clean["source"].isin({"openai", "fallback"}), "source"] = "fallback"

    clean["affirmation"] = clean["affirmation"].fillna("").astype(str).str.strip()
    clean = clean[clean["affirmation"].str.len() >= 5]

    clean["created_at"] = pd.to_datetime(
        clean["created_at"],
        errors="coerce",
        utc=True,
    )
    clean = clean.dropna(subset=["created_at"])

    clean["event_date"] = clean["created_at"].dt.date.astype(str)

    if "rating" in clean.columns:
        clean["rating"] = pd.to_numeric(clean["rating"], errors="coerce")
        clean.loc[~clean["rating"].between(1, 5, inclusive="both"), "rating"] = pd.NA

    return clean
