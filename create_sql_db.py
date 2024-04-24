import pandas as pd
import sqlite3

# Step 1: Load your CSV data into a pandas DataFrame
csv_file_path = 'faker/dataset_3.csv'
df = pd.read_csv(csv_file_path)
print(df.head())

# Step 2: Create a SQLite database connection
database_path = 'sqlite_medical.db'
conn = sqlite3.connect(database_path)

# Step 3: Write the data into the SQLite database
table_name = 'medical_data'  # Name the table in which to store the data
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Close the database connection
conn.close()

print(f"Data from {csv_file_path} has been written to {database_path} in the table {table_name}.")
