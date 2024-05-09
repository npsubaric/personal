import pandas as pd
import os

# Specify the directory and file name of the Excel file
directory = 'G:\\Other computers\\My Laptop (1)\\Documents\\Apt_Clients\\Sidley_Austin\\Python_Downloads\\Campus API'
excel_file = 'API_metadata.xlsx'

# Load the Excel file into a DataFrame for "Table Names" and "All Tables" tabs
table_names_df = pd.read_excel(os.path.join(directory, excel_file), sheet_name='Table Names')
all_tables_df = pd.read_excel(os.path.join(directory, excel_file), sheet_name='All Tables')

# Snowflake data types equivalent dictionary
snowflake_data_types = {
    'DateTimeOffset': 'TIMESTAMP_NTZ(9)',
    'Int32': 'NUMBER(38,0)',
    'String': 'VARCHAR(16777216)',
    'Boolean': 'BOOLEAN',
    'Guid': 'VARCHAR(255)',  # Adjust the length as needed
    'Int64': 'NUMBER(38,0)',
    'Int16': 'NUMBER(38,0)',
    'Decimal': 'DECIMAL',
    'Byte': 'BINARY',  # Adjust the length as needed
    'Double': 'DOUBLE'
}

# Initialize the list to store DDL statements
ddl_statements = []

# Iterate over each table name in the "Table Names" tab
for index, row in table_names_df.iterrows():
    # Extract table name from the 'TaskName' column
    table_name = row['TaskName'].upper()

    # Start building the DDL statement for the final table
    ddl_final_statement = f'CREATE OR REPLACE TABLE RAW.CAMPUS.{table_name} (\n'
    
    # Start building the DDL statement for the staging table
    ddl_stage_statement = f'CREATE OR REPLACE TABLE RAW.CAMPUS_STAGE.{table_name} (\n'

    # Filter the "All Tables" DataFrame to include only the current table's columns
    columns_df = all_tables_df[all_tables_df['TaskName'] == table_name]

    # Initialize lists to store column definitions for final and staging tables
    column_definitions_final = []
    column_definitions_stage = []

    # Iterate over each column in the filtered DataFrame
    for col_index, col_row in columns_df.iterrows():
        column_name = col_row['Column_Name']
        data_type = col_row['data_type']

        # Map the data type to the corresponding Snowflake data type
        snowflake_data_type = snowflake_data_types.get(data_type, 'VARCHAR(255)')

        # Add column definitions to the lists for final and staging tables
        column_definitions_final.append(f'\t{column_name} {snowflake_data_type}')
        column_definitions_stage.append(f'\t{column_name} {snowflake_data_type}')

    # Concatenate all column definitions into single strings for final and staging tables
    ddl_final_statement += ',\n'.join(column_definitions_final)
    ddl_stage_statement += ',\n'.join(column_definitions_stage)

    # Add closing parentheses to the DDL statements for final and staging tables
    ddl_final_statement += ',' + '''
    ETL_INSERTED_DATE TIMESTAMP_NTZ(9),
    ETL_UPDATED_DATE TIMESTAMP_NTZ(9),
    INSERTED_TASK_KEY NUMBER(38,0),
    UPDATED_TASK_KEY NUMBER(38,0),
    IS_DELETED BOOLEAN,
    DELETED_DATE_TIME TIMESTAMP_NTZ(9)
);\n'''
    ddl_stage_statement += '\n);\n'

    # Append the DDL statements for final and staging tables to the list of statements
    ddl_statements.append(ddl_final_statement)
    ddl_statements.append(ddl_stage_statement)

# Save DDL statements to a .sql file
ddl_file_path = os.path.join(directory, 'CAMPUS_DDL.sql')
with open(ddl_file_path, 'w') as ddl_file:
    ddl_file.write('\n'.join(ddl_statements))
