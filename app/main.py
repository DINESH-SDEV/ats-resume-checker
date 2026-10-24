from pydantic import BaseModel
from app.scorer import score_resume
from fastapi import FastAPI
from app.auth import router as auth_router 
app = FastAPI(
    title="AI Resume ATS Checker",
    description="Check resume compatibility with job descriptions",
    version="1.0.0"
)
app.include_router(auth_router)
class ResumeRequest(BaseModel):
    resume_text: str
    job_text: str


@app.post("/score")
def score_resume_api(request: ResumeRequest):
    return score_resume(
        request.resume_text,
        request.job_text
    )

@app.get("/")
def home():
    return {
        "message": "Hello World",
        "project": "AI Resume ATS Checker",
        "status": "Running successfully"
    }
