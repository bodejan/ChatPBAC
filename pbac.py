from model import VisitModel
from db import find

def convert(document: dict):
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
        # IP fields
        ReportYear_IP=document.get('ReportYear_IP'),
        DiagnosisCategory_IP=document.get('DiagnosisCategory_IP'),
        DiagnosisSubCategory_IP=document.get('DiagnosisSubCategory_IP'),
        TreatmentCategory_IP=document.get('TreatmentCategory_IP'),
        TreatmentSubCategory_IP=document.get('TreatmentSubCategory_IP'),
        Determination_IP=document.get('Determination_IP'),
        Type_IP=document.get('Type_IP'),
        AgeRange_IP=document.get('AgeRange_IP'),
        PatientGender_IP=document.get('PatientGender_IP'),
        Findings_IP=document.get('Findings_IP'),
        PatientName_IP=document.get('PatientName_IP'),
        PatientAge_IP=document.get('PatientAge_IP'),
        PatientPhone_IP=document.get('PatientPhone_IP'),
        PatientAddress_IP=document.get('PatientAddress_IP'),
        PatientBloodType_IP=document.get('PatientBloodType_IP'),
        PatientSSN_IP=document.get('PatientSSN_IP'),
        PatientInsuranceProvider_IP=document.get('PatientInsuranceProvider_IP'),
        PatientInsuranceNumber_IP=document.get('PatientInsuranceNumber_IP'),
        ConsultingPhysician_IP=document.get('ConsultingPhysician_IP')
    )

    return visit


def convert_all(documents: list):
    return [convert(doc) for doc in documents]

def mask(visit: VisitModel, access_purpose: str):
    masked_fields = 0
    
    for key in list(vars(visit).keys()):
        # Skip specific keys that don't require masking
        if key.endswith('_IP') or key == 'ReferenceID':
            continue
        
        # Retrieve the corresponding IP field for this key
        ip_field = f"{key}_IP"
        
        # Get the list of intended purposes for this field
        intended_purposes = getattr(visit, ip_field, None)
        
        # Check if the access_purpose is in the list of intended purposes
        if intended_purposes is not None and access_purpose not in intended_purposes:
            setattr(visit, key, 'Masked')
            masked_fields += 1

    return visit, masked_fields


def mask_all(visits: list, access_purpose: str):
    filtered_visits = []
    total_masked_fields = 0
    
    for visit in visits:
        filtered_visit, masked_fields = mask(visit, access_purpose)
        filtered_visits.append(filtered_visit)
        total_masked_fields += masked_fields
    
    return filtered_visits, {'masked_fields': total_masked_fields}


def run_pbac(documents: list, access_purpose: str):
    visits = convert_all(documents)
    filtered_visits, report = mask_all(visits, access_purpose)
    return filtered_visits, report

        
if __name__ == "__main__":
    query = {"DiagnosisSubCategory": 'Obesity'}
    docs = find(query, 100)
    docs, report = run_pbac(docs, 2048, query)
    print(report)
    for doc in docs:
        print('---------------------------------')
        if doc:
            print(doc.to_dict())

    






