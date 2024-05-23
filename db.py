from sqlalchemy import create_engine, Column, Integer, Float, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import pandas as pd

Base = declarative_base()


class MedicalRecord(Base):
    __tablename__ = 'medical_records'

    reference_id = Column(String, primary_key=True)
    report_year = Column(Integer)
    diagnosis_category = Column(String)
    diagnosis_sub_category = Column(String)
    treatment_category = Column(String)
    treatment_sub_category = Column(String)
    determination = Column(String)
    treatment_type = Column(String)
    patient_age_range = Column(String)
    patient_gender = Column(Integer)
    findings = Column(Text)
    patient_name = Column(String)
    patient_age = Column(Float)
    patient_phone = Column(String)
    patient_address = Column(String)
    patient_blood_type = Column(String)
    patient_ssn = Column(String)
    patient_insurance_provider = Column(String)
    patient_insurance_number = Column(String)
    patient_emergency_contact = Column(String)
    patient_occupation = Column(String)
    consulting_physician = Column(String)

    metadata_ = relationship(
        "MedicalMetadata", back_populates="medical_record", uselist=False)


class MedicalMetadata(Base):
    __tablename__ = 'medical_metadata'

    reference_id = Column(String, ForeignKey(
        'medical_records.reference_id'), primary_key=True)
    diagnosis_category_aip = Column(Integer)
    diagnosis_category_pip = Column(Integer)
    diagnosis_sub_category_aip = Column(Integer)
    diagnosis_sub_category_pip = Column(Integer)
    treatment_category_aip = Column(Integer)
    treatment_category_pip = Column(Integer)
    treatment_sub_category_aip = Column(Integer)
    treatment_sub_category_pip = Column(Integer)
    determination_aip = Column(Integer)
    determination_pip = Column(Integer)
    treatment_type_aip = Column(Integer)
    treatment_type_pip = Column(Integer)
    patient_age_range_aip = Column(Integer)
    patient_age_range_pip = Column(Integer)
    findings_aip = Column(Integer)
    findings_pip = Column(Integer)
    patient_name_aip = Column(Integer)
    patient_name_pip = Column(Integer)
    patient_age_aip = Column(Integer)
    patient_age_pip = Column(Integer)
    patient_phone_aip = Column(Integer)
    patient_phone_pip = Column(Integer)
    patient_address_aip = Column(Integer)
    patient_address_pip = Column(Integer)
    patient_blood_type_aip = Column(Integer)
    patient_blood_type_pip = Column(Integer)
    patient_ssn_aip = Column(Integer)
    patient_ssn_pip = Column(Integer)
    patient_insurance_provider_aip = Column(Integer)
    patient_insurance_provider_pip = Column(Integer)
    patient_insurance_number_aip = Column(Integer)
    patient_insurance_number_pip = Column(Integer)
    patient_emergency_contact_aip = Column(Integer)
    patient_emergency_contact_pip = Column(Integer)
    patient_occupation_aip = Column(Integer)
    patient_occupation_pip = Column(Integer)
    consulting_physician_aip = Column(Integer)
    consulting_physician_pip = Column(Integer)

    medical_record = relationship("MedicalRecord", back_populates="metadata_")


class Purpose(Base):
    __tablename__ = 'purposes'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('purposes.id'), nullable=True)
    code = Column(Integer)
    aip_code = Column(Integer)
    pip_code = Column(Integer)

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
            parent_id=row['parent_id'],
            code=row['code'],
            aip_code=row['aip_code'],
            pip_code=row['pip_code']
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
