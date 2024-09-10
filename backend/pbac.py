from collections import OrderedDict
from backend.config.model import VisitModel, Response
from backend.config.const import KEYS
import logging

logger = logging.getLogger()

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
    masked_visits = []
    total_masked_fields = 0
    
    for visit in visits:
        masked_visit, masked_fields = mask(visit, access_purpose)
        masked_visits.append(masked_visit)
        total_masked_fields += masked_fields
    
    return masked_visits, total_masked_fields


def filter(action, result, access_purpose: str):
    if action == 'find':
        visits = convert_all(result)
        filtered_visits, total_masked_fields = mask_all(visits, access_purpose)
        result = filtered_visits
        masked = total_masked_fields
        return result
    else:
        return result
    
def verify_query(query: dict) -> bool:
    """
    Verifies that if a field exists in the query string and has a corresponding IP field 
    in the 'ip' list, then that IP field must also be present in the query string.

    Args:
        query (dict): The query dictionary to verify.

    Returns:
        bool: True if the query passes the verification, False otherwise.
    """
    query_str = str(query)

    _, ip_fields, non_ip_fields = VisitModel().get_keys()

    for field in non_ip_fields:
        ip_field = f"{field}_IP"
        if field in query_str and ip_field in ip_fields:
            if ip_field not in query_str:
                error = f"Missing IP field for {field}."
                logger.error(error)
                return False, error
    logger.info(f"Query verified.")
    return True, None

def re_write_query(query: dict, action: str, access_purpose: str) -> dict:
    """
    Rewrite the query by adding _IP fields.
    """

    relevant_keys = []
    query_str = str(query)

    for key in KEYS:
        if key in query_str:
            relevant_keys.append(key)

    if action == 'find' or action == 'countDocuments' or action == 'findOne':
        modified_query = OrderedDict()
        for key in relevant_keys:
            ip_key = f"{key}_IP"
            modified_query[ip_key] = access_purpose
        
        modified_query.update(query)

        return dict(modified_query)
    
    elif action == 'aggregate':
        if not isinstance(query, list):
            raise ValueError(f"For '{action}', the query should be a list of pipeline stages.")

        match_stage = OrderedDict()
        modified_pipeline = []

        for key in relevant_keys:
            ip_key = f"{key}_IP"
            match_stage[ip_key] = access_purpose
        
        if match_stage:
            modified_pipeline.append({ "$match": dict(match_stage) })  # Add the _IP fields in a $match stage

        # Append the original pipeline stages
        modified_pipeline.extend(query)

        return modified_pipeline
    
    else:
        raise ValueError(f"Invalid action: {action}.")
        
if __name__ == "__main__":
    pass
    






