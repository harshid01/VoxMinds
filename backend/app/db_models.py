from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

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


class JobRole(Base):
    __tablename__ = "job_roles"

    id = Column(Integer, primary_key=True, index=True)
    job_role_code = Column(String, unique=True, nullable=True)
    title = Column(String, nullable=False)
    sector = Column(String, nullable=True)
    nsqf_level = Column(String, nullable=True)
    qualification_title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    source = Column(String, nullable=True)

    competencies = relationship(
        "Competency",
        back_populates="job_role"
    )


class Competency(Base):
    __tablename__ = "competencies"

    id = Column(Integer, primary_key=True, index=True)
    job_role_id = Column(Integer, ForeignKey("job_roles.id"))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    job_role = relationship(
        "JobRole",
        back_populates="competencies"
    )