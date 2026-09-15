from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Beneficiary(Base):
    __tablename__ = "beneficiaries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    language = Column(String, nullable=True)
    education = Column(String, nullable=True)
    family_occupation = Column(String, nullable=True)
    current_livelihood = Column(String, nullable=True)
    skills = Column(Text, nullable=True)
    interests = Column(Text, nullable=True)
    mobility_constraints = Column(Text, nullable=True)
    employment_preference = Column(String, nullable=True)
    district = Column(String, nullable=True)
    state = Column(String, nullable=True)
    experience_years = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class JobRole(Base):
    __tablename__ = "job_roles"
    id = Column(Integer, primary_key=True, index=True)
    job_role_code = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    sector = Column(String, nullable=True)
    nsqf_level = Column(String, nullable=True)
    qualification_title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    source = Column(String, nullable=True)
    training_duration_weeks = Column(Integer, default=8)
    competencies = relationship("Competency", back_populates="job_role", cascade="all, delete-orphan")

class Competency(Base):
    __tablename__ = "competencies"
    id = Column(Integer, primary_key=True, index=True)
    job_role_id = Column(Integer, ForeignKey("job_roles.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    job_role = relationship("JobRole", back_populates="competencies")

class Opportunity(Base):
    __tablename__ = "opportunities"
    id = Column(Integer, primary_key=True, index=True)
    district = Column(String, nullable=False)
    state = Column(String, nullable=False)
    role_title = Column(String, nullable=False)
    demand_level = Column(String, nullable=False)
    demand_count = Column(Integer, default=0)
    training_capacity = Column(Integer, default=0)
    wage_min = Column(Integer, default=0)
    wage_max = Column(Integer, default=0)
    enterprise_fit = Column(String, default="medium")
    source = Column(String, default="DEMO_DATA_NOT_OFFICIAL")

class Outcome(Base):
    __tablename__ = "outcomes"
    id = Column(Integer, primary_key=True, index=True)
    beneficiary_id = Column(Integer, ForeignKey("beneficiaries.id"), nullable=False)
    stage = Column(String, nullable=False)
    status = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
