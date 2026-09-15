SKILL_COMPETENCY_MAP = {
    "Electrical Repair": [
        "Electrical Repair",
        "Electrical Repair and Maintenance",
        "Electrical Maintenance",
        "Electrical Safety",
    ],
    "Electrical Wiring": [
        "Electrical Wiring",
        "Domestic Wiring",
        "Electrical Safety",
    ],
    "Tailoring": [
        "Sewing",
        "Garment Stitching",
        "Tailoring",
    ],
    "Carpentry": [
        "Carpentry",
        "Woodworking",
        "Furniture Making",
    ],
    "Plumbing": [
        "Plumbing",
        "Pipe Fitting",
        "Water Supply Systems",
    ],
    "Welding": [
        "Welding",
        "Metal Joining",
        "Welding Safety",
    ],
    "Driving": [
        "Vehicle Driving",
        "Vehicle Safety",
        "Basic Vehicle Maintenance",
    ],
    "Farming": [
        "Agriculture",
        "Crop Cultivation",
        "Farm Operations",
    ],
}


def map_skills_to_competencies(skills: list):
    """
    Map canonical beneficiary skills to
    competency concepts.

    Prototype mapping only.
    Official NSQF competency mappings should
    eventually come from verified official sources.
    """

    results = []

    for skill in skills:
        competencies = SKILL_COMPETENCY_MAP.get(
            skill,
            []
        )

        results.append({
            "skill": skill,
            "competencies": competencies,
        })

    return results