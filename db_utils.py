import logging
from sqlalchemy import Column, Integer, String, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, case, func


from config import DB_PATH

import time

# Import your models
from db import Base, MedicalRecord, MedicalMetadata, Purpose

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def check_compliance(access_code, aip, pip):
    return (access_code & pip == 0) and (access_code & aip != 0)


def get_session():
    # Create an engine and a session
    engine = create_engine(DB_PATH)
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


def get_medical_five(session):
    return session.query(MedicalRecord).limit(5).all()


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

# TRY to use as CTE


def filter_accessible_records(records, access_code):
    filtered_records = []

    if type(records) == MedicalRecord:
        records = [records]

    if type(records) == list and type(records[0]) == MedicalRecord:
        for record in records:
            metadata = record.metadata_
            masked_record = {}
            for column in record.__table__.columns:
                column_name = column.name
                aip = getattr(metadata, f"{column_name}_aip", None)
                pip = getattr(metadata, f"{column_name}_pip", None)
                if aip is not None and pip is not None:
                    if check_compliance(access_code, aip, pip):
                        masked_record[column_name] = getattr(
                            record, column_name)
                    else:
                        masked_record[column_name] = 'Masked'
                else:
                    masked_record[column_name] = getattr(record, column_name)
            filtered_records.append(masked_record)
        return filtered_records
    else:
        logging.error("Invalid input type")
        return records


def create_masked_cte(session, access_code):
    def get_compliance_case(column, aip_column, pip_column):
        if aip_column is not None and pip_column is not None:
            return case(
                [(check_compliance(access_code, aip_column, pip_column), column)],
                else_='Masked'
            ).label(column.key)
        else:
            return column

    masked_columns = []
    for column in MedicalRecord.__table__.columns:
        if column.key in MedicalMetadata.__table__.columns.keys():
            aip_column = getattr(MedicalMetadata, f"{column.key}_aip", None)
            pip_column = getattr(MedicalMetadata, f"{column.key}_pip", None)
            masked_columns.append(get_compliance_case(
                getattr(MedicalRecord, column.key), aip_column, pip_column))
        else:
            masked_columns.append(
                getattr(MedicalRecord, column.key).label(column.key))

    cte = session.query(
        # MedicalRecord.reference_id,
        *masked_columns
    ).join(MedicalMetadata, MedicalRecord.reference_id == MedicalMetadata.reference_id).cte(name='masked_records')

    return cte


if __name__ == "__main__":
    start = time.time()
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

        """

        record = session.query(MedicalRecord).all()
        filtered = filter_accessible_records(record, 2)
        print(filtered)
        """ masked_cte = create_masked_cte(session, 2)
        print(masked_cte)

        # Query the masked data
        query = session.query(masked_cte)
        print(query)
        results = query.all()
        print(results) """
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Close the session
        close_session(session)
