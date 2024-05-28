from sqlalchemy import create_engine, Column, Integer, Float, VARCHAR, Text, ForeignKey, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import pandas as pd

Base = declarative_base()


class MedicalRecord(Base):
    __tablename__ = 'medical_records'
    __table_args__ = {
        'comment': "Table containing This data is from the California Department of Managed Health Care (DMHC). It contains all decisions from Independent Medical Reviews (IMR) administered by the DMHC since January 1, 2001. An IMR is an independent review of a denied, delayed, or modified health care service that the health plan has determined to be not medically necessary, experimental/investigational or non-emergent/urgent. If the IMR is decided in an enrollee's favor, the health plan must authorize the service or treatment requested."}

    reference_id = Column(VARCHAR, primary_key=True,
                          comment='Unique reference ID for the medical record')
    report_year = Column(
        Integer, comment='Year of the medical report, available options: [2016 2006 2015 2014 2010 2005 2004 2009 2008 2007 2001 2013 2012 2002 2003 2011]')
    diagnosis_category = Column(VARCHAR, comment="Primary diagnosis category, available options: ['Infectious' 'Mental' 'Autism Spectrum' 'Prevention/Good Health' 'Cardiac/Circulatory' 'OB-Gyn / Pregnancy' 'Digestive System / Gastrointestinal' 'Orthopedic / Musculoskeletal' 'Central Nervous System/ Neuromuscular' 'Endocrine/ Metabolic' 'Pediatrics' 'Chronic Pain' 'Respiratory System' 'Cancer' 'Morbid Obesity' 'Ears, Nose, Throat' 'Post Surgical Complication' 'Immunologic' 'Skin' 'Not Applicable' 'Foot' 'Dental' 'Blood Related' 'Genetic' 'Genitourinary/ Kidney' 'Vision' 'Trauma/Injuries' 'Organ Failure' 'Alcohol and Drug Addiction']")
    diagnosis_sub_category = Column(
        VARCHAR, comment='Sub-category of the diagnosis')
    treatment_category = Column(VARCHAR, comment="Primary treatment category, available options: ['Pharmacy/Prescription Drugs' 'Mental Health Treatment' 'Autism Related Treatment' 'Diagnostic Imaging, Screening and Testing' 'Cardio Vascular' 'Durable Medical Equipment' 'Diagnostic/Physician Evaluation' 'Orthopedic' 'Emergency/Urgent Care' 'General Surgery' 'Acute Medical Services - Outpatient' 'Not Applicable' 'Pain Management' 'Cancer Treatment' 'Reconstructive/Plastic Surgery' 'Rehabilitation Services - Skilled Nursing Facility - Inpatient' 'Special Procedure' 'Electrical/ Thermal/ Radiofreq. Interventions' 'Alternative Treatment' 'OB/GYN Procedures' 'Neurosugery' 'Dental/Orthodontic' 'Home Health Care' 'Acute Medical Services - Inpatient' 'Ear, Nose and Throat Procedures' 'Rehabilitation Services - Outpatient' 'Vision' 'Urology' nan 'Preventive Health Screening' 'Chiropractic' 'Ophthalmology']")
    treatment_sub_category = Column(
        VARCHAR, comment='Sub-category of the treatment')
    determination = Column(
        VARCHAR, comment="Indicates if the determination was upheld or overturned, available options: ['Overturned Decision of Health Plan' 'Upheld Decision of Health Plan']")
    treatment_type = Column(
        VARCHAR, comment="Type of treatment administered, available options: ['Medical Necessity' 'Experimental/Investigational' 'Urgent Care']")
    patient_age_range = Column(
        VARCHAR, comment="Age range of the patient, available options: ['41-50' '21-30' '0-10' '65+' '51-64' '11_20' '31-40' nan]")
    patient_gender = Column(
        Integer, comment="Gender of the patient, available options: ['Male' 'Female' nan]")
    findings = Column(Text, comment='Findings from the medical examination')
    patient_name = Column(VARCHAR, comment='Full name of the patient')
    patient_age = Column(Integer, comment='Age of the patient')
    patient_phone = Column(VARCHAR, comment='Phone number of the patient')
    patient_address = Column(VARCHAR, comment='Address of the patient')
    patient_blood_type = Column(
        VARCHAR, comment="Blood type of the patient, available options: ['A-' 'B+' 'O+' 'AB-' 'O-' 'AB+' 'B-' 'A+']")
    patient_ssn = Column(
        VARCHAR, comment='Social Security Number of the patient')
    patient_insurance_provider = Column(
        VARCHAR, comment="Insurance provider of the patient, available options: ['Kaiser Foundation' 'Highmark' 'Anthem Inc.' 'Cigna Health' 'HCSC(Health Care Service Corporation)' 'Molina Healthcare' 'WellCare' 'Medicare' 'Humana' 'UnitedHealth Group' 'Independence Health Group' 'Medicaid' 'CVS Health(Aetna)' 'Blue Cross Blue Shield' 'Centene Corporation' 'GuideWell Mutual Holding']")
    patient_insurance_number = Column(
        VARCHAR, comment='Insurance number of the patient')
    patient_emergency_contact = Column(
        VARCHAR, comment='Emergency contact details of the patient')
    patient_occupation = Column(VARCHAR, comment='Occupation of the patient')
    consulting_physician = Column(
        VARCHAR, comment="Physician who consulted on the case, available options: ['Dr. Jerry Daniels' 'Dr. Eddie Young' 'Dr. Michelle Lamb' 'Dr. Shelly Hunt' 'Dr. Alexandria Gaines' 'Dr. James Barber']")


class TempMedicalRecord(Base):
    __tablename__ = 'temp_medical_records'
    __table_args__ = {
        'comment': "Table containing This data is from the California Department of Managed Health Care (DMHC). It contains all decisions from Independent Medical Reviews (IMR) administered by the DMHC since January 1, 2001. An IMR is an independent review of a denied, delayed, or modified health care service that the health plan has determined to be not medically necessary, experimental/investigational or non-emergent/urgent. If the IMR is decided in an enrollee's favor, the health plan must authorize the service or treatment requested."}

    reference_id = Column(VARCHAR, ForeignKey('medical_records.reference_id'),
                          primary_key=True, comment='Unique reference ID for the medical record')
    report_year = Column(
        Integer, comment='Year of the medical report, available options: [2016 2006 2015 2014 2010 2005 2004 2009 2008 2007 2001 2013 2012 2002 2003 2011]')
    diagnosis_category = Column(VARCHAR, comment="Primary diagnosis category, available options: ['Infectious' 'Mental' 'Autism Spectrum' 'Prevention/Good Health' 'Cardiac/Circulatory' 'OB-Gyn / Pregnancy' 'Digestive System / Gastrointestinal' 'Orthopedic / Musculoskeletal' 'Central Nervous System/ Neuromuscular' 'Endocrine/ Metabolic' 'Pediatrics' 'Chronic Pain' 'Respiratory System' 'Cancer' 'Morbid Obesity' 'Ears, Nose, Throat' 'Post Surgical Complication' 'Immunologic' 'Skin' 'Not Applicable' 'Foot' 'Dental' 'Blood Related' 'Genetic' 'Genitourinary/ Kidney' 'Vision' 'Trauma/Injuries' 'Organ Failure' 'Alcohol and Drug Addiction']")
    diagnosis_sub_category = Column(
        VARCHAR, comment='Sub-category of the diagnosis')
    treatment_category = Column(VARCHAR, comment="Primary treatment category, available options: ['Pharmacy/Prescription Drugs' 'Mental Health Treatment' 'Autism Related Treatment' 'Diagnostic Imaging, Screening and Testing' 'Cardio Vascular' 'Durable Medical Equipment' 'Diagnostic/Physician Evaluation' 'Orthopedic' 'Emergency/Urgent Care' 'General Surgery' 'Acute Medical Services - Outpatient' 'Not Applicable' 'Pain Management' 'Cancer Treatment' 'Reconstructive/Plastic Surgery' 'Rehabilitation Services - Skilled Nursing Facility - Inpatient' 'Special Procedure' 'Electrical/ Thermal/ Radiofreq. Interventions' 'Alternative Treatment' 'OB/GYN Procedures' 'Neurosugery' 'Dental/Orthodontic' 'Home Health Care' 'Acute Medical Services - Inpatient' 'Ear, Nose and Throat Procedures' 'Rehabilitation Services - Outpatient' 'Vision' 'Urology' nan 'Preventive Health Screening' 'Chiropractic' 'Ophthalmology']")
    treatment_sub_category = Column(
        VARCHAR, comment='Sub-category of the treatment')
    determination = Column(
        VARCHAR, comment="Indicates if the determination was upheld or overturned, available options: ['Overturned Decision of Health Plan' 'Upheld Decision of Health Plan']")
    treatment_type = Column(
        VARCHAR, comment="Type of treatment administered, available options: ['Medical Necessity' 'Experimental/Investigational' 'Urgent Care']")
    patient_age_range = Column(
        VARCHAR, comment="Age range of the patient, available options: ['41-50' '21-30' '0-10' '65+' '51-64' '11_20' '31-40' nan]")
    patient_gender = Column(
        Integer, comment="Gender of the patient, available options: ['Male' 'Female' nan]")
    findings = Column(Text, comment='Findings from the medical examination')
    patient_name = Column(VARCHAR, comment='Full name of the patient')
    patient_age = Column(Integer, comment='Age of the patient')
    patient_phone = Column(VARCHAR, comment='Phone number of the patient')
    patient_address = Column(VARCHAR, comment='Address of the patient')
    patient_blood_type = Column(
        VARCHAR, comment="Blood type of the patient, available options: ['A-' 'B+' 'O+' 'AB-' 'O-' 'AB+' 'B-' 'A+']")
    patient_ssn = Column(
        VARCHAR, comment='Social Security Number of the patient')
    patient_insurance_provider = Column(
        VARCHAR, comment="Insurance provider of the patient, available options: ['Kaiser Foundation' 'Highmark' 'Anthem Inc.' 'Cigna Health' 'HCSC(Health Care Service Corporation)' 'Molina Healthcare' 'WellCare' 'Medicare' 'Humana' 'UnitedHealth Group' 'Independence Health Group' 'Medicaid' 'CVS Health(Aetna)' 'Blue Cross Blue Shield' 'Centene Corporation' 'GuideWell Mutual Holding']")
    patient_insurance_number = Column(
        VARCHAR, comment='Insurance number of the patient')
    patient_emergency_contact = Column(
        VARCHAR, comment='Emergency contact details of the patient')
    patient_occupation = Column(VARCHAR, comment='Occupation of the patient')
    consulting_physician = Column(
        VARCHAR, comment="Physician who consulted on the case, available options: ['Dr. Jerry Daniels' 'Dr. Eddie Young' 'Dr. Michelle Lamb' 'Dr. Shelly Hunt' 'Dr. Alexandria Gaines' 'Dr. James Barber']")

    metadata_ = relationship(
        "MedicalMetadata", back_populates="temp_medical_record", uselist=False, primaryjoin="TempMedicalRecord.reference_id == MedicalMetadata.reference_id")


class MedicalMetadata(Base):
    __tablename__ = 'medical_metadata'
    __table_args__ = {
        'comment': 'Table containing purpose-based access control metadata for medical records; allowed intended purposes (AIP) and prohibited intended purposes (PIP)'}

    reference_id = Column(VARCHAR, ForeignKey('temp_medical_records.reference_id'),
                          primary_key=True, comment='Reference ID linking to the medical record')
    diagnosis_category_aip = Column(
        Integer, comment='Diagnosis category AIP code')
    diagnosis_category_pip = Column(
        Integer, comment='Diagnosis category PIP code')
    diagnosis_sub_category_aip = Column(
        Integer, comment='Diagnosis sub-category AIP code')
    diagnosis_sub_category_pip = Column(
        Integer, comment='Diagnosis sub-category PIP code')
    treatment_category_aip = Column(
        Integer, comment='Treatment category AIP code')
    treatment_category_pip = Column(
        Integer, comment='Treatment category PIP code')
    treatment_sub_category_aip = Column(
        Integer, comment='Treatment sub-category AIP code')
    treatment_sub_category_pip = Column(
        Integer, comment='Treatment sub-category PIP code')
    determination_aip = Column(Integer, comment='Determination AIP code')
    determination_pip = Column(Integer, comment='Determination PIP code')
    treatment_type_aip = Column(Integer, comment='Treatment type AIP code')
    treatment_type_pip = Column(Integer, comment='Treatment type PIP code')
    patient_age_range_aip = Column(
        Integer, comment='Patient age range AIP code')
    patient_age_range_pip = Column(
        Integer, comment='Patient age range PIP code')
    findings_aip = Column(Integer, comment='Findings AIP code')
    findings_pip = Column(Integer, comment='Findings PIP code')
    patient_name_aip = Column(Integer, comment='Patient name AIP code')
    patient_name_pip = Column(Integer, comment='Patient name PIP code')
    patient_age_aip = Column(Integer, comment='Patient age AIP code')
    patient_age_pip = Column(Integer, comment='Patient age PIP code')
    patient_phone_aip = Column(Integer, comment='Patient phone AIP code')
    patient_phone_pip = Column(Integer, comment='Patient phone PIP code')
    patient_address_aip = Column(Integer, comment='Patient address AIP code')
    patient_address_pip = Column(Integer, comment='Patient address PIP code')
    patient_blood_type_aip = Column(
        Integer, comment='Patient blood type AIP code')
    patient_blood_type_pip = Column(
        Integer, comment='Patient blood type PIP code')
    patient_ssn_aip = Column(Integer, comment='Patient SSN AIP code')
    patient_ssn_pip = Column(Integer, comment='Patient SSN PIP code')
    patient_insurance_provider_aip = Column(
        Integer, comment='Patient insurance provider AIP code')
    patient_insurance_provider_pip = Column(
        Integer, comment='Patient insurance provider PIP code')
    patient_insurance_number_aip = Column(
        Integer, comment='Patient insurance number AIP code')
    patient_insurance_number_pip = Column(
        Integer, comment='Patient insurance number PIP code')
    patient_emergency_contact_aip = Column(
        Integer, comment='Patient emergency contact AIP code')
    patient_emergency_contact_pip = Column(
        Integer, comment='Patient emergency contact PIP code')
    patient_occupation_aip = Column(
        Integer, comment='Patient occupation AIP code')
    patient_occupation_pip = Column(
        Integer, comment='Patient occupation PIP code')
    consulting_physician_aip = Column(
        Integer, comment='Consulting physician AIP code')
    consulting_physician_pip = Column(
        Integer, comment='Consulting physician PIP code')

    temp_medical_record = relationship(
        "TempMedicalRecord", back_populates="metadata_")


class Purpose(Base):
    __tablename__ = 'purposes'
    __table_args__ = {
        'comment': 'Table containing purpose codes for medical records'}

    id = Column(Integer, primary_key=True, comment='Primary key')
    name = Column(VARCHAR, comment='Name of the purpose')
    parent_id = Column(Integer, ForeignKey('purposes.id'), nullable=True,
                       comment='Parent purpose ID for hierarchical purposes')
    code = Column(Integer, comment='Purpose code')
    aip_code = Column(Integer, comment='AIP code for the purpose')
    pip_code = Column(Integer, comment='PIP code for the purpose')
    description = Column(VARCHAR, comment='Description of the purpose')

    parent = relationship("Purpose", remote_side=[id], backref="children")


def populate_db():

    # Load data from CSV files
    medical_data = pd.read_csv('ex_ante/california_fake_data.csv')
    metadata_data = pd.read_csv('ex_ante/california_fake_metadata.csv')
    purposes_data = pd.read_csv('ex_ante/california_fake_purposes.csv')

    # Create an SQLite database
    engine = create_engine('sqlite:///medical_database.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Populate the Purposes table
    for index, row in purposes_data.iterrows():
        purpose = Purpose(
            id=row['id'],
            name=row['name'],
            parent_id=row['parent_id'],
            code=row['code'],
            aip_code=row['aip_code'],
            pip_code=row['pip_code'],
            description=row['description']
        )
        session.add(purpose)

    # Populate the MedicalRecord and MedicalMetadata tables
    for index, row in medical_data.iterrows():
        medical_record = MedicalRecord(
            reference_id=row['reference_id'],
            report_year=row['report_year'],
            diagnosis_category=row['diagnosis_category'],
            diagnosis_sub_category=row['diagnosis_sub_category'],
            treatment_category=row['treatment_category'],
            treatment_sub_category=row['treatment_sub_category'],
            determination=row['determination'],
            treatment_type=row['treatment_type'],
            patient_age_range=row['patient_age_range'],
            patient_gender=row['patient_gender'],
            findings=row['findings'],
            patient_name=row['patient_name'],
            patient_age=row['patient_age'],
            patient_phone=row['patient_phone'],
            patient_address=row['patient_address'],
            patient_blood_type=row['patient_blood_type'],
            patient_ssn=row['patient_ssn'],
            patient_insurance_provider=row['patient_insurance_provider'],
            patient_insurance_number=row['patient_insurance_number'],
            patient_emergency_contact=row['patient_emergency_contact'],
            patient_occupation=row['patient_occupation'],
            consulting_physician=row['consulting_physician']
        )
        session.add(medical_record)

    for index, row in metadata_data.iterrows():
        medical_metadata = MedicalMetadata(
            reference_id=row['reference_id'],
            diagnosis_category_aip=row['diagnosis_category_aip'],
            diagnosis_category_pip=row['diagnosis_category_pip'],
            diagnosis_sub_category_aip=row['diagnosis_sub_category_aip'],
            diagnosis_sub_category_pip=row['diagnosis_sub_category_pip'],
            treatment_category_aip=row['treatment_category_aip'],
            treatment_category_pip=row['treatment_category_pip'],
            treatment_sub_category_aip=row['treatment_sub_category_aip'],
            treatment_sub_category_pip=row['treatment_sub_category_pip'],
            determination_aip=row['determination_aip'],
            determination_pip=row['determination_pip'],
            treatment_type_aip=row['treatment_type_aip'],
            treatment_type_pip=row['treatment_type_pip'],
            patient_age_range_aip=row['patient_age_range_aip'],
            patient_age_range_pip=row['patient_age_range_pip'],
            findings_aip=row['findings_aip'],
            findings_pip=row['findings_pip'],
            patient_name_aip=row['patient_name_aip'],
            patient_name_pip=row['patient_name_pip'],
            patient_age_aip=row['patient_age_aip'],
            patient_age_pip=row['patient_age_pip'],
            patient_phone_aip=row['patient_phone_aip'],
            patient_phone_pip=row['patient_phone_pip'],
            patient_address_aip=row['patient_address_aip'],
            patient_address_pip=row['patient_address_pip'],
            patient_blood_type_aip=row['patient_blood_type_aip'],
            patient_blood_type_pip=row['patient_blood_type_pip'],
            patient_ssn_aip=row['patient_ssn_aip'],
            patient_ssn_pip=row['patient_ssn_pip'],
            patient_insurance_provider_aip=row['patient_insurance_provider_aip'],
            patient_insurance_provider_pip=row['patient_insurance_provider_pip'],
            patient_insurance_number_aip=row['patient_insurance_number_aip'],
            patient_insurance_number_pip=row['patient_insurance_number_pip'],
            patient_emergency_contact_aip=row['patient_emergency_contact_aip'],
            patient_emergency_contact_pip=row['patient_emergency_contact_pip'],
            patient_occupation_aip=row['patient_occupation_aip'],
            patient_occupation_pip=row['patient_occupation_pip'],
            consulting_physician_aip=row['consulting_physician_aip'],
            consulting_physician_pip=row['consulting_physician_pip']
        )
        session.add(medical_metadata)

    # Commit the changes
    session.commit()

    # Close the session
    session.close()


if __name__ == '__main__':
    populate_db()
