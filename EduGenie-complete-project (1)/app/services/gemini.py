import json
from typing import Any
from app.config import get_settings

class GeminiService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._client = None

    @property
    def client(self):
        if not self.settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured. Add it to .env")
        if self._client is None:
            try:
                from google import genai
            except ImportError as exc:
                raise RuntimeError("google-genai is not installed. Run: pip install -r requirements.txt") from exc
            self._client = genai.Client(api_key=self.settings.gemini_api_key)
        return self._client

    def generate(self, prompt: str, *, json_schema: dict[str, Any] | None = None) -> str:
        try:
            from google.genai import types
        except ImportError as exc:
            raise RuntimeError("google-genai is not installed. Run: pip install -r requirements.txt") from exc
        config = types.GenerateContentConfig(
            temperature=0.3,
            response_mime_type="application/json" if json_schema else "text/plain",
            response_schema=json_schema,
        )
        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=config,
        )
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response")
        return text.strip()

    def generate_json(self, prompt: str, schema: dict[str, Any]) -> Any:
        raw = self.generate(prompt, json_schema=schema)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            cleaned = raw.removeprefix("```json").removesuffix("```").strip()
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                raise RuntimeError(f"Gemini returned invalid JSON: {exc}") from exc
