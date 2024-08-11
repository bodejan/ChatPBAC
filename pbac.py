from model import VisitModel, PIPModel, AIPModel, Purpose
from db import find

def get_purposes():
    purposes = {
        'general_purpose': Purpose('General-Purpose', 0, None, 1, 8191, 8191),
        'clinical_care': Purpose('Clinical-Care', 1, 0, 2, 2, 3),
        'research': Purpose('Research', 2, 0, 4, 6244, 6245),
        'patient_support_service': Purpose('Patient-Support-Service', 3, 0, 8, 392, 393),
        'third_party': Purpose('Third-Party', 4, 0, 16, 1552, 1553),
        'public_research': Purpose('Public-Research', 5, 2, 32, 6176, 6181),
        'private_research': Purpose('Private-Research', 6, 2, 64, 64, 69),
        'billing': Purpose('Billing', 7, 3, 128, 128, 137),
        'communication': Purpose('Communication', 8, 3, 256, 256, 265),
        'marketing': Purpose('Marketing', 9, 4, 512, 512, 529),
        'product_development': Purpose('Product-Development', 10, 4, 1024, 1024, 1041),
        'military_research': Purpose('Military-Research', 11, 5, 2048, 2048, 2085),
        'non_military_research': Purpose('Non-Military-Research', 12, 5, 4096, 4096, 4133)
    }

    return purposes

def decode_purposes(encoded_value):
    purposes = get_purposes()
    decoded_purposes = []
    for purpose in purposes.values():
        if encoded_value & purpose.code:
            decoded_purposes.append(purpose.name)
    return decoded_purposes

def verify_access(access_code, aip, pip):
    if type(aip) == int and type(pip) == int:
        return (access_code & pip == 0) and (access_code & aip != 0)
    else:
        return False

def convert(document: list):
    aip_data = document.get('AIP', {})
    pip_data = document.get('PIP', {})
    
    visit = VisitModel(
        ReferenceID=document.get('ReferenceID'),
        ReportYear=document.get('ReportYear'),
        DiagnosisCategory=document.get('DiagnosisCategory'),
        DiagnosisSubCategory=document.get('DiagnosisSubCategory'),
        TreatmentCategory=document.get('TreatmentCategory'),
        TreatmentSubCategory=document.get('TreatmentSubCategory'),
        Determination=document.get('Determination'),
        Type=document.get('Type'),
        AgeRange=document.get('AgeRange'),
        PatientGender=document.get('PatientGender'),
        Findings=document.get('Findings'),
        PatientName=document.get('PatientName'),
        PatientAge=document.get('PatientAge'),
        PatientPhone=document.get('PatientPhone'),
        PatientAddress=document.get('PatientAddress'),
        PatientBloodType=document.get('PatientBloodType'),
        PatientSSN=document.get('PatientSSN'),
        PatientInsuranceProvider=document.get('PatientInsuranceProvider'),
        PatientInsuranceNumber=document.get('PatientInsuranceNumber'),
        ConsultingPhysician=document.get('ConsultingPhysician'),
        AIP=AIPModel(**aip_data),
        PIP=PIPModel(**pip_data)
    )

    return visit

def convert_all(documents: list):
    return [convert(doc) for doc in documents]

def filter(visit: VisitModel, access_code: int, query: dict):
    masked_fields = 0
    for key in list(vars(visit).keys()):
        if key in ['AIP', 'PIP', 'ReferenceID']:
            continue
        aip = getattr(visit.AIP, key, None)
        pip = getattr(visit.PIP, key, None)
        verified = verify_access(access_code, aip, pip)
        if not verified and key in query:
            return None, 0
        elif not verified:
            setattr(visit, key, 'Masked')
            masked_fields += 1

    return visit, masked_fields

def filter_all(visits: list, access_code: int, query: dict):
    filtered_visits = []
    masked_fields = 0
    excluded_documents = 0
    for visit in visits:
        filtered_visit, counter = filter(visit, access_code, query)
        if filtered_visit:
            filtered_visits.append(filtered_visit)
            masked_fields += counter
        else:
            excluded_documents += 1
    
    return filtered_visits, {'masked_fields': masked_fields, 'excluded_documents': excluded_documents}

def run(documents: list, access_code: int, query: dict):
    visits = convert_all(documents)
    filtered_visits, report = filter_all(visits, access_code, query)
    return filtered_visits, report

        
if __name__ == "__main__":
    query = {"DiagnosisSubCategory": 'Obesity'}
    docs = find(query, 100)
    docs, report = run(docs, 2048, query)
    print(report)
    for doc in docs:
        print('---------------------------------')
        if doc:
            print(doc.to_dict())

    






