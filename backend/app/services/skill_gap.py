from app.services.competency_mapper import competency_set

def calculate_skill_gap(profile, role):
    existing=competency_set(profile.get("skills",[]))
    required={c.name.strip().lower() for c in role.competencies}
    matched=sorted(existing & required)
    missing=sorted(required-existing)
    return {"matched":matched,"missing":missing,"required_count":len(required),"matched_count":len(matched),"gap_count":len(missing),"coverage":round(len(matched)/len(required)*100,1) if required else 0}
