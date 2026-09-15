import re


SKILL_MAP = {
    "electrical_repair": {
        "canonical": "Electrical Repair",
        "category": "Electrical",
        "aliases": [
            "electrical repair",
            "electric repair",
            "electric repairing",
            "electrical repairing",
            "fan repair",
            "repair fan",
            "fix fans",
            "fix fan",
            "motor repair",
            "બિજલી રિપેર",
            "ઇલેક્ટ્રિકલ રિપેર",
            "પંખો રિપેર",
            "बिजली रिपेयर",
            "पंखा रिपेयर",
        ],
    },

    "electrical_wiring": {
        "canonical": "Electrical Wiring",
        "category": "Electrical",
        "aliases": [
            "electrical wiring",
            "electric wiring",
            "wiring",
            "house wiring",
            "wire fitting",
            "વાયરિંગ",
            "ઇલેક્ટ્રિકલ વાયરિંગ",
            "ઘરનું વાયરિંગ",
            "बिजली की वायरिंग",
            "वायरिंग",
        ],
    },

    "tailoring": {
        "canonical": "Tailoring",
        "category": "Apparel",
        "aliases": [
            "tailoring",
            "tailor",
            "stitching",
            "sewing",
            "dress making",
            "કપડાં સીવવા",
            "સિલાઈ",
            "ટેલરિંગ",
            "सिलाई",
            "दर्जी",
            "कपड़े सिलना",
        ],
    },

    "carpentry": {
        "canonical": "Carpentry",
        "category": "Construction",
        "aliases": [
            "carpentry",
            "carpenter",
            "wood work",
            "woodworking",
            "furniture making",
            "લાકડાનું કામ",
            "સુથારી કામ",
            "सुतार",
            "लकड़ी का काम",
            "बढ़ई का काम",
        ],
    },

    "plumbing": {
        "canonical": "Plumbing",
        "category": "Construction",
        "aliases": [
            "plumbing",
            "plumber",
            "pipe fitting",
            "water pipe work",
            "પ્લમ્બિંગ",
            "પાઇપ ફિટિંગ",
            "નળનું કામ",
            "प्लंबिंग",
            "पाइप फिटिंग",
            "नल का काम",
        ],
    },

    "welding": {
        "canonical": "Welding",
        "category": "Manufacturing",
        "aliases": [
            "welding",
            "welder",
            "metal welding",
            "વેલ્ડિંગ",
            "લોખંડ વેલ્ડિંગ",
            "वेल्डिंग",
            "लोहे की वेल्डिंग",
        ],
    },

    "driving": {
        "canonical": "Driving",
        "category": "Transportation",
        "aliases": [
            "driving",
            "driver",
            "car driving",
            "truck driving",
            "auto driving",
            "ડ્રાઇવિંગ",
            "ડ્રાઇવર",
            "गाड़ी चलाना",
            "ड्राइविंग",
            "ड्राइवर",
        ],
    },

    "farming": {
        "canonical": "Farming",
        "category": "Agriculture",
        "aliases": [
            "farming",
            "farmer",
            "agriculture",
            "cultivation",
            "खेती",
            "कृषि",
            "ખેતી",
            "કૃષિ",
        ],
    },
}


def normalize_text(text: str) -> str:
    """
    Basic text normalization.

    Keeps Unicode characters so Gujarati and Hindi
    text can also be processed.
    """
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_skills(text: str):
    """
    Convert natural-language skill descriptions
    into canonical skill concepts.
    """

    normalized_text = normalize_text(text)

    matches = []

    for skill_id, skill_data in SKILL_MAP.items():
        for alias in skill_data["aliases"]:
            if alias.lower() in normalized_text:
                matches.append({
                    "skill_id": skill_id,
                    "canonical": skill_data["canonical"],
                    "category": skill_data["category"],
                    "matched_alias": alias,
                })
                break

    return matches