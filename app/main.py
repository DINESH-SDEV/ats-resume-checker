
from fastapi import FastAPI

app = FastAPI(
    title="AI Resume ATS Checker",
    description="Check resume compatibility with job descriptions",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Hello World",
        "project": "AI Resume ATS Checker",
        "status": "Running successfully"
    }
