import re


def extract_profile(transcript: str):
    text = transcript.lower()

    profile = {
        "education": None,
        "family_occupation": None,
        "current_livelihood": None,
        "skills": [],
        "interests": [],
        "mobility_constraints": [],
        "employment_preference": None,
        "district": None,
        "state": None,
    }

    # Education
    if "12th" in text or "twelfth" in text:
        profile["education"] = "12th"

    elif "10th" in text or "tenth" in text:
        profile["education"] = "10th"

    elif "graduate" in text or "graduation" in text:
        profile["education"] = "Graduate"

    # Family occupation
    occupations = [
        "electrician",
        "farmer",
        "tailor",
        "carpenter",
        "plumber",
        "driver",
        "mason",
        "welder",
    ]

    for occupation in occupations:
        if occupation in text:
            profile["family_occupation"] = occupation.title()
            break

    # Interests
    interests = [
        "electrical",
        "farming",
        "tailoring",
        "carpentry",
        "plumbing",
        "driving",
        "welding",
        "computer",
    ]

    for interest in interests:
        if interest in text:
            profile["interests"].append(interest.title())

    # Employment preference
    if "business" in text or "self employment" in text:
        profile["employment_preference"] = "self_employment"

    elif "job" in text or "employment" in text:
        profile["employment_preference"] = "wage_employment"

    # Mobility
    mobility_keywords = [
        "cannot travel",
        "can't travel",
        "limited mobility",
        "mobility problem",
        "cannot walk",
    ]

    for keyword in mobility_keywords:
        if keyword in text:
            profile["mobility_constraints"].append(keyword)

    return profile