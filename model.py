class AIPModel:
    def __init__(self, 
                 ReportYear=None, 
                 DiagnosisCategory=None, 
                 DiagnosisSubCategory=None, 
                 TreatmentCategory=None, 
                 TreatmentSubCategory=None, 
                 Determination=None, 
                 Type=None, 
                 Findings=None, 
                 AgeRange=None, 
                 PatientAge=None, 
                 PatientGender=None, 
                 PatientName=None, 
                 PatientPhone=None, 
                 PatientAddress=None, 
                 PatientBloodType=None, 
                 PatientSSN=None, 
                 PatientInsuranceProvider=None, 
                 PatientInsuranceNumber=None, 
                 ConsultingPhysician=None):
        self.ReportYear = ReportYear
        self.DiagnosisCategory = DiagnosisCategory
        self.DiagnosisSubCategory = DiagnosisSubCategory
        self.TreatmentCategory = TreatmentCategory
        self.TreatmentSubCategory = TreatmentSubCategory
        self.Determination = Determination
        self.Type = Type
        self.Findings = Findings
        self.AgeRange = AgeRange
        self.PatientAge = PatientAge
        self.PatientGender = PatientGender
        self.PatientName = PatientName
        self.PatientPhone = PatientPhone
        self.PatientAddress = PatientAddress
        self.PatientBloodType = PatientBloodType
        self.PatientSSN = PatientSSN
        self.PatientInsuranceProvider = PatientInsuranceProvider
        self.PatientInsuranceNumber = PatientInsuranceNumber
        self.ConsultingPhysician = ConsultingPhysician

class PIPModel:
    def __init__(self, 
                 ReportYear=None, 
                 DiagnosisCategory=None, 
                 DiagnosisSubCategory=None, 
                 TreatmentCategory=None, 
                 TreatmentSubCategory=None, 
                 Determination=None, 
                 Type=None, 
                 Findings=None, 
                 AgeRange=None, 
                 PatientAge=None, 
                 PatientGender=None, 
                 PatientName=None, 
                 PatientPhone=None, 
                 PatientAddress=None, 
                 PatientBloodType=None, 
                 PatientSSN=None, 
                 PatientInsuranceProvider=None, 
                 PatientInsuranceNumber=None, 
                 ConsultingPhysician=None):
        self.ReportYear = ReportYear
        self.DiagnosisCategory = DiagnosisCategory
        self.DiagnosisSubCategory = DiagnosisSubCategory
        self.TreatmentCategory = TreatmentCategory
        self.TreatmentSubCategory = TreatmentSubCategory
        self.Determination = Determination
        self.Type = Type
        self.Findings = Findings
        self.AgeRange = AgeRange
        self.PatientAge = PatientAge
        self.PatientGender = PatientGender
        self.PatientName = PatientName
        self.PatientPhone = PatientPhone
        self.PatientAddress = PatientAddress
        self.PatientBloodType = PatientBloodType
        self.PatientSSN = PatientSSN
        self.PatientInsuranceProvider = PatientInsuranceProvider
        self.PatientInsuranceNumber = PatientInsuranceNumber
        self.ConsultingPhysician = ConsultingPhysician

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
                 AIP=None, 
                 PIP=None):
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
        self.AIP = AIP if AIP else AIPModel()
        self.PIP = PIP if PIP else PIPModel()

    def to_dict(self):
        return self.__dict__

class Purpose:
    def __init__(self, name, id, parent_id, code, aip_code = 0, pip_code = 0):
        self.name = name
        self.id = id
        self.parent_id = parent_id
        self.code = code
        self.aip_code = aip_code
        self.pip_code = pip_code

    def __repr__(self):
        return f"Name: {self.name}, ID: {self.id}, Parent ID: {self.parent_id}, Code: {self.code}, AIP Code: {self.aip_code}, PIP Code: {self.pip_code}"
    
    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "parent_id": self.parent_id,
            "code": self.code,
            "aip_code": self.aip_code,
            "pip_code": self.pip_code
        }