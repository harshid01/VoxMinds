from typing import List, Optional
from pydantic import BaseModel, Field

class AnswerExtractionRequest(BaseModel):
    transcript: str = Field(..., min_length=1)
    language: Optional[str] = "en"

class BeneficiaryProfile(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    language: Optional[str] = "en"
    education: Optional[str] = None
    family_occupation: Optional[str] = None
    current_livelihood: Optional[str] = None
    skills: List[str] = []
    interests: List[str] = []
    mobility_constraints: List[str] = []
    employment_preference: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    experience_years: Optional[int] = None
