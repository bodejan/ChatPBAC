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


def close_session(session):
    session.close()


def get_schema_with_comments(engine):
    inspector = inspect(engine)
    schema = []

    for table_name in inspector.get_table_names():
        schema.append(f"Table: {table_name}")

        # Get the table comment
        table_comment = inspector.get_table_comment(table_name).get('text', '')
        if table_comment:
            schema.append(f"  Comment: {table_comment}")

        # Get columns information
        columns = inspector.get_columns(table_name)
        for column in columns:
            column_name = column['name']
            column_type = column['type']
            column_comment = column.get('comment', '')
            column_primary_key = 'Primary Key' if column.get(
                'primary_key', False) else ''
            column_info = f"  Column: {column_name} ({column_type}) {
                column_primary_key}"
            if column_comment:
                column_info += f" - {column_comment}"
            schema.append(column_info)

        schema.append("")  # Add an empty line for better readability

    return "\n".join(schema)


if __name__ == "__main__":

    session = get_session()

    try:
        # Example usage
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
        # print_all_medical_records(session)
    finally:
        # Close the session
        close_session(session)
