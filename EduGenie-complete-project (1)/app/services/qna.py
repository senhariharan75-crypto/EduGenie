from app.services.gemini import GeminiService

def answer_question(question: str) -> str:
    prompt = f"""You are EduGenie, an educational assistant. Answer the student's question accurately and concisely.
Use simple language, define technical terms, and use short bullets when helpful. Do not invent facts.

Student question:
{question}
"""
    return GeminiService().generate(prompt)
