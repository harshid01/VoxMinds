from app.database import Base, engine, SessionLocal
from app import db_models
from app.auth import hash_password

def seed():
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    try:
        b=db.query(db_models.Beneficiary).filter(db_models.Beneficiary.name=='Demo Beneficiary').first()
        if not b:
            b=db_models.Beneficiary(name='Demo Beneficiary',age=24,language='en',education='10th',family_occupation='Electrical work',current_livelihood='Helper',skills='electrical repair,wiring',interests='solar,technology',mobility_constraints='',employment_preference='wage',district='Surat',state='Gujarat',experience_years=2)
            db.add(b); db.commit(); db.refresh(b)
        accounts=[('VoxMinds User','user@voxminds.in','user123','beneficiary',b.id),('VoxMinds Admin','admin@voxminds.in','admin123','admin',None)]
        for name,email,pw,role,bid in accounts:
            u=db.query(db_models.User).filter(db_models.User.email==email).first()
            if not u:
                db.add(db_models.User(name=name,email=email,password_hash=hash_password(pw),role=role,beneficiary_id=bid,active=True))
            else:
                # Refresh development credentials using the current Argon2 password scheme.
                u.password_hash=hash_password(pw); u.active=True; u.role=role; u.beneficiary_id=bid
        db.commit(); print('Auth demo accounts ready')
    finally: db.close()
if __name__=='__main__': seed()
