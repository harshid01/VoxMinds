def dashboard_summary(db):
    from app import db_models
    beneficiaries=db.query(db_models.Beneficiary).count(); outcomes=db.query(db_models.Outcome).count(); opportunities=db.query(db_models.Opportunity).all()
    demand=sum(o.demand_count for o in opportunities); capacity=sum(o.training_capacity for o in opportunities)
    roles={}
    for o in opportunities: roles[o.role_title]=roles.get(o.role_title,0)+o.demand_count
    districts={}
    for o in opportunities: districts[o.district]=districts.get(o.district,0)+max(o.demand_count-o.training_capacity,0)
    return {'beneficiaries_assessed':beneficiaries,'outcome_events':outcomes,'local_demand':demand,'training_capacity':capacity,'capacity_gap':max(demand-capacity,0),'role_demand':sorted([{'role':k,'demand':v} for k,v in roles.items()],key=lambda x:x['demand'],reverse=True),'district_gaps':sorted([{'district':k,'gap':v} for k,v in districts.items()],key=lambda x:x['gap'],reverse=True)}
