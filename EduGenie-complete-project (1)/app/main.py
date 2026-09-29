from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import get_settings
from app.schemas import QARequest, ExplanationRequest, QuizRequest, LearningRequest, TextRequest, QuizResponse
from app.services.qna import answer_question
from app.services.explanation_module import explain
from app.services.quiz_module import generate_quiz
from app.services.summary_module import summarize
from app.services.learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent.parent
settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name},
    )
@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name, "gemini_configured": bool(settings.gemini_api_key)}

def run_safely(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        if settings.debug:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {exc}") from exc
        raise HTTPException(status_code=500, detail="EduGenie could not complete the request.") from exc

@app.post("/qa")
def qa(payload: QARequest):
    return {"answer": run_safely(answer_question, payload.question)}

@app.post("/explain")
def explanation(payload: ExplanationRequest):
    return {"explanation": run_safely(explain, payload.topic)}

@app.post("/quiz", response_model=QuizResponse)
def quiz(payload: QuizRequest):
    return {"questions": run_safely(generate_quiz, payload.passage, payload.count)}

@app.post("/summarize")
def summary(payload: TextRequest):
    return {"summary": run_safely(summarize, payload.text)}

@app.post("/learn/recommendations")
def learning(payload: LearningRequest):
    return {"recommendations": run_safely(get_learning_recommendations, payload.topic, payload.level, payload.weeks)}
