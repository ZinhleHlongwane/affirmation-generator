from pathlib import Path

import pandas as pd
import requests
import streamlit as st

ROOT = Path(__file__).resolve().parent
GOLD = ROOT / "data" / "lake" / "gold"
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Affirmation Intelligence",
    page_icon="✨",
    layout="wide",
)

st.title("✨ Affirmation Intelligence Platform")
st.caption("AI + Kafka + Spark + AWS data engineering")

generate_tab, analytics_tab = st.tabs(["Generate", "Analytics"])

with generate_tab:
    left, right = st.columns(2)

    with left:
        name = st.text_input("Name")
        mood = st.text_input("Current mood")
        goal = st.text_input("Goal")

        category = st.selectbox(
            "Category",
            [
                "general",
                "career",
                "confidence",
                "learning",
                "focus",
                "wellbeing",
                "relationships",
            ],
        )

        tone = st.selectbox(
            "Tone",
            [
                "encouraging",
                "calm",
                "bold",
                "gentle",
                "kawaii",
            ],
        )

        if st.button("Generate", type="primary"):
            payload = {
                "name": name or None,
                "mood": mood or None,
                "goal": goal or None,
                "category": category,
                "tone": tone,
            }

            try:
                response = requests.post(
                    f"{API_URL}/api/v1/affirmations/generate",
                    json=payload,
                    timeout=20,
                )

                response.raise_for_status()
                st.session_state["latest"] = response.json()

            except requests.RequestException as exc:
                st.error(
                    "Start the API first with "
                    "`python -m uvicorn app.main:app`."
                )
                st.caption(str(exc))

    with right:
        latest = st.session_state.get("latest")

        if latest:
            st.success(latest["affirmation"])

            if latest["source"] == "openai":
                mode = "Cloud AI"

                st.caption(
                    f"Mode: {mode} · "
                    f"Category: {latest['category']} · "
                    f"Tone: {latest['tone']}"
                )

                st.info(
                    "Cloud AI mode generates affirmations "
                    "using the configured AI provider."
                )

            else:
                mode = "Offline Generator"

                st.caption(
                    f"Mode: {mode} · "
                    f"Category: {latest['category']} · "
                    f"Tone: {latest['tone']}"
                )

                st.info(
                    "Offline mode runs locally without paid API credits."
                )

        else:
            st.info("Generate an affirmation to see it here.")

with analytics_tab:
    daily_path = GOLD / "daily_metrics.csv"
    category_path = GOLD / "category_metrics.csv"

    if not daily_path.exists() or not category_path.exists():
        st.warning("Run `python -m pipeline.batch_etl` first.")

    else:
        daily = pd.read_csv(daily_path)
        categories = pd.read_csv(category_path)

        total = (
            int(daily["generation_count"].sum())
            if not daily.empty
            else 0
        )

        ai_total = (
            int(daily["ai_generation_count"].sum())
            if not daily.empty
            else 0
        )

        offline_total = total - ai_total

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Total generations",
            total,
        )

        c2.metric(
            "Offline generations",
            offline_total,
        )

        c3.metric(
            "Cloud AI generations",
            ai_total,
        )

        if not daily.empty:
            st.subheader("Daily volume")

            st.line_chart(
                daily.set_index("event_date")[
                    ["generation_count"]
                ]
            )

        if not categories.empty:
            st.subheader("Category popularity")

            st.bar_chart(
                categories.set_index("category")[
                    ["generation_count"]
                ]
            )

            st.dataframe(
                categories,
                width="stretch",
            )