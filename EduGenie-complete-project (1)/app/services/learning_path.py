from app.services.gemini import GeminiService

def get_learning_recommendations(topic: str, level: str = "beginner", weeks: int = 6) -> str:
    prompt = f"""Create a personalized learning path for: {topic}
Learner level: {level}
Duration: {weeks} weeks

Start from appropriate foundations and progress toward advanced concepts. Organize by week.
For each week include goals, key topics, a small practice task, and suggested resource types (videos, articles, books, or documentation).
Keep it practical and concise. Do not fabricate exact URLs or named resources unless you are confident they exist.
"""
    return GeminiService().generate(prompt)
