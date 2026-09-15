from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app import db_models
from app.models import AnswerExtractionRequest, BeneficiaryProfile
from app.services.profile_extractor import extract_profile
from app.services.interview_engine import get_next_question
from app.services.skill_normalizer import normalize_skills
from app.services.competency_mapper import map_skills_to_competencies
from app.services.job_role_matcher import match_job_roles
from app.services.skill_gap import calculate_skill_gap
from app.services.roadmap import build_roadmap
from app.services.analytics import dashboard_summary
from app.auth_routes import router as auth_router
from app.admin_routes import router as admin_router
from app.auth_routes import current_user

app=FastAPI(title='VoxMinds API',description='AI-powered livelihood decision-support infrastructure for PM-AJAY GIA',version='3.0.0')
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:5173','http://127.0.0.1:5173'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
Base.metadata.create_all(bind=engine)

@app.on_event('startup')
def startup():
    # Development convenience: create demo accounts only in development mode.
    import os
    if os.getenv('VOXMINDS_ENV', 'development').lower() == 'development':
        from app.seed_auth import seed
        seed()
app.include_router(auth_router)
app.include_router(admin_router)

def listify(v): return [x.strip() for x in (v or '').split(',') if x.strip()]
def beneficiary_dict(b):
    return {'id':b.id,'name':b.name,'age':b.age,'language':b.language,'education':b.education,'family_occupation':b.family_occupation,'current_livelihood':b.current_livelihood,'skills':listify(b.skills),'interests':listify(b.interests),'mobility_constraints':listify(b.mobility_constraints),'employment_preference':b.employment_preference,'district':b.district,'state':b.state,'experience_years':b.experience_years,'created_at':b.created_at.isoformat() if b.created_at else None}
def role_dict(r):
    return {'id':r.id,'job_role_code':r.job_role_code,'title':r.title,'sector':r.sector,'nsqf_level':r.nsqf_level,'qualification_title':r.qualification_title,'description':r.description,'source':r.source,'training_duration_weeks':r.training_duration_weeks,'competencies':[{'id':c.id,'name':c.name,'description':c.description} for c in r.competencies]}

@app.get('/')
def root(): return {'message':'VoxMinds API is running','status':'success','version':'3.0.0'}
@app.get('/health')
def health(): return {'status':'healthy'}
@app.post('/api/profile/extract')
def profile_extract(req:AnswerExtractionRequest): return {'success':True,'transcript':req.transcript,'profile':extract_profile(req.transcript)}
@app.post('/api/interview/next')
def interview_next(profile:dict,language:str='en'): return get_next_question(profile,language)

@app.post('/api/beneficiaries')
def create_beneficiary(profile:BeneficiaryProfile,db:Session=Depends(get_db)):
    p=profile.model_dump(); b=db_models.Beneficiary(**{k:p.get(k) for k in ['name','age','language','education','family_occupation','current_livelihood','employment_preference','district','state','experience_years']},skills=','.join(p.get('skills',[])),interests=','.join(p.get('interests',[])),mobility_constraints=','.join(p.get('mobility_constraints',[])))
    db.add(b); db.commit(); db.refresh(b); return {'success':True,'beneficiary':beneficiary_dict(b)}
@app.put('/api/beneficiaries/{beneficiary_id}')
def update_beneficiary(beneficiary_id:int,profile:BeneficiaryProfile,db:Session=Depends(get_db)):
    b=db.get(db_models.Beneficiary,beneficiary_id)
    if not b: raise HTTPException(404,'Beneficiary not found')
    p=profile.model_dump()
    for k in ['name','age','language','education','family_occupation','current_livelihood','employment_preference','district','state','experience_years']:
        setattr(b,k,p.get(k))
    b.skills=','.join(p.get('skills',[])); b.interests=','.join(p.get('interests',[])); b.mobility_constraints=','.join(p.get('mobility_constraints',[]))
    db.commit(); db.refresh(b); return {'success':True,'beneficiary':beneficiary_dict(b)}
@app.get('/api/beneficiaries/{beneficiary_id}')
def get_beneficiary(beneficiary_id:int,db:Session=Depends(get_db)):
    b=db.get(db_models.Beneficiary,beneficiary_id)
    if not b: raise HTTPException(404,'Beneficiary not found')
    return {'success':True,'beneficiary':beneficiary_dict(b)}
@app.get('/api/beneficiaries')
def list_beneficiaries(db:Session=Depends(get_db)):
    rows=db.query(db_models.Beneficiary).order_by(db_models.Beneficiary.id.desc()).limit(100).all(); return {'success':True,'count':len(rows),'beneficiaries':[beneficiary_dict(x) for x in rows]}


@app.get('/api/me/profile')
def my_profile(authorization: str|None=Header(default=None), db:Session=Depends(get_db)):
    u=current_user(authorization,db)
    if not u.beneficiary_id: raise HTTPException(403,'This account has no beneficiary profile')
    b=db.get(db_models.Beneficiary,u.beneficiary_id)
    if not b: raise HTTPException(404,'Beneficiary profile not found')
    return {'success':True,'beneficiary':beneficiary_dict(b)}

@app.put('/api/me/profile')
def update_my_profile(profile:BeneficiaryProfile, authorization: str|None=Header(default=None), db:Session=Depends(get_db)):
    u=current_user(authorization,db)
    if not u.beneficiary_id: raise HTTPException(403,'This account has no beneficiary profile')
    b=db.get(db_models.Beneficiary,u.beneficiary_id)
    if not b: raise HTTPException(404,'Beneficiary profile not found')
    p=profile.model_dump()
    for k in ['name','age','language','education','family_occupation','current_livelihood','employment_preference','district','state','experience_years']:
        if k in p: setattr(b,k,p.get(k))
    b.skills=','.join(p.get('skills',[])); b.interests=','.join(p.get('interests',[])); b.mobility_constraints=','.join(p.get('mobility_constraints',[]))
    u.name=b.name
    db.commit(); db.refresh(b)
    return {'success':True,'beneficiary':beneficiary_dict(b)}

@app.post('/api/me/outcomes')
def my_outcome(data:dict, authorization: str|None=Header(default=None), db:Session=Depends(get_db)):
    u=current_user(authorization,db)
    if not u.beneficiary_id: raise HTTPException(403,'This account has no beneficiary profile')
    o=db_models.Outcome(beneficiary_id=u.beneficiary_id,stage=data.get('stage','assessment'),status=data.get('status','started'),notes=data.get('notes'))
    db.add(o); db.commit(); db.refresh(o)
    return {'success':True,'outcome_id':o.id}

@app.get('/api/job-roles')
def job_roles(db:Session=Depends(get_db)):
    rows=db.query(db_models.JobRole).all(); return {'success':True,'count':len(rows),'job_roles':[role_dict(r) for r in rows]}
@app.post('/api/skills/normalize')
def normalize(data:dict):
    text=data.get('text',''); skills=normalize_skills(text); return {'success':bool(text.strip()),'input':text,'skills':skills,'count':len(skills)}
@app.post('/api/skills/map-competencies')
def map_comp(data:dict): return {'success':True,'mappings':map_skills_to_competencies(data.get('skills',[]))}
@app.post('/api/job-roles/recommend')
def recommend(data:dict,db:Session=Depends(get_db)):
    profile=data.get('profile') or data; roles=db.query(db_models.JobRole).all(); opps=db.query(db_models.Opportunity).all(); recs=match_job_roles(profile,roles,opps,5)
    return {'success':True,'recommendations':recs,'demo_notice':'Opportunity and NSQF records are demo data until replaced with verified official sources.'}
@app.post('/api/job-roles/{job_role_id}/skill-gap')
def skill_gap(job_role_id:int,data:dict,db:Session=Depends(get_db)):
    role=db.get(db_models.JobRole,job_role_id)
    if not role: raise HTTPException(404,'Job role not found')
    profile=data.get('profile') or data; return {'success':True,'job_role':role_dict(role),'gap':calculate_skill_gap(profile,role)}
@app.post('/api/roadmap')
def roadmap(data:dict,db:Session=Depends(get_db)):
    profile=data.get('profile',{}); role_id=data.get('job_role_id'); role=db.get(db_models.JobRole,role_id)
    if not role: raise HTTPException(404,'Job role not found')
    opps=db.query(db_models.Opportunity).all(); rec=match_job_roles(profile,[role],opps,1)[0]; gap=calculate_skill_gap(profile,role)
    return {'success':True,'recommendation':rec,'gap':gap,'roadmap':build_roadmap(profile,rec,gap)}

@app.get('/api/opportunities')
def opportunities(district:str|None=None,db:Session=Depends(get_db)):
    q=db.query(db_models.Opportunity)
    if district: q=q.filter(db_models.Opportunity.district.ilike(district))
    rows=q.all(); return {'success':True,'count':len(rows),'opportunities':[{'id':o.id,'district':o.district,'state':o.state,'role_title':o.role_title,'demand_level':o.demand_level,'demand_count':o.demand_count,'training_capacity':o.training_capacity,'capacity_gap':max(o.demand_count-o.training_capacity,0),'wage_min':o.wage_min,'wage_max':o.wage_max,'enterprise_fit':o.enterprise_fit,'source':o.source} for o in rows],'demo_notice':'Opportunity data is synthetic demonstration data.'}
@app.get('/api/dashboard/summary')
def dashboard(db:Session=Depends(get_db)): return {'success':True,'summary':dashboard_summary(db)}
@app.post('/api/outcomes')
def outcome(data:dict,db:Session=Depends(get_db)):
    b=db.get(db_models.Beneficiary,data.get('beneficiary_id'))
    if not b: raise HTTPException(404,'Beneficiary not found')
    o=db_models.Outcome(beneficiary_id=b.id,stage=data.get('stage','assessment'),status=data.get('status','started'),notes=data.get('notes')); db.add(o); db.commit(); db.refresh(o); return {'success':True,'outcome_id':o.id}
@app.get('/api/outcomes/{beneficiary_id}')
def outcomes(beneficiary_id:int,db:Session=Depends(get_db)):
    rows=db.query(db_models.Outcome).filter(db_models.Outcome.beneficiary_id==beneficiary_id).order_by(db_models.Outcome.id.desc()).all(); return {'success':True,'outcomes':[{'id':o.id,'stage':o.stage,'status':o.status,'notes':o.notes,'created_at':o.created_at.isoformat() if o.created_at else None} for o in rows]}
@app.get('/api/me/dashboard')
def my_dashboard(authorization: str|None=Header(default=None), db:Session=Depends(get_db)):
    from app.auth_routes import current_user
    u=current_user(authorization,db)
    if not u.beneficiary_id:
        return {'success':True,'user':{'name':u.name,'email':u.email},'beneficiary':None,'recommendations':[],'outcomes':[]}
    b=db.get(db_models.Beneficiary,u.beneficiary_id)
    if not b: raise HTTPException(404,'Beneficiary profile not found')
    profile=beneficiary_dict(b)
    roles=db.query(db_models.JobRole).all(); opps=db.query(db_models.Opportunity).all()
    recs=match_job_roles(profile,roles,opps,3)
    outs=db.query(db_models.Outcome).filter(db_models.Outcome.beneficiary_id==b.id).order_by(db_models.Outcome.id.desc()).all()
    return {'success':True,'user':{'name':u.name,'email':u.email},'beneficiary':profile,'recommendations':recs,'outcomes':[{'stage':o.stage,'status':o.status,'notes':o.notes,'created_at':o.created_at.isoformat() if o.created_at else None} for o in outs]}

@app.get('/api/channels/status')
def channel_status(): return {'web':True,'whatsapp':{'mode':'adapter-ready','configured':False},'ivr':{'mode':'adapter-ready','configured':False},'note':'Connect approved provider credentials before production use.'}
