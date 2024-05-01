import csv
import os

base = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(base, "sidley_datamart_views.csv"), mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')  # Use tab as the delimiter

    for row in csv_reader:
        table_schema = row['TABLE_SCHEMA']
        table_name = row['TABLE_NAME']
        view_definition = row['VIEW_DEFINITION']

        # Create a new directory for the table schema if it doesn't exist
        schema_dir = os.path.join(base, table_schema)
        os.makedirs(schema_dir, exist_ok=True)

        # Write the view definition to a new .sql file in the schema directory
        with open(os.path.join(schema_dir, f"{table_name}.sql"), mode='w') as sql_file:
            sql_file.write(view_definition)