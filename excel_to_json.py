import pandas as pd
import json
import os

# Define the columns you want to include in your JSON output
columns_of_interest = [
    'TaskName',
    'SourceName',
    'RelativeURL',
    'CDCColumn',
    'SelectList',
    'Scope',
    'RawDatabaseName',
    'RawStageSchemaName',
    'RawStageTableName',
    'RawFinalTableName',
    'RawStageToRawFinalSQL',
    'DeleteLogicFlag',
    'UpdateDeleteFile',
    "APIClientID",
    "TokenEndpoint",
    "BaseURL",
    "APIClientSecretName",


]

# Assuming a mapping of column names in SelectList to their data types
# This is a placeholder and should be adjusted to match your actual data
data_type_mapping = {
    'default': 'String'  # Example default type, adjust as needed
}

# Specify your Excel file and directory
directory = 'G:\\Other computers\\My Laptop (1)\\Documents\\Apt_Clients\\Sidley_Austin\\Python_Downloads\\Campus API'
src_file_name = 'API_metadata.xlsx'
full_path = os.path.join(directory, src_file_name)

# Load the "Table Names" and "All Tables" tabs
table_names_df = pd.read_excel(full_path, sheet_name='Table Names')
all_tables_df = pd.read_excel(full_path, sheet_name='All Tables')

# Prepare the list for JSON export
config_list = []

# Filter the all_tables_df DataFrame to include only rows where TaskName is in the Table Names list
filtered_all_tables_df = all_tables_df[all_tables_df['TaskName'].isin(table_names_df['TaskName'].unique())]

# Iterate over unique task names in the filtered DataFrame
for task_name in filtered_all_tables_df['TaskName'].unique():
    # Select the first occurrence of the current task name
    task_row = filtered_all_tables_df[filtered_all_tables_df['TaskName'] == task_name].iloc[0]

    # Create a dictionary for the task, including only the columns of interest
    task_dict = {col: task_row[col] for col in columns_of_interest if col in task_row}

    # Hardcode 'UpdateDeleteFile' to an empty string
    task_dict['UpdateDeleteFile'] = ""

    # Generate mappings from SelectList
    select_list = task_row['SelectList'].split(',') if 'SelectList' in task_row and task_row['SelectList'] else []
    mappings = []
    for column in select_list:
        mappings.append({
            "source": {"path": f"['{column.strip()}']"},
            "sink": {
                "name": column.strip().upper(),
                "type": data_type_mapping.get(column.strip(), data_type_mapping['default'])
            }
        })

    # Add the mapping object to the task dictionary
    task_dict['mapping'] = {
        "type": "TabularTranslator",
        "mappings": mappings,
        "collectionReference": "$['value']"
    }

    config_list.append(task_dict)

# Export to JSON
export_file_name = os.path.splitext(src_file_name)[0] + '_config.json'
with open(os.path.join(directory, export_file_name), 'w') as f:
    json.dump(config_list, f, indent=4)
