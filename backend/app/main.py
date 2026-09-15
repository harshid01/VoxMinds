from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import AnswerExtractionRequest
from app.services.profile_extractor import extract_profile
from app.services.interview_engine import get_next_question
from sqlalchemy.orm import Session
from fastapi import Depends


app = FastAPI(
    title="VoxMinds API",
    description="AI-powered livelihood assistant",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "VoxMinds API is running",
        "status": "success",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/profile/extract")
def extract_answer(request: AnswerExtractionRequest):
    profile = extract_profile(request.transcript)

    return {
        "success": True,
        "transcript": request.transcript,
        "profile": profile,
    }
@app.post("/api/interview/next")
def next_interview_question(
    profile: dict,
    language: str = "en"
):
    result = get_next_question(profile, language)

    return result

@app.get("/api/job-roles")
def get_job_roles(
    db: Session = Depends(get_db)
):
    roles = db.query(
        db_models.JobRole
    ).all()

    return {
        "success": True,
        "count": len(roles),
        "job_roles": [
            {
                "id": role.id,
                "job_role_code": role.job_role_code,
                "title": role.title,
                "sector": role.sector,
                "nsqf_level": role.nsqf_level,
                "qualification_title":
                    role.qualification_title,
                "description": role.description,
                "source": role.source,
                "competencies": [
                    {
                        "id": competency.id,
                        "name": competency.name,
                        "description":
                            competency.description,
                    }
                    for competency in role.competencies
                ],
            }
            for role in roles
        ],
    }