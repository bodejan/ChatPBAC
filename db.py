from sqlalchemy import create_engine, Column, Integer, Float, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

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


class Purpose(Base):
    __tablename__ = 'purposes'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('purposes.id'), nullable=True)
    code = Column(Integer)
    aip_code = Column(Integer)
    pip_code = Column(Integer)

    parent = relationship("Purpose", remote_side=[id], backref="children")


# Create an engine
engine = create_engine('sqlite:///medical_records.db')

# Create all tables
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()


# Database setup
engine = create_engine('sqlite:///pbac_complex.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
