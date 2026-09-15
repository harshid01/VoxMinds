def build_roadmap(profile, recommendation, gap):
    role=recommendation["title"]
    self_emp=profile.get("employment_preference")=="self_employment"
    steps=[
      {"stage":1,"title":"Profile validated","status":"completed","action":"Confirm your education, experience, location and existing skills."},
      {"stage":2,"title":"Skill-gap assessment","status":"completed","action":f"Your current competency coverage is {gap['coverage']}%."},
      {"stage":3,"title":"NSQF-aligned pathway","status":"current","action":f"Target job role: {role}. Verify the official qualification and training provider before enrolment."},
      {"stage":4,"title":"Training & practice","status":"next","action":f"Build the missing competencies: {', '.join(gap['missing'][:4]) or 'role-specific advanced competencies'}."},
      {"stage":5,"title":"Certification / assessment","status":"next","action":"Complete assessment and certification through an authorized pathway."},
    ]
    if self_emp:
        steps += [{"stage":6,"title":"Enterprise readiness","status":"next","action":"Prepare equipment, startup budget, customer segment and local market plan."},{"stage":7,"title":"Livelihood launch","status":"next","action":"Start or expand the enterprise and record outcomes."}]
    else:
        steps += [{"stage":6,"title":"Placement readiness","status":"next","action":"Create a verified profile and connect to suitable local employers or opportunities."},{"stage":7,"title":"Livelihood outcome","status":"next","action":"Track placement, retention and income outcome."}]
    return steps
