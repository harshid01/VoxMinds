from app.services.skill_normalizer import normalize_skills

def extract_profile(transcript: str):
    text = transcript.lower()
    p = {"education":None,"family_occupation":None,"current_livelihood":None,"skills":[],"interests":[],"mobility_constraints":[],"employment_preference":None,"district":None,"state":None,"experience_years":None}
    education = [("12th", ["12th","twelfth","higher secondary","बारहवीं","બારમું"]),("10th",["10th","tenth","secondary","दसवीं","દસમું"]),("Graduate",["graduate","graduation","degree","સ્નાતક","स्नातक"])]
    for value, aliases in education:
        if any(a in text for a in aliases): p["education"]=value; break
    occupations=["electrician","farmer","tailor","carpenter","plumber","driver","mason","welder"]
    for x in occupations:
        if x in text: p["family_occupation"]=x.title(); break
    if "farm" in text or "खेती" in text or "ખેતી" in text: p["current_livelihood"]="Agriculture"
    elif "tailor" in text or "sewing" in text or "દરજી" in text: p["current_livelihood"]="Tailoring"
    p["skills"]=[x["canonical"] for x in normalize_skills(transcript)]
    interest_terms={"electrical":"Electrical","solar":"Solar","farming":"Agriculture","tailoring":"Tailoring","carpentry":"Carpentry","plumbing":"Plumbing","welding":"Welding","computer":"Digital Work"}
    p["interests"]=[v for k,v in interest_terms.items() if k in text]
    if any(x in text for x in ["self employment","self-employment","business","own shop","પોતાનો ધંધો","अपना व्यवसाय"]): p["employment_preference"]="self_employment"
    elif any(x in text for x in ["job","employment","salary","નોકરી","नौकरी"]): p["employment_preference"]="wage_employment"
    if any(x in text for x in ["cannot travel","can't travel","limited mobility","mobility problem","ઘરેથી","घर से"]): p["mobility_constraints"].append("limited_travel")
    districts=["ahmedabad","surat","vadodara","rajkot","gandhinagar","bhavnagar","jamnagar","mehsana","anand","kheda"]
    states=["gujarat","maharashtra","rajasthan","madhya pradesh","delhi","uttar pradesh"]
    for d in districts:
        if d in text: p["district"]=d.title(); break
    for st in states:
        if st in text: p["state"]=st.title(); break
    return p
