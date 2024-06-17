import logging

DB_CONTEXT = "The dataset contains detailed records of medical visits from multiple patients, including information about symptoms, diagnoses, treatments, and patient demographics. Each record also includes specific details such as the consulting physician, patient consent for treatments, emergency contacts, and the intended purposes of the medical data."

DB_PATH = 'sqlite:///medical_database.db'

DB_DESCRIPTION = """
Table: medical_records
Description: Table containing This data is from the California Department of Managed Health Care (DMHC). It contains all decisions from Independent Medical Reviews (IMR) administered by the DMHC since January 1, 2001. An IMR is an independent review of a denied, delayed, or modified health care service that the health plan has determined to be not medically necessary, experimental/investigational or non-emergent/urgent. If the IMR is decided in an enrollee's favor, the health plan must authorize the service or treatment requested.
Columns:
  - reference_id (VARCHAR): Unique reference ID for the medical record
  - report_year (INTEGER): Year of the medical report, available options: [2016 2006 2015 2014 2010 2005 2004 2009 2008 2007 2001 2013 2012 2002 2003 2011]
  - diagnosis_category (VARCHAR): Primary diagnosis category, available options: ['Infectious' 'Mental' 'Autism Spectrum' 'Prevention/Good Health' 'Cardiac/Circulatory' 'OB-Gyn / Pregnancy' 'Digestive System / Gastrointestinal' 'Orthopedic / Musculoskeletal' 'Central Nervous System/ Neuromuscular' 'Endocrine/ Metabolic' 'Pediatrics' 'Chronic Pain' 'Respiratory System' 'Cancer' 'Morbid Obesity' 'Ears, Nose, Throat' 'Post Surgical Complication' 'Immunologic' 'Skin' 'Not Applicable' 'Foot' 'Dental' 'Blood Related' 'Genetic' 'Genitourinary/ Kidney' 'Vision' 'Trauma/Injuries' 'Organ Failure' 'Alcohol and Drug Addiction']
  - diagnosis_sub_category (VARCHAR): Sub-category of the diagnosis
  - treatment_category (VARCHAR): Primary treatment category, available options: ['Pharmacy/Prescription Drugs' 'Mental Health Treatment' 'Autism Related Treatment' 'Diagnostic Imaging, Screening and Testing' 'Cardio Vascular' 'Durable Medical Equipment' 'Diagnostic/Physician Evaluation' 'Orthopedic' 'Emergency/Urgent Care' 'General Surgery' 'Acute Medical Services - Outpatient' 'Not Applicable' 'Pain Management' 'Cancer Treatment' 'Reconstructive/Plastic Surgery' 'Rehabilitation Services - Skilled Nursing Facility - Inpatient' 'Special Procedure' 'Electrical/ Thermal/ Radiofreq. Interventions' 'Alternative Treatment' 'OB/GYN Procedures' 'Neurosugery' 'Dental/Orthodontic' 'Home Health Care' 'Acute Medical Services - Inpatient' 'Ear, Nose and Throat Procedures' 'Rehabilitation Services - Outpatient' 'Vision' 'Urology' nan 'Preventive Health Screening' 'Chiropractic' 'Ophthalmology']
  - treatment_sub_category (VARCHAR): Sub-category of the treatment
  - determination (VARCHAR): Indicates if the determination was upheld or overturned, available options: ['Overturned Decision of Health Plan' 'Upheld Decision of Health Plan']
  - treatment_type (VARCHAR): Type of treatment administered, available options: ['Medical Necessity' 'Experimental/Investigational' 'Urgent Care']
  - patient_age_range (VARCHAR): Age range of the patient, available options: ['41-50' '21-30' '0-10' '65+' '51-64' '11_20' '31-40' nan]
  - patient_gender (INTEGER): Gender of the patient, available options: ['Male' 'Female' nan]
  - findings (TEXT): Findings from the medical examination
  - patient_name (VARCHAR): Full name of the patient
  - patient_age (FLOAT): Age of the patient
  - patient_phone (VARCHAR): Phone number of the patient
  - patient_address (VARCHAR): Address of the patient
  - patient_blood_type (VARCHAR): Blood type of the patient, available options: ['A-' 'B+' 'O+' 'AB-' 'O-' 'AB+' 'B-' 'A+']
  - patient_ssn (VARCHAR): Social Security Number of the patient
  - patient_insurance_provider (VARCHAR): Insurance provider of the patient, available options: ['Kaiser Foundation' 'Highmark' 'Anthem Inc.' 'Cigna Health' 'HCSC(Health Care Service Corporation)' 'Molina Healthcare' 'WellCare' 'Medicare' 'Humana' 'UnitedHealth Group' 'Independence Health Group' 'Medicaid' 'CVS Health(Aetna)' 'Blue Cross Blue Shield' 'Centene Corporation' 'GuideWell Mutual Holding']
  - patient_insurance_number (VARCHAR): Insurance number of the patient
  - patient_emergency_contact (VARCHAR): Emergency contact details of the patient
  - patient_occupation (VARCHAR): Occupation of the patient
  - consulting_physician (VARCHAR): Physician who consulted on the case, available options: ['Dr. Jerry Daniels' 'Dr. Eddie Young' 'Dr. Michelle Lamb' 'Dr. Shelly Hunt' 'Dr. Alexandria Gaines' 'Dr. James Barber']
  """

PURPOSES_v2 = {
    "General-Purpose": {
        "id": 1,
        "parent_id": None,
        "code": 1,
        "aip_code": 8191,
        "pip_code": 8191,
        "description": "Root access for all purposes."
    },
    "Clinical-Care": {
        "id": 2,
        "parent_id": 1,
        "code": 2,
        "aip_code": 2,
        "pip_code": 3,
        "description": "Data access for patient clinical care activities and treatment."
    },
    "Research": {
        "id": 3,
        "parent_id": 1,
        "code": 4,
        "aip_code": 124,
        "pip_code": 125,
        "description": "Data access for medical research including public and private."
    },
    "Public-Research": {
        "id": 4,
        "parent_id": 3,
        "code": 8,
        "aip_code": 56,
        "pip_code": 61,
        "description": "Data access for public research activities including military and non-military."
    },
    "Military-Research": {
        "id": 5,
        "parent_id": 4,
        "code": 16,
        "aip_code": 16,
        "pip_code": 29,
        "description": "Data access for military-related medical research."
    },
    "Non-Military-Research": {
        "id": 6,
        "parent_id": 4,
        "code": 32,
        "aip_code": 32,
        "pip_code": 45,
        "description": "Data access for non-military medical research purposes."
    },
    "Private-Research": {
        "id": 7,
        "parent_id": 3,
        "code": 64,
        "aip_code": 64,
        "pip_code": 69,
        "description": "Data access for private sector medical research."
    },
    "Patient-Support-Service": {
        "id": 8,
        "parent_id": 1,
        "code": 128,
        "aip_code": 896,
        "pip_code": 897,
        "description": "Data access for patient support services and care coordination."
    },
    "Billing": {
        "id": 9,
        "parent_id": 8,
        "code": 256,
        "aip_code": 256,
        "pip_code": 385,
        "description": "Data access for billing, insurance, and financial operations."
    },
    "Communication": {
        "id": 10,
        "parent_id": 8,
        "code": 512,
        "aip_code": 512,
        "pip_code": 641,
        "description": "Data access for patient and provider communication, e.g., scheduling appointments."
    },
    "Third-Party": {
        "id": 11,
        "parent_id": 1,
        "code": 1024,
        "aip_code": 7168,
        "pip_code": 7169,
        "description": "Data access for interactions with third-party medical service providers."
    },
    "Marketing": {
        "id": 12,
        "parent_id": 11,
        "code": 2048,
        "aip_code": 2048,
        "pip_code": 3073,
        "description": "Data access for medical marketing and promotional activities."
    },
    "Product-Development": {
        "id": 13,
        "parent_id": 11,
        "code": 4096,
        "aip_code": 4096,
        "pip_code": 5121,
        "description": "Data access for the development and testing of new third-party medical products and services."
    },
    "None": {
        "description": "No specific access purpose identified."
    },
    "Error": {
        "description": "An error occurred please retry."
    }
}

PURPOSES = [
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
    },
    {
        "name": "None",  # do not delete this
        "description": "None of the previous purposes matches. The access purpose is not defined in the input.",
        "code": "None",
        "example": "And how many?"
    },
    {
        "name": "Error",
        "description": "An error occurred please retry.",
        "code": "Error",
        "example": "",
    }
]

PURPOSE_NAMES = [
    "Clinical Care",
    "Research",
    "Billing and Insurance Claims Processing",
    "Patient Support Services",
    "Public Health Monitoring and Response",
    "Clinical Trial Recruitment",
    "Product Development",
    "Marketing",
    "None",  # do not delete this
]

PURPOSE_DESCRIPTIONS = [
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


def get_purpose_data():
    summary = ''
    for name, description, code, example in zip(PURPOSE_NAMES, PURPOSE_DESCRIPTIONS, PURPOSE_CODES, PURPOSE_EXAMPLES):
        summary += f'name: {name}\ndescription: {
            description}\ncode: {code}\nexample: {example}\n\n'
    return summary


def get_purpose_names():
    return list(PURPOSES_v2.keys())


def get_purpose_name_by_code(code):
    for name, info in PURPOSES_v2.items():
        if info.get("code") == code:
            return name
    return "Code not found"


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
