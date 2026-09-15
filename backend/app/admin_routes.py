from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import db_models
from app.auth_routes import current_user

router=APIRouter(prefix='/api/admin',tags=['Admin'])

def admin_user(authorization,db):
    u=current_user(authorization,db)
    if u.role!='admin': raise HTTPException(403,'Admin access required')
    return u

@router.get('/overview')
def overview(authorization: str|None=Header(default=None),db:Session=Depends(get_db)):
    admin_user(authorization,db)
    beneficiaries=db.query(db_models.Beneficiary).count()
    users=db.query(db_models.User).filter(db_models.User.role=='beneficiary').count()
    outcomes=db.query(db_models.Outcome).count()
    roles=db.query(db_models.JobRole).count()
    opportunities=db.query(db_models.Opportunity).count()
    return {'success':True,'stats':{'beneficiaries':beneficiaries,'users':users,'outcomes':outcomes,'job_roles':roles,'opportunities':opportunities}}

@router.get('/beneficiaries')
def beneficiaries(authorization: str|None=Header(default=None),db:Session=Depends(get_db)):
    admin_user(authorization,db)
    rows=db.query(db_models.Beneficiary).order_by(db_models.Beneficiary.id.desc()).limit(200).all()
    return {'success':True,'beneficiaries':[{'id':b.id,'name':b.name,'district':b.district,'state':b.state,'education':b.education,'employment_preference':b.employment_preference,'created_at':b.created_at.isoformat() if b.created_at else None} for b in rows]}
