from app.services.gemini import GeminiService

QUIZ_SCHEMA = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "question": {"type": "STRING"},
            "options": {"type": "ARRAY", "items": {"type": "STRING"}},
            "correct_answer": {"type": "STRING"},
            "explanation": {"type": "STRING"},
        },
        "required": ["question", "options", "correct_answer", "explanation"],
    },
}

def generate_quiz(passage: str, count: int = 3) -> list[dict]:
    prompt = f"""Create exactly {count} multiple-choice questions from the passage below.
Each question must have exactly four distinct options. The correct_answer must exactly match one option.
Questions must test understanding rather than trivial wording. Return only the requested JSON structure.

PASSAGE:
{passage}
"""
    data = GeminiService().generate_json(prompt, QUIZ_SCHEMA)
    if not isinstance(data, list):
        raise RuntimeError("Quiz response was not a list")
    normalized = []
    for item in data[:count]:
        options = item.get("options", [])
        if len(options) != 4 or item.get("correct_answer") not in options:
            raise RuntimeError("Gemini returned an invalid quiz question")
        normalized.append({
            "question": item["question"],
            "options": options,
            "correct_answer": item["correct_answer"],
            "explanation": item.get("explanation", ""),
        })
    if len(normalized) != count:
        raise RuntimeError("Gemini did not return the requested number of questions")
    return normalized
