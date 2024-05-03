PURPOSE_NAMES =[
    "Clinical Care", 
    "Research",
    "Billing and Insurance Claims Processing",
    "Patient Support Services",
    "Public Health Monitoring and Response",
    "Clinical Trial Recruitment",
    "Product Development",
    "Marketing",
    "None" # do not delete this
]
    
PURPOSE_DESCRIPTIONS =[
    "Facilitates ongoing patient care by providing healthcare providers with comprehensive access to patient histories, diagnoses, treatments, and contact information. This purpose supports informed clinical decisions and personalized care plans.",
    "Supports medical research by allowing access to anonymized patient data, focusing on diagnosis and treatment outcomes. Researchers can study patterns, effectiveness, and potential improvements in healthcare delivery and treatments.",
    "Enables the processing of billing and insurance claims through access to patient insurance information, treatment categories, and patient identifiers. This purpose assists in verifying coverage and submitting claims to insurance providers.",
    "Facilitates the provision of support services to patients, including appointment scheduling, follow-up arrangements, and emergency contact communication. Ensures patients receive timely care and information.",
    "Allows for the monitoring of public health trends and the management of health crises by analyzing aggregated data on diagnoses, treatments, and patient demographics. Supports public health initiatives and emergency response planning.",
    "Supports the identification and recruitment of potential clinical trial participants by matching patient diagnoses and treatments with trial eligibility criteria. Facilitates advancements in medical research and treatment development.",
    "Informs the development of medical products and services by analyzing treatment outcomes, patient demographics, and health conditions. Drives innovation in healthcare solutions tailored to patient needs. Data will be shared with third parties.",
    "Tailors health-related marketing initiatives to patient demographics and conditions, promoting relevant healthcare services, products, and wellness programs. Aims to enhance patient engagement and healthcare outcomes.",
    "None of the previous purposes matches. The access purpose is not defined in the input."
]

PURPOSE_CODES = [
    'Care', 
    'Research', 
    'Insurance', 
    'Support', 
    'Public', 
    'Trial',
    'Product', 
    'Marketing',
    'None'
]

PURPOSE_EXAMPLES = [
    "Summarize the medical history of patient PAP587444 for medical purposes. Only consider the first two visits.",
    "How many available records do I have that can be used for research?",
    "Get all patients that came in third of January, 2017 to process payments.",
    "Give me the data for patient PAP249364 to schedule a follow-up appointment.",
    "How many people were sick in Q1, 2017. For the analysis of public health trends.",
    "I research cancer. Are there any patients I can contact for a trial program?",
    "I want to improve obesity therapies. Are there any patients I can contact to improve our current offering?",
    "How many patients can I contact to promote our new drug?",
    "And how many?"
]
    
PURPOSES= [
    {
        "name": "Clinical Care",
        "description": "Facilitates ongoing patient care by providing healthcare providers with comprehensive access to patient histories, diagnoses, treatments, and contact information. This purpose supports informed clinical decisions and personalized care plans.",
        "code": "Care",
        "example": "Summarize the medical history of patient PAP587444 for medical purposes. Only consider the first two visits."
    },
    {
        "name": "Research",
        "description": "Supports medical research by allowing access to anonymized patient data, focusing on diagnosis and treatment outcomes. Researchers can study patterns, effectiveness, and potential improvements in healthcare delivery and treatments.",
        "code": "Research",
        "example": "How many available records do I have that can be used for research?"
    },
    {
        "name": "Billing and Insurance Claims Processing",
        "description": "Enables the processing of billing and insurance claims through access to patient insurance information, treatment categories, and patient identifiers. This purpose assists in verifying coverage and submitting claims to insurance providers.",
        "code": "Insurance",
        "example": "Get all patients that came in third of January, 2017 to process payments."
    },
    {
        "name": "Patient Support Services",
        "description": "Facilitates the provision of support services to patients, including appointment scheduling, follow-up arrangements, and emergency contact communication. Ensures patients receive timely care and information.",
        "code": "Support",
        "example": "Give me the data for patient PAP249364 to schedule a follow-up appointment."
    },
    {
        "name": "Public Health Monitoring and Response",
        "description": "Allows for the monitoring of public health trends and the management of health crises by analyzing aggregated data on diagnoses, treatments, and patient demographics. Supports public health initiatives and emergency response planning.",
        "code": "Public",
        "example": "How many people were sick in Q1, 2017. For the analysis of public health trends."
    },
    {
        "name": "Clinical Trial Recruitment",
        "description": "Supports the identification and recruitment of potential clinical trial participants by matching patient diagnoses and treatments with trial eligibility criteria. Facilitates advancements in medical research and treatment development.",
        "code": "Trial",
        "example": "I research cancer. Are there any patients I can contact for a trial program?"
    },
    {
        "name": "Product Development",
        "description": "Informs the development of medical products and services by analyzing treatment outcomes, patient demographics, and health conditions. Drives innovation in healthcare solutions tailored to patient needs. Data will be shared with third parties.",
        "code": "Product",
        "example": "I want to improve obesity therapies. Are there any patients I can contact to improve our current offering?"
    },
    {
        "name": "Marketing",
        "description": "Tailors health-related marketing initiatives to patient demographics and conditions, promoting relevant healthcare services, products, and wellness programs. Aims to enhance patient engagement and healthcare outcomes.",
        "code": "Marketing",
        "example": "How many patients can I contact to promote our new drug?"
    }
]

def get_example_purposes():
    summary = ''
    for name, description, code, example in zip(PURPOSE_NAMES, PURPOSE_DESCRIPTIONS, PURPOSE_CODES, PURPOSE_EXAMPLES):
        summary += f'name: {name}\ndescription: {description}\ncode: {code}\nexample: {example}\n\n'
    return summary