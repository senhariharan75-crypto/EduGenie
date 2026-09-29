from typing import Literal
from pydantic import BaseModel, Field, field_validator

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Input cannot be empty")
        return value

class QARequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=20000)

class ExplanationRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=10000)

class QuizRequest(BaseModel):
    passage: str = Field(..., min_length=1, max_length=20000)
    count: int = Field(default=3, ge=1, le=10)

class LearningRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=5000)
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    weeks: int = Field(default=6, ge=1, le=52)

class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str = ""

class QuizResponse(BaseModel):
    questions: list[QuizQuestion]
