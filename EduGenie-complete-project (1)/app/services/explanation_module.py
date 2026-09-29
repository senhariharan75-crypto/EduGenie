from functools import lru_cache
from app.config import get_settings
from app.services.gemini import GeminiService

@lru_cache(maxsize=1)
def _load_local_pipeline():
    from transformers import pipeline
    return pipeline("text2text-generation", model=get_settings().local_explanation_model)

def _local_explain(topic: str) -> str:
    pipe = _load_local_pipeline()
    prompt = f"Explain {topic} simply for a beginner in 5 short points."
    result = pipe(prompt, max_new_tokens=180, do_sample=False)[0]["generated_text"]
    return result.strip()

def explain(topic: str) -> str:
    settings = get_settings()
    if settings.use_local_explanation:
        try:
            return _local_explain(topic)
        except Exception:
            pass
    prompt = f"""Explain the educational topic '{topic}' for a beginner.
Use simple language, an intuitive example, and 4-6 short bullet points. Avoid unnecessary jargon.
"""
    return GeminiService().generate(prompt)
