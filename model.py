import json


class VisitModel:
    def __init__(self, 
                 ReferenceID=None, 
                 ReportYear=None, 
                 DiagnosisCategory=None, 
                 DiagnosisSubCategory=None, 
                 TreatmentCategory=None, 
                 TreatmentSubCategory=None, 
                 Determination=None, 
                 Type=None, 
                 AgeRange=None, 
                 PatientGender=None, 
                 Findings=None, 
                 PatientName=None, 
                 PatientAge=None, 
                 PatientPhone=None, 
                 PatientAddress=None, 
                 PatientBloodType=None, 
                 PatientSSN=None, 
                 PatientInsuranceProvider=None, 
                 PatientInsuranceNumber=None, 
                 ConsultingPhysician=None, 
                 # Intended Purpose fields
                 ReportYear_IP=None, 
                 DiagnosisCategory_IP=None, 
                 DiagnosisSubCategory_IP=None, 
                 TreatmentCategory_IP=None, 
                 TreatmentSubCategory_IP=None, 
                 Determination_IP=None, 
                 Type_IP=None, 
                 AgeRange_IP=None, 
                 PatientGender_IP=None, 
                 Findings_IP=None, 
                 PatientName_IP=None, 
                 PatientAge_IP=None, 
                 PatientPhone_IP=None, 
                 PatientAddress_IP=None, 
                 PatientBloodType_IP=None, 
                 PatientSSN_IP=None, 
                 PatientInsuranceProvider_IP=None, 
                 PatientInsuranceNumber_IP=None, 
                 ConsultingPhysician_IP=None):
        self.ReferenceID = ReferenceID
        self.ReportYear = ReportYear
        self.DiagnosisCategory = DiagnosisCategory
        self.DiagnosisSubCategory = DiagnosisSubCategory
        self.TreatmentCategory = TreatmentCategory
        self.TreatmentSubCategory = TreatmentSubCategory
        self.Determination = Determination
        self.Type = Type
        self.AgeRange = AgeRange
        self.PatientGender = PatientGender
        self.Findings = Findings
        self.PatientName = PatientName
        self.PatientAge = PatientAge
        self.PatientPhone = PatientPhone
        self.PatientAddress = PatientAddress
        self.PatientBloodType = PatientBloodType
        self.PatientSSN = PatientSSN
        self.PatientInsuranceProvider = PatientInsuranceProvider
        self.PatientInsuranceNumber = PatientInsuranceNumber
        self.ConsultingPhysician = ConsultingPhysician
        # IP (Intended Purpose) Fields
        self.ReportYear_IP = ReportYear_IP
        self.DiagnosisCategory_IP = DiagnosisCategory_IP
        self.DiagnosisSubCategory_IP = DiagnosisSubCategory_IP
        self.TreatmentCategory_IP = TreatmentCategory_IP
        self.TreatmentSubCategory_IP = TreatmentSubCategory_IP
        self.Determination_IP = Determination_IP
        self.Type_IP = Type_IP
        self.AgeRange_IP = AgeRange_IP
        self.PatientGender_IP = PatientGender_IP
        self.Findings_IP = Findings_IP
        self.PatientName_IP = PatientName_IP
        self.PatientAge_IP = PatientAge_IP
        self.PatientPhone_IP = PatientPhone_IP
        self.PatientAddress_IP = PatientAddress_IP
        self.PatientBloodType_IP = PatientBloodType_IP
        self.PatientSSN_IP = PatientSSN_IP
        self.PatientInsuranceProvider_IP = PatientInsuranceProvider_IP
        self.PatientInsuranceNumber_IP = PatientInsuranceNumber_IP
        self.ConsultingPhysician_IP = ConsultingPhysician_IP

    def to_dict_all(self):
        return str(self.__dict__)
    
    def to_dict(self):
        """Return a dictionary without the Intended Purpose fields."""
        return {
            "ReferenceID": self.ReferenceID,
            "ReportYear": self.ReportYear,
            "DiagnosisCategory": self.DiagnosisCategory,
            "DiagnosisSubCategory": self.DiagnosisSubCategory,
            "TreatmentCategory": self.TreatmentCategory,
            "TreatmentSubCategory": self.TreatmentSubCategory,
            "Determination": self.Determination,
            "Type": self.Type,
            "AgeRange": self.AgeRange,
            "PatientGender": self.PatientGender,
            "Findings": self.Findings,
            "PatientName": self.PatientName,
            "PatientAge": self.PatientAge,
            "PatientPhone": self.PatientPhone,
            "PatientAddress": self.PatientAddress,
            "PatientBloodType": self.PatientBloodType,
            "PatientSSN": self.PatientSSN,
            "PatientInsuranceProvider": self.PatientInsuranceProvider,
            "PatientInsuranceNumber": self.PatientInsuranceNumber,
            "ConsultingPhysician": self.ConsultingPhysician,
        }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)



class Purpose:
    def __init__(self, name, id, parent_id, code, aip_code = 0, pip_code = 0):
        self.name = name
        self.id = id
        self.parent_id = parent_id
        self.code = code
        self.aip_code = aip_code
        self.pip_code = pip_code



class Context:
    def __init__(self, action = None, query = None, result = [], masked = None):
        self.action = action
        self.query = query
        self.result = result
        self.masked = masked

    def __repr__(self):
        return f'Query: {self.query}, Result: {self.result}'
