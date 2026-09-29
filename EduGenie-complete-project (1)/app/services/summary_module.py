from app.services.gemini import GeminiService

def summarize(text: str) -> str:
    prompt = f"""Summarize the following educational passage for a student.
Keep the core facts, important terminology, and relationships. Remove repetition. Use a short heading and bullet points where useful.

PASSAGE:
{text}
"""
    return GeminiService().generate(prompt)
