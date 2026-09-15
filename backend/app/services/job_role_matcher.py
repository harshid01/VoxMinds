from app.services.competency_mapper import competency_set

def score_role(profile, role, opportunity=None):
    existing=competency_set(profile.get("skills",[]))
    required={c.name.strip().lower() for c in role.competencies}
    matched=existing & required
    skill_match=(len(matched)/len(required)*100) if required else 0
    interests={x.lower() for x in profile.get("interests",[])}
    interest_match=100 if interests and any((role.title.lower() in i or i in role.title.lower()) or (role.sector and role.sector.lower() in i) for i in interests) else (40 if not interests else 0)
    education_match=100 if profile.get("education") in ["12th","Graduate"] else 70
    mobility_match=100 if not profile.get("mobility_constraints") else 75
    pref=profile.get("employment_preference")
    enterprise=100 if pref=="self_employment" and opportunity and opportunity.enterprise_fit in ["high","medium"] else 70
    local=50
    if opportunity:
        local={"high":100,"medium":70,"low":40}.get(opportunity.demand_level.lower(),50)
    score=0.30*skill_match+0.15*interest_match+0.10*education_match+0.10*mobility_match+0.10*enterprise+0.25*local
    reasons=[]
    if matched: reasons.append(f"Matches {len(matched)} existing competencies")
    if opportunity and opportunity.demand_level.lower()=="high": reasons.append("High local demand signal")
    if pref=="self_employment": reasons.append("Supports the self-employment preference")
    if not reasons: reasons.append("Provides a structured NSQF-aligned pathway")
    return {"job_role_id":role.id,"job_role_code":role.job_role_code,"title":role.title,"sector":role.sector,"nsqf_level":role.nsqf_level,"qualification_title":role.qualification_title,"score":round(score,1),"matched_competencies":sorted(matched),"skill_match":round(skill_match,1),"reasons":reasons,"opportunity":None if not opportunity else {"district":opportunity.district,"demand_level":opportunity.demand_level,"demand_count":opportunity.demand_count,"training_capacity":opportunity.training_capacity,"wage_min":opportunity.wage_min,"wage_max":opportunity.wage_max,"source":opportunity.source}}

def match_job_roles(profile, roles, opportunities, top_k=5):
    out=[]
    district=(profile.get("district") or "").lower()
    for role in roles:
        opp=next((o for o in opportunities if o.role_title.lower()==role.title.lower() and (not district or o.district.lower()==district)),None)
        out.append(score_role(profile,role,opp))
    return sorted(out,key=lambda x:x["score"],reverse=True)[:top_k]
