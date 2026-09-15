id="q8m2a1"
INTERVIEW_QUESTIONS = [
    {
        "field": "education",
        "question": {
            "en": "What is your highest level of education?",
            "hi": "आपकी सबसे उच्च शिक्षा क्या है?",
            "gu": "તમારું સૌથી વધુ શિક્ષણ કેટલું છે?"
        }
    },
    {
        "field": "family_occupation",
        "question": {
            "en": "What traditional or family work does your family do?",
            "hi": "आपके परिवार का पारंपरिक या मुख्य काम क्या है?",
            "gu": "તમારા પરિવારનું પરંપરાગત અથવા મુખ્ય કામ શું છે?"
        }
    },
    {
        "field": "current_livelihood",
        "question": {
            "en": "What work are you currently doing?",
            "hi": "आप अभी कौन सा काम करते हैं?",
            "gu": "તમે હાલમાં કયું કામ કરો છો?"
        }
    },
    {
        "field": "skills",
        "question": {
            "en": "What skills or work experience do you already have?",
            "hi": "आपके पास पहले से कौन-कौन से कौशल या काम का अनुभव है?",
            "gu": "તમારી પાસે પહેલેથી કઈ કુશળતા અથવા કામનો અનુભવ છે?"
        }
    },
    {
        "field": "interests",
        "question": {
            "en": "What type of work are you interested in?",
            "hi": "आप किस प्रकार के काम में रुचि रखते हैं?",
            "gu": "તમને કયા પ્રકારના કામમાં રસ છે?"
        }
    },
    {
        "field": "mobility_constraints",
        "question": {
            "en": "Do you have any difficulty travelling for training or work?",
            "hi": "क्या आपको प्रशिक्षण या काम के लिए यात्रा करने में कोई कठिनाई है?",
            "gu": "શું તમને તાલીમ અથવા કામ માટે મુસાફરી કરવામાં કોઈ મુશ્કેલી છે?"
        }
    },
    {
        "field": "employment_preference",
        "question": {
            "en": "Would you prefer a job or starting your own business?",
            "hi": "आप नौकरी करना पसंद करेंगे या अपना व्यवसाय शुरू करना?",
            "gu": "તમે નોકરી કરવાનું પસંદ કરશો કે પોતાનો વ્યવસાય શરૂ કરશો?"
        }
    },
    {
        "field": "location",
        "question": {
            "en": "Which district and state do you currently live in?",
            "hi": "आप वर्तमान में किस जिले और राज्य में रहते हैं?",
            "gu": "તમે હાલમાં કયા જિલ્લા અને રાજ્યમાં રહો છો?"
        }
    }
]


def get_next_question(profile: dict, language: str = "en"):
    """
    Find the first important profile field that is still missing.
    """

    for item in INTERVIEW_QUESTIONS:
        field = item["field"]

        value = profile.get(field)

        if value is None:
            return {
                "completed": False,
                "field": field,
                "question": item["question"].get(
                    language,
                    item["question"]["en"]
                )
            }

    return {
        "completed": True,
        "field": None,
        "question": None
    }