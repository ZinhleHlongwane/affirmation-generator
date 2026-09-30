from dataclasses import dataclass

from app.core.config import Settings


@dataclass
class GenerationResult:
    text: str
    source: str
    model_name: str | None = None


class AffirmationAIService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def generate(
        self,
        *,
        name: str | None,
        mood: str | None,
        goal: str | None,
        category: str,
        tone: str,
    ) -> GenerationResult:
        if self.settings.ai_enabled and self.settings.openai_api_key:
            try:
                return self._generate_with_openai(
                    name=name,
                    mood=mood,
                    goal=goal,
                    category=category,
                    tone=tone,
                )
            except Exception:
                pass

        return GenerationResult(
            text=self._fallback(name=name, goal=goal, category=category, tone=tone),
            source="fallback",
        )

    def _generate_with_openai(
        self,
        *,
        name: str | None,
        mood: str | None,
        goal: str | None,
        category: str,
        tone: str,
    ) -> GenerationResult:
        from openai import OpenAI

        client = OpenAI(api_key=self.settings.openai_api_key)

        context = {
            "name": name or "not provided",
            "mood": mood or "not provided",
            "goal": goal or "general growth",
            "category": category,
            "tone": tone,
        }

        response = client.responses.create(
            model=self.settings.openai_model,
            instructions=(
                "Generate one short, realistic first-person affirmation between "
                "12 and 35 words. Avoid medical, legal, financial or supernatural "
                "claims. Return only the affirmation text."
            ),
            input=f"User context: {context}",
        )

        text = response.output_text.strip()
        if not text:
            raise ValueError("AI response was empty.")

        return GenerationResult(
            text=text,
            source="openai",
            model_name=self.settings.openai_model,
        )

    def _fallback(
        self,
        *,
        name: str | None,
        goal: str | None,
        category: str,
        tone: str,
    ) -> str:
        templates = {
            "career": "I can keep learning, building and moving toward the career I want.",
            "confidence": "I trust myself to learn from challenges and grow in confidence.",
            "learning": "Every problem I work through strengthens how I think and learn.",
            "focus": "I can focus on the next useful step and let progress build from there.",
            "wellbeing": "I can treat myself with patience while choosing what supports my wellbeing.",
            "relationships": "I can communicate with honesty, respect and healthy boundaries.",
            "general": "I can grow at my own pace and still be proud of the progress I make.",
        }

        text = templates.get(category, templates["general"])

        if goal:
            text = f"I can keep working toward {goal} one practical step at a time."

        if tone == "bold":
            text = text.replace("I can", "I will", 1)
        elif tone == "kawaii":
            text += " ✨🌸"

        if name:
            text = f"{name}, {text[0].lower() + text[1:]}"

        return text
