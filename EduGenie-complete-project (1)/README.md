# EduGenie — Google Gemini Powered Learning Assistant

A complete FastAPI + HTML/CSS/JavaScript educational assistant based on the supplied EduGenie project document.

## Features
- Q&A via Gemini
- Beginner-friendly topic explanation
- 3-question MCQ quiz with 4 options and answer checking
- Educational passage summarization
- Beginner/intermediate/advanced learning paths with week planning
- `/health` endpoint
- Responsive browser UI
- Optional local LaMini-Flan-T5 explanation model; disabled by default so setup stays lightweight

## Project structure
```text
EduGenie/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── schemas.py
│   └── services/
│       ├── gemini.py
│       ├── explanation_module.py
│       ├── qna.py
│       ├── quiz_module.py
│       ├── summary_module.py
│       └── learning_path.py
├── static/
│   ├── app.js
│   └── style.css
├── templates/
│   └── index.html
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## VS Code setup (Windows)
1. Install Python 3.10+ and VS Code.
2. Open this folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment:
   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
5. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
6. Copy `.env.example` to `.env` and put your Google AI Studio Gemini API key in `GEMINI_API_KEY`.
7. Start the server:
   ```powershell
   uvicorn main:app --reload
   ```
8. Open http://127.0.0.1:8000

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

## Testing
Run automated tests:
```bash
pytest -q
```

Health check:
```text
http://127.0.0.1:8000/health
```

FastAPI interactive API documentation:
```text
http://127.0.0.1:8000/docs
```

## API examples
### Q&A
`POST /qa`
```json
{"question":"Which is the largest ocean?"}
```

### Explain
`POST /explain`
```json
{"topic":"Pythagoras theorem"}
```

### Quiz
`POST /quiz`
```json
{"passage":"Photosynthesis is the process by which green plants convert light energy into chemical energy.","count":3}
```

### Summarize
`POST /summarize`
```json
{"text":"Long educational passage..."}
```

### Learning path
`POST /learn/recommendations`
```json
{"topic":"SQL","level":"beginner","weeks":6}
```

## Optional local explanation model
The original project document describes LaMini-Flan-T5-783M for explanations. To enable it:
1. Uncomment `transformers` and `torch` in `requirements.txt`.
2. Run `pip install -r requirements.txt` again.
3. Set `USE_LOCAL_EXPLANATION=true` in `.env`.

The app falls back to Gemini if the local model cannot load.

## Security notes
- Never commit `.env` or an API key.
- Keep API keys server-side; the browser never receives the Gemini key.
- For production, set `DEBUG=false`, restrict CORS, add authentication/rate limiting, and use HTTPS.
