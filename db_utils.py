import logging
from sqlalchemy import Column, Engine, ForeignKey, Integer, MetaData, String, Table, create_engine, delete, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, case, func
from sqlalchemy.orm import Session
from langchain_community.utilities import SQLDatabase


from config import DB_PATH, PURPOSES_v2, get_purpose_name_by_code

import time

# Import your models
from db import Base, MedicalRecord, MedicalMetadata, Purpose, PBACMedicalRecord

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def check_compliance(access_code, aip, pip):
    return (access_code & pip == 0) and (access_code & aip != 0)


def get_table_info(base, include):
    schema_info = {}
    classes = base.__subclasses__()
    classes = [cls for cls in classes if cls in include]
    for cls in classes:
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

        table_info = {
            'description': table_description,
            'columns': columns_info,
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
        structured_string += "\n"

    return structured_string


def get_session():
    engine = create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def close_session(session):
    session.close()


def filter_results(records, access_code):
    def remove_none(array_of_dicts):
        # Remove key-value pairs where the value is None
        filtered_array = [{k: v for k, v in d.items() if v is not None}
                          for d in array_of_dicts]
        return filtered_array
    filtered_records = []

    for record in records:
        metadata = record.metadata_
        masked_record = {}
        for column in record.__table__.columns:
            column_name = column.name
            aip = getattr(metadata, f"{column_name}_aip", None)
            pip = getattr(metadata, f"{column_name}_pip", None)
            attribute = getattr(record, column_name)
            if aip is not None and pip is not None and attribute is not None:
                if check_compliance(access_code, aip, pip):
                    masked_record[column_name] = attribute
                else:
                    masked_record[column_name] = 'Masked'
            else:
                masked_record[column_name] = getattr(record, column_name)
        filtered_records.append(masked_record)
    return remove_none(filtered_records)


def insert_into_temp_table(session, medical_records):
    try:
        # Delete all entries in TempMedicalRecord
        session.query(PBACMedicalRecord).delete()

        # Iterate through each medical record and create TempMedicalRecord objects
        for medical_record in medical_records:
            temp_medical_record_data = {}

            # Iterate through each column of TempMedicalRecord
            for column in PBACMedicalRecord.__table__.columns:
                # Check if the column exists in the medical record
                if hasattr(medical_record, column.name):
                    # If it exists, add it to the data dictionary
                    temp_medical_record_data[column.name] = getattr(
                        medical_record, column.name)
                else:
                    # If it doesn't exist, assign None to the column in the data dictionary
                    temp_medical_record_data[column.name] = None

            # Create the TempMedicalRecord object with the collected data
            temp_medical_record = PBACMedicalRecord(**temp_medical_record_data)

            # Add the TempMedicalRecord object to the session
            session.add(temp_medical_record)

        # Commit the changes
        session.commit()
        print("Medical records copied successfully to TempMedicalRecord.")
    except Exception as e:
        # Rollback the session if an error occurs
        session.rollback()
        print("An error occurred:", str(e))


def evaluate_sensitivity(records):
    sensitive = False

    # One record
    if type(records) == MedicalRecord:
        records = [records]
        sensitive = True
    # Multiple records
    elif type(records) == list and type(records[0]) == MedicalRecord:
        sensitive = True
    else:
        logging.info(f"Retrieved records are not of parent class. Type: {
                     type(records)}, Record: {records}")

    return sensitive


def execute_text_query(session, query):
    try:
        text_query = text(query)
        result = session.execute(text_query).fetchall()
        return result
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return None


def create_temp_pbac_table(access_purpose):
    try:
        access_code = PURPOSES_v2.get(access_purpose).get('code')
        session = get_session()
        all = session.query(MedicalRecord).all()
        filter_and_insert_records(session, all, access_code)
        session.close()
        logging.info(
            f"Temp. PBAC table for purpose '{access_purpose}' created successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


def filter_and_insert_records(session, records, access_code):
    def remove_none(array_of_dicts):
        # Remove key-value pairs where the value is None
        filtered_array = [{k: v for k, v in d.items() if v is not None}
                          for d in array_of_dicts]
        return filtered_array

    try:
        # Delete all entries in PBACMedicalRecord
        session.query(PBACMedicalRecord).delete()

        # Filter and mask records
        filtered_records = []

        for record in records:
            metadata = record.metadata_
            masked_record = {}
            for column in record.__table__.columns:
                if column.name == 'metadata_':
                    continue
                column_name = column.name
                aip = getattr(metadata, f"{column_name}_aip", None)
                pip = getattr(metadata, f"{column_name}_pip", None)
                attribute = getattr(record, column_name)
                if aip is not None and pip is not None and attribute is not None:
                    if check_compliance(access_code, aip, pip):
                        masked_record[column_name] = attribute
                    else:
                        masked_record[column_name] = 'Masked'
                else:
                    masked_record[column_name] = getattr(record, column_name)
            filtered_records.append(masked_record)

        filtered_records = remove_none(filtered_records)

        # Insert filtered records into PBACMedicalRecord
        for filtered_record in filtered_records:
            temp_medical_record = PBACMedicalRecord(**filtered_record)
            session.add(temp_medical_record)

        # Commit the changes
        session.commit()
        print("Medical records filtered and copied successfully to PBACMedicalRecord.")
    except Exception as e:
        # Rollback the session if an error occurs
        session.rollback()
        print("An error occurred:", str(e))

# Example usage:
# filter_and_insert_records(session, records, access_code)


if __name__ == "__main__":
    create_temp_pbac_table(16)
