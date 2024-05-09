import pandas as pd
import os

# Specify the directory and file name of the Excel file
directory = 'G:\\Other computers\\My Laptop (1)\\Documents\\Apt_Clients\\Sidley_Austin\\Python_Downloads\\Campus API'
excel_file = 'API_metadata.xlsx'

# Specify the directory to save the merge SQL files
output_directory = 'G:\Other computers\My Laptop (1)\Documents\Apt_Clients\Sidley_Austin\Snowflake\L&D\MERGE STORED PROCEDURES'


# Load the Excel file into a DataFrame for "Table Names" and "All Tables" tabs
table_names_df = pd.read_excel(os.path.join(directory, excel_file), sheet_name='Table Names')
all_tables_df = pd.read_excel(os.path.join(directory, excel_file), sheet_name='All Tables')

# Initialize the list to store merge statements
merge_statements = []

# Iterate over each table name in the "Table Names" tab
for index, row in table_names_df.iterrows():
    # Extract table name from the 'TaskName' column
    table_name = row['TaskName'].upper()

    # Start building the merge statement
    merge_statement = f'''
MERGE INTO RAW.CAMPUS.{table_name} TGT
USING RAW.CAMPUS_STAGE.{table_name} STG
'''

    # Start building the ON condition for the merge statement
    on_conditions = []
    for col_index, col_row in all_tables_df.iterrows():
        if col_row['TaskName'] == table_name:
            if len(on_conditions) == 0:
                on_conditions.append(f"        ON  IFNULL(TGT.{col_row['Column_Name']}::STRING,'') = IFNULL(STG.{col_row['Column_Name']}::STRING,'')")
            else:
                on_conditions.append(f"        AND IFNULL(TGT.{col_row['Column_Name']}::STRING,'') = IFNULL(STG.{col_row['Column_Name']}::STRING,'')")
    
    # Join the ON conditions and add them to the merge statement
    merge_statement += '\n'.join(on_conditions)

    # Start building the WHEN NOT MATCHED THEN INSERT section of the merge statement
    insert_values = []
    for col_index, col_row in all_tables_df.iterrows():
        if col_row['TaskName'] == table_name:
            insert_values.append(f"\t{col_row['Column_Name']},")
    
    # Join the insert values and add them to the merge statement
    merge_statement += f'''
    
WHEN NOT MATCHED THEN INSERT (
'''

    # Append the insert values to the merge statement
    merge_statement += '\n'.join(insert_values)

    # Add the ETL columns to the insert values
    merge_statement += '''
    ETL_INSERTED_DATE,
    ETL_UPDATED_DATE,
    INSERTED_TASK_KEY,
    UPDATED_TASK_KEY,
    IS_DELETED,
    DELETED_DATE_TIME
)
'''

    # Add the VALUES section to the merge statement
    merge_statement += '''
VALUES (
'''

    # Append the insert values to the merge statement
    merge_statement += '\n'.join([f'\tSTG.{col_row["Column_Name"]},' if col_row['Column_Name'] not in ['ETL_INSERTED_DATE', 'ETL_UPDATED_DATE', 'INSERTED_TASK_KEY', 'UPDATED_TASK_KEY', 'IS_DELETED', 'DELETED_DATE_TIME'] else f'\t{col_row["Column_Name"]},' for col_index, col_row in all_tables_df.iterrows() if col_row['TaskName'] == table_name])

    # Add the ETL columns to the insert values
    merge_statement += f'''
    CURRENT_TIMESTAMP::TIMESTAMP_NTZ(9),
    CURRENT_TIMESTAMP::TIMESTAMP_NTZ(9),
    @TASK_KEY,
    @TASK_KEY,
    FALSE,
    NULL
);
'''

    # Append the merge statement to the list of statements
    merge_statements.append(merge_statement)

    # Save the merge statement to a file in the output directory
    merge_file_path = os.path.join(output_directory, f'merge_campus_{table_name.lower()}.sql')
    with open(merge_file_path, 'w') as merge_file:
        merge_file.write(merge_statement)

# Print the file paths of saved merge statements
for table_name in table_names_df['TaskName'].str.upper():
    print(f'Merge statement for table {table_name} saved to {os.path.join(output_directory, "merge_campus_"f"{table_name}sql")}')
