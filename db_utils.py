import logging
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


from config import DB_PATH, PURPOSES

from db import MedicalRecord, PBACMedicalRecord

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
            structured_string += f"  - {column_name} ({column_info['type']}): {column_info['description']}\n"
        structured_string += "\n"

    return structured_string


def get_session():
    engine = create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def close_session(session):
    session.close()


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
        access_code = PURPOSES.get(access_purpose).get('code')
        session = get_session()
        all = session.query(MedicalRecord).all()
        filter_and_insert_records(session, all, access_code)
        logging.info(
            f"Temp. PBAC table for purpose '{access_purpose}' successfully created.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        session.close()


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
    except Exception as e:
        # Rollback the session if an error occurs
        session.rollback()
        print("An error occurred:", str(e))


def create_sql_db():
    # Step 1: Load your CSV data into a pandas DataFrame
    csv_file_path = 'ex_ante/california_fake.csv'
    df = pd.read_csv(csv_file_path)
    print(df.head())

    # Step 2: Create a SQLite database connection
    database_path = 'sqlite_medical_neo.db'
    conn = sqlite3.connect(database_path)

    # Step 3: Write the data into the SQLite database
    table_name = 'medical_data'  # Name the table in which to store the data
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Close the database connection
    conn.close()

    print(f"Data from {csv_file_path} has been written to {database_path} in the table {table_name}.")


if __name__ == "__main__":
    create_temp_pbac_table(16)
