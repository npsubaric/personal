import xml.etree.ElementTree as ET
from openpyxl import Workbook

# Define the namespaces used in the XML file
namespaces = {
    'edmx': 'http://docs.oasis-open.org/odata/ns/edmx',
    'edm': 'http://docs.oasis-open.org/odata/ns/edm'
}

# Load and parse the XML file
tree = ET.parse(r"G:\Other computers\My Laptop (1)\Documents\Apt_Clients\Sidley_Austin\Python_Downloads\Campus API\API_metadata.xml")  # Updated file path
root = tree.getroot()

# Create a new workbook
wb = Workbook()

# Create "All Tables" worksheet
ws_all_tables = wb.active
ws_all_tables.title = "All Tables"

# Write column headers for "All Tables" worksheet
ws_all_tables.append(['TaskName', 'SourceName', 'RelativeURL', 'SelectList', 
                      'Scope', 'Column_Name', 'column_id', 'data_type', 
                      'RawFinalTableName', 'RawStageTableName', 'RawDatabaseName', 
                      'RawStageSchemaName', 'CDCColumn', 'RawStageToRawFinalSQL', 
                      'DeleteLogicFlag', 'UpdateDeleteFile', 'APIClientID', 
                      'TokenEndpoint', 'BaseURL', 'APIClientSecretName'])

# Create "Table Names" worksheet
ws_table_names = wb.create_sheet(title="Table Names")
# ws_table_names.append(['TaskName'])

# Find all EntityType elements in the XML
entity_types = root.findall('.//edm:Schema//edm:EntityType', namespaces)

# Iterate through entity types
for entity_type in entity_types:
    entity_type_name = entity_type.attrib.get('Name', '')

    # Extract data from each Property within each EntityType
    properties = entity_type.findall('.//edm:Property', namespaces)

    # Initialize column_id for each entity type
    column_id = 1

    # Track CDC column for each TaskName
    cdc_columns = {}

    # Concatenate column names for SelectList
    select_list = ','.join([property_elem.attrib.get('Name', '') for property_elem in properties])

    # Iterate through properties
    for property_elem in properties:
        TaskName = entity_type.attrib.get('Name', '').upper()
        SourceName = 'API_OAUTH'
        RelativeURL = entity_type.attrib.get('Name', '')
        Scope = 'obj_' + entity_type.attrib.get('Name', '') + ':read'
        Column_Name = property_elem.attrib.get('Name', '')
        # column_id = 
        data_type = property_elem.attrib.get('Type', '').split('.')[-1]
        RawFinalTableName = entity_type.attrib.get('Name', '').upper()
        RawStageTableName = entity_type.attrib.get('Name', '').upper()
        RawDatabaseName = 'RAW'
        RawStageSchemaName = 'CAMPUS_STAGE'

        # Set CDCColumn if column_id is 1, otherwise set to None
        CDCColumn = cdc_columns.get(TaskName) if column_id != 1 else Column_Name
        cdc_columns[TaskName] = CDCColumn

        RawStageToRawFinalSQL = 'merge_campus_' + entity_type.attrib.get('Name', '') + '.sql'
        DeleteLogicFlag = 'N'
        UpdateDeleteFile = ''
        APIClientID = '1l4r3s8a1t6c7'
        TokenEndpoint = 'https://sidleylms-stg.csod.com/services/api/oauth2/token'
        BaseURL = 'https://sidleylms-stg.csod.com/services/api/x/dataexporter/api/objects/'
        APIClientSecretName = 'CornerstoneAPISecret'

        # Write the row to the "All Tables" worksheet
        ws_all_tables.append([TaskName, SourceName, RelativeURL, select_list,
                              Scope, Column_Name, column_id, data_type, 
                              RawFinalTableName, RawStageTableName, RawDatabaseName, 
                              RawStageSchemaName, CDCColumn, RawStageToRawFinalSQL, 
                              DeleteLogicFlag, UpdateDeleteFile, APIClientID, 
                              TokenEndpoint, BaseURL, APIClientSecretName])

        # Increment column_id
        column_id += 1

    # Write task name to "Table Names" worksheet
    # ws_table_names.append([TaskName])

# Save the workbook
wb.save('API_metadata.xlsx')


