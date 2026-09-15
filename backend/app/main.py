from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app import db_models
from app.models import AnswerExtractionRequest
from app.services.profile_extractor import extract_profile
from app.services.interview_engine import get_next_question
from app.services.skill_normalizer import normalize_skills
from app.services.competency_mapper import (map_skills_to_competencies)
from app.services.job_role_matcher import match_job_roles

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

@app.post("/api/skills/normalize")
def normalize_skill_endpoint(data: dict):
    text = data.get("text", "")

    if not text.strip():
        return {
            "success": False,
            "message": "Text is required",
            "skills": [],
        }

    skills = normalize_skills(text)

    return {
        "success": True,
        "input": text,
        "count": len(skills),
        "skills": skills,
    }
@app.post("/api/skills/map-competencies")
def map_skill_competencies(data: dict):
    skills = data.get("skills", [])

    if not skills:
        return {
            "success": False,
            "message": "Skills are required",
            "mappings": [],
        }

    mappings = map_skills_to_competencies(skills)

    return {
        "success": True,
        "skills": skills,
        "mappings": mappings,
    }

@app.post("/api/job-roles/recommend")
def recommend_job_roles(
    data: dict,
    db: Session = Depends(get_db)
):
    skills = data.get("skills", [])

    if not skills:
        return {
            "success": False,
            "message": "Skills are required",
            "recommendations": [],
        }

    job_roles = (
        db.query(db_models.JobRole)
        .all()
    )

    recommendations = match_job_roles(
        skills=skills,
        job_roles=job_roles,
        top_k=5
    )

    return {
        "success": True,
        "skills": skills,
        "count": len(recommendations),
        "recommendations": recommendations,
    }