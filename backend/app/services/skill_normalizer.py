SKILL_MAP = {
    "Electrical Repair": {"category":"Electrical", "aliases":["electrical repair","electric repair","motor repair","electrical maintenance","ઇલેક્ટ્રિકલ રિપેર","बिजली मरम्मत"]},
    "Electrical Wiring": {"category":"Electrical", "aliases":["electrical wiring","electric wiring","wiring","house wiring","વાયરિંગ","ઇલેક્ટ્રિકલ વાયરિંગ","बिजली की वायरिंग"]},
    "Tailoring": {"category":"Apparel", "aliases":["tailoring","tailor","sewing","stitching","દરજી કામ","सिलाई"]},
    "Carpentry": {"category":"Construction", "aliases":["carpentry","carpenter","woodwork","furniture making","સુથારી","बढ़ई"]},
    "Plumbing": {"category":"Construction", "aliases":["plumbing","plumber","pipe fitting","પ્લમ્બિંગ","प्लंबिंग"]},
    "Welding": {"category":"Fabrication", "aliases":["welding","welder","metal joining","વેલ્ડિંગ","वेल्डिंग"]},
    "Driving": {"category":"Transport", "aliases":["driving","driver","vehicle driving","ડ્રાઇવિંગ","ड्राइविंग"]},
    "Farming": {"category":"Agriculture", "aliases":["farming","farmer","agriculture","crop cultivation","ખેતી","खेती"]},
    "Computer Basics": {"category":"Digital", "aliases":["computer","computer basics","ms office","digital work","કમ્પ્યુટર","कंप्यूटर"]},
}

def normalize_skills(text: str):
    t = text.lower()
    found=[]
    for canonical, data in SKILL_MAP.items():
        for alias in data["aliases"]:
            if alias.lower() in t:
                found.append({"canonical":canonical,"category":data["category"],"matched_alias":alias})
                break
    return found
