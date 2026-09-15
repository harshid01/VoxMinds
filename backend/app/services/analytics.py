def dashboard_summary(db):
    from app import db_models
    beneficiaries=db.query(db_models.Beneficiary).count()
    outcomes=db.query(db_models.Outcome).count()
    opportunities=db.query(db_models.Opportunity).all()
    demand=sum(o.demand_count for o in opportunities)
    capacity=sum(o.training_capacity for o in opportunities)
    by_role={}
    for o in opportunities: by_role[o.role_title]=by_role.get(o.role_title,0)+o.demand_count
    return {"beneficiaries_assessed":beneficiaries,"outcome_events":outcomes,"local_demand":demand,"training_capacity":capacity,"capacity_gap":max(demand-capacity,0),"role_demand":sorted([{"role":k,"demand":v} for k,v in by_role.items()],key=lambda x:x["demand"],reverse=True)}
