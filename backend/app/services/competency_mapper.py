SKILL_COMPETENCY_MAP={
"Electrical Repair":["Electrical Repair","Electrical Maintenance","Electrical Safety"],
"Electrical Wiring":["Electrical Wiring","Domestic Wiring","Electrical Safety"],
"Tailoring":["Sewing","Garment Stitching","Tailoring"],
"Carpentry":["Carpentry","Woodworking","Furniture Making"],
"Plumbing":["Plumbing","Pipe Fitting","Water Supply Systems"],
"Welding":["Welding","Metal Joining","Welding Safety"],
"Driving":["Vehicle Driving","Vehicle Safety","Basic Vehicle Maintenance"],
"Farming":["Agriculture","Crop Cultivation","Farm Operations"],
"Computer Basics":["Digital Literacy","Computer Operations","Office Productivity"]}

def map_skills_to_competencies(skills):
    return [{"skill":s,"competencies":SKILL_COMPETENCY_MAP.get(s,[])} for s in skills]

def competency_set(skills):
    return {c.lower() for m in map_skills_to_competencies(skills) for c in m["competencies"]}
