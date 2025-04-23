# ----------------------------------------------
# Dictionary: disease_details
# ----------------------------------------------
# This dictionary stores detailed medical information
# for various skin-related diseases. Each key represents
# a disease name, and its value is another dictionary
# containing details such as causes, symptoms,
# medications, and recommended actions.

disease_details = {
    # Chickenpox details
    "Chickenpox": {
        "causes": "Varicella-zoster virus infection.",  # Virus responsible for chickenpox
        "medications": "Antiviral drugs, antihistamines for itching.",  # Common treatments
        "symptoms": "Fever, itchy rash with blisters.",  # Key symptoms
        "what_to_do": "Keep skin clean, avoid scratching, consult doctor if severe."  # Advice for patients
    },

    # Cowpox details
    "Cowpox": {
        "causes": "Cowpox virus infection, transmitted from animals.",  # Animal-transmitted viral infection
        "medications": "Supportive care, antiviral medications if necessary.",  # General management
        "symptoms": "Localized pustular lesions, fever, swollen lymph nodes.",  # Clinical signs
        "what_to_do": "Keep lesions clean, avoid scratching, consult healthcare provider."  # Care suggestions
    },

    # Healthy skin (used when no disease is detected)
    "Healthy": {
        "causes": "N/A",  # Not applicable for healthy skin
        "medications": "N/A",  # No medication needed
        "symptoms": "N/A",  # No symptoms
        "what_to_do": "No action needed."  # No treatment required
    },

    # Hand, Foot and Mouth Disease (HFMD)
    "HFMD": {
        "causes": "Caused by coxsackievirus or enterovirus.",  # Viral source
        "medications": "Pain relievers, fever reducers, topical ointments.",  # Relief-focused treatment
        "symptoms": "Fever, mouth sores, skin rash on hands and feet.",  # Typical indicators
        "what_to_do": "Maintain hydration, rest, avoid spreading infection."  # Home care and prevention
    },

    # Measles (correct spelling)
    "Measles": {
        "causes": "Measles virus infection.",  # Viral infection
        "medications": "Supportive care, vitamin A supplements.",  # Nutrient support and monitoring
        "symptoms": "Fever, cough, runny nose, rash.",  # Initial and visible symptoms
        "what_to_do": "Rest, fluids, isolation to prevent spread."  # Isolation advised
    },

    # Measels (duplicate with typo - included just in case model returns this variant)
    "Measels": {
        "causes": "Measles virus infection.",  # Same as above
        "medications": "Supportive care, vitamin A supplements.",
        "symptoms": "Fever, cough, runny nose, rash.",
        "what_to_do": "Rest, fluids, isolation to prevent spread."
    },

    # Monkeypox details
    "Monkeypox": {
        "causes": "Monkeypox virus infection, transmitted through close contact.",  # Spread via physical proximity
        "medications": "Supportive care, antiviral drugs in severe cases.",  # Treatment based on severity
        "symptoms": "Fever, headache, muscle aches, rash with pustules.",  # Distinct symptom pattern
        "what_to_do": "Isolate patient, maintain hygiene, consult healthcare provider."  # Prevention & care
    },

    # Mpox (alternate name for Monkeypox, recognized in modern medical discussions)
    "Mpox": {
        "causes": "Monkeypox virus infection, transmitted through close contact.",
        "medications": "Supportive care, antiviral drugs in severe cases.",
        "symptoms": "Fever, headache, muscle aches, rash with pustules.",
        "what_to_do": "Isolate patient, maintain hygiene, consult healthcare provider."
    },

    # Normal Skin / No Disease (another healthy label)
    "Normal Skin / No Disease": {
        "causes": "N/A",
        "medications": "N/A",
        "symptoms": "N/A",
        "what_to_do": "No action needed."
    },
}
