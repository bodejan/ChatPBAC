from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker


# Import your models
from db import Base, MedicalRecord, MedicalMetadata, Purpose


def get_session():
    # Create an engine and a session
    engine = create_engine('sqlite:///medical_database.db')
    Session = sessionmaker(bind=engine)
    return Session()


def get_medical_record_by_reference_id(session, reference_id):
    return session.query(MedicalRecord).filter_by(reference_id=reference_id).first()


def get_all_purposes(session):
    return session.query(Purpose).all()


def get_medical_metadata_by_reference_id(session, reference_id):
    return session.query(MedicalMetadata).filter_by(reference_id=reference_id).first()


def print_all_medical_records(session):
    records = session.query(MedicalRecord).all()
    for record in records:
        print(record.reference_id, record.patient_name,
              record.diagnosis_category)


def print_all_purposes(session):
    purposes = get_all_purposes(session)
    for purpose in purposes:
        print(purpose.id, purpose.code, purpose.aip_code, purpose.pip_code)


def get_schema_info(base):
    schema_info = {}
    for cls in base.__subclasses__():
        # Get the table comment
        table_description = cls.__table__.comment if cls.__table__.comment else ''

        columns_info = {}
        for column in cls.__table__.columns:
            # Get the column comment
            column_description = column.comment if column.comment else ''
            columns_info[column.name] = {
                'type': str(column.type),
                'description': column_description
            }

        relationships_info = {}
        for rel in cls.__mapper__.relationships:
            # Get the relationship comment from the info dictionary
            rel_description = rel.info.get('description', '')
            relationships_info[rel.key] = {
                'description': rel_description
            }

        table_info = {
            'description': table_description,
            'columns': columns_info,
            'relationships': relationships_info
        }
        schema_info[cls.__tablename__] = table_info

    # Format the schema information as a structured string
    structured_string = ""
    for table, info in schema_info.items():
        structured_string += f"Table: {table}\n"
        structured_string += f"Description: {info['description']}\n"
        structured_string += "Columns:\n"
        for column_name, column_info in info['columns'].items():
            structured_string += f"  - {column_name} ({column_info['type']}): {
                column_info['description']}\n"
        structured_string += "Relationships:\n"
        for rel_name, rel_info in info['relationships'].items():
            structured_string += f"  - {rel_name}: {rel_info['description']}\n"
        structured_string += "\n"

    return structured_string


def close_session(session):
    session.close()


if __name__ == "__main__":

    session = get_session()

    try:
        """ # Example usage
        reference_id = 'MN16-22639'

        medical_record = get_medical_record_by_reference_id(
            session, reference_id)
        if medical_record:
            print(f"Medical Record for {reference_id}:")
            print(medical_record.patient_name,
                  medical_record.diagnosis_category)

        print("All Purposes:")
        print_all_purposes(session)

        print("All Medical Records:")
        print_all_medical_records(session) """
        print(get_schema_info(Base))
    finally:
        # Close the session
        close_session(session)
