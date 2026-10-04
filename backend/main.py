from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analyzer import analyze_code
from ai_reviewer import ai_review

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodeInput(BaseModel):
    code: str
    language: str = "python"


@app.get("/")
def root():
    return {"message": "AI Code Review Assistant is running"}


@app.post("/review")
def review_code(payload: CodeInput):
    issues = analyze_code(payload.code)
    return {
        "language": payload.language,
        "issue_count": len(issues),
        "issues": issues,
    }


@app.post("/review-ai")
def review_code_ai(payload: CodeInput):
    issues = analyze_code(payload.code)
    try:
        feedback = ai_review(payload.code, issues)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI review failed: {e}")
    return {
        "language": payload.language,
        "issues": issues,
        "ai_feedback": feedback,
    }
