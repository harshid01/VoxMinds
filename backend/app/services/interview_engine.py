QUESTIONS={
"en":[("education","What is the highest class or qualification you completed?"),("family_occupation","What work or traditional occupation does your family do?"),("current_livelihood","What work are you doing currently?"),("skills","What work or skills are you already comfortable doing?"),("interests","What kind of work would you like to learn or do?"),("mobility_constraints","Do you have any difficulty travelling to a training centre or workplace?"),("employment_preference","Would you prefer a job or to start your own work or business?"),("location","Which district and state do you live in?")],
"hi":[("education","आपने सबसे अधिक कौन सी कक्षा या योग्यता पूरी की है?"),("family_occupation","आपके परिवार का पारंपरिक या वर्तमान काम क्या है?"),("current_livelihood","आप अभी कौन सा काम करते हैं?"),("skills","आपको कौन-कौन से काम या कौशल पहले से आते हैं?"),("interests","आप किस तरह का काम सीखना या करना चाहते हैं?"),("mobility_constraints","क्या आपको प्रशिक्षण केंद्र या काम की जगह जाने में कोई परेशानी है?"),("employment_preference","क्या आप नौकरी करना चाहते हैं या अपना काम/व्यवसाय शुरू करना चाहते हैं?"),("location","आप किस जिले और राज्य में रहते हैं?")],
"gu":[("education","તમે સૌથી વધુ કઈ કક્ષા અથવા લાયકાત પૂર્ણ કરી છે?"),("family_occupation","તમારા પરિવારનું પરંપરાગત અથવા હાલનું કામ શું છે?"),("current_livelihood","તમે હાલમાં કયું કામ કરો છો?"),("skills","તમને પહેલેથી કયા કામ અથવા કુશળતા આવે છે?"),("interests","તમે કયા પ્રકારનું કામ શીખવા અથવા કરવા માંગો છો?"),("mobility_constraints","શું તમને તાલીમ કેન્દ્ર અથવા કામની જગ્યાએ જવામાં કોઈ મુશ્કેલી છે?"),("employment_preference","તમે નોકરી કરવા માંગો છો કે પોતાનો વ્યવસાય શરૂ કરવા માંગો છો?"),("location","તમે કયા જિલ્લા અને રાજ્યમાં રહો છો?")] }

def get_next_question(profile, language="en"):
    for field, question in QUESTIONS.get(language, QUESTIONS["en"]):
        value=profile.get(field)
        missing = value is None or value == "" or (field in {"skills", "interests"} and value == [])
        if missing:
            return {"completed":False,"field":field,"question":question}
    return {"completed":True,"field":None,"question":None}
