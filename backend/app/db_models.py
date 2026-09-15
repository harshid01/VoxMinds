from sqlalchemy import Column,Integer,String,Text,ForeignKey,DateTime,Boolean,Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
class Beneficiary(Base):
    __tablename__='beneficiaries'; id=Column(Integer,primary_key=True,index=True); name=Column(String); age=Column(Integer); language=Column(String); education=Column(String); family_occupation=Column(String); current_livelihood=Column(String); skills=Column(Text); interests=Column(Text); mobility_constraints=Column(Text); employment_preference=Column(String); district=Column(String); state=Column(String); experience_years=Column(Integer); created_at=Column(DateTime,default=datetime.utcnow)
class JobRole(Base):
    __tablename__='job_roles'; id=Column(Integer,primary_key=True,index=True); job_role_code=Column(String,unique=True,nullable=False); title=Column(String,nullable=False); sector=Column(String); nsqf_level=Column(String); qualification_title=Column(String); description=Column(Text); source=Column(String); training_duration_weeks=Column(Integer,default=8); competencies=relationship('Competency',back_populates='job_role',cascade='all, delete-orphan')
class Competency(Base):
    __tablename__='competencies'; id=Column(Integer,primary_key=True,index=True); job_role_id=Column(Integer,ForeignKey('job_roles.id'),nullable=False); name=Column(String,nullable=False); description=Column(Text); job_role=relationship('JobRole',back_populates='competencies')
class Opportunity(Base):
    __tablename__='opportunities'; id=Column(Integer,primary_key=True,index=True); district=Column(String,nullable=False); state=Column(String,nullable=False); role_title=Column(String,nullable=False); demand_level=Column(String,nullable=False); demand_count=Column(Integer,default=0); training_capacity=Column(Integer,default=0); wage_min=Column(Integer,default=0); wage_max=Column(Integer,default=0); enterprise_fit=Column(String,default='medium'); source=Column(String,default='DEMO_DATA_NOT_OFFICIAL')
class Outcome(Base):
    __tablename__='outcomes'; id=Column(Integer,primary_key=True,index=True); beneficiary_id=Column(Integer,ForeignKey('beneficiaries.id'),nullable=False); stage=Column(String,nullable=False); status=Column(String,nullable=False); notes=Column(Text); created_at=Column(DateTime,default=datetime.utcnow)

class User(Base):
    __tablename__='users'; id=Column(Integer,primary_key=True,index=True); name=Column(String,nullable=False); email=Column(String,unique=True,index=True,nullable=False); password_hash=Column(String,nullable=False); role=Column(String,nullable=False,default='beneficiary'); beneficiary_id=Column(Integer,nullable=True); active=Column(Boolean,default=True); created_at=Column(DateTime,default=datetime.utcnow)

class RefreshSession(Base):
    __tablename__='refresh_sessions'
    id=Column(Integer,primary_key=True,index=True)
    jti=Column(String,unique=True,index=True,nullable=False)
    user_id=Column(Integer,ForeignKey('users.id'),nullable=False,index=True)
    expires_at=Column(DateTime,nullable=False)
    revoked_at=Column(DateTime,nullable=True)
    created_at=Column(DateTime,default=datetime.utcnow)
