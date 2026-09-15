from app.database import Base, engine, SessionLocal
from app.db_models import JobRole, Competency, Opportunity

ROLES=[
("DEMO-ELECTRICAL-001","Electrical Technician","Electrical","DEMO","DEMO RECORD - VERIFY OFFICIAL SOURCE",["Electrical Repair","Electrical Maintenance","Electrical Safety","Domestic Wiring"]),
("DEMO-SOLAR-001","Solar Technician","Renewable Energy","DEMO","DEMO RECORD - VERIFY OFFICIAL SOURCE",["Electrical Wiring","Solar Installation","Solar Maintenance","Electrical Safety"]),
("DEMO-TAILOR-001","Tailoring Professional","Apparel","DEMO","DEMO RECORD - VERIFY OFFICIAL SOURCE",["Sewing","Garment Stitching","Tailoring"]),
("DEMO-CARPENTRY-001","Carpenter","Construction","DEMO","DEMO RECORD - VERIFY OFFICIAL SOURCE",["Carpentry","Woodworking","Furniture Making"]),
("DEMO-DIGITAL-001","Digital Service Assistant","IT-ITeS","DEMO","DEMO RECORD - VERIFY OFFICIAL SOURCE",["Digital Literacy","Computer Operations","Office Productivity"])]
OPPS=[
("Ahmedabad","Gujarat","Electrical Technician","high",320,180,12000,22000,"medium"),("Ahmedabad","Gujarat","Solar Technician","high",140,100,14000,26000,"high"),("Ahmedabad","Gujarat","Tailoring Professional","medium",180,250,9000,18000,"high"),("Ahmedabad","Gujarat","Carpenter","medium",120,90,12000,22000,"high"),("Ahmedabad","Gujarat","Digital Service Assistant","high",210,160,10000,20000,"medium"),("Surat","Gujarat","Tailoring Professional","high",300,220,10000,20000,"high"),("Surat","Gujarat","Electrical Technician","medium",180,150,12000,22000,"medium")]

def seed():
    Base.metadata.create_all(bind=engine); db=SessionLocal()
    try:
      if db.query(JobRole).count()==0:
        for code,title,sector,level,qual,comps in ROLES:
          r=JobRole(job_role_code=code,title=title,sector=sector,nsqf_level=level,qualification_title=qual,description="Demonstration role; replace with verified official NSQF/QP data before production.",source="DEMO_DATA_NOT_OFFICIAL",training_duration_weeks=10); db.add(r); db.flush()
          for c in comps: db.add(Competency(job_role_id=r.id,name=c,description="Demo competency"))
      if db.query(Opportunity).count()==0:
        for d,s,r,level,dem,cap,w1,w2,ent in OPPS: db.add(Opportunity(district=d,state=s,role_title=r,demand_level=level,demand_count=dem,training_capacity=cap,wage_min=w1,wage_max=w2,enterprise_fit=ent))
      db.commit(); print("VoxMinds demo knowledge base seeded.")
    finally: db.close()
if __name__=="__main__": seed()
