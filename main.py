import pandas as pd
import sqlalchemy.exc
from sqlalchemy.engine import URL, create_engine
import struct
from azure.identity import DefaultAzureCredential
from pprint import pprint
from sqlalchemy import text

# connection parameters
server = 'tcp:ods-sql-server-us.database.windows.net'
database = 'salesops-sql-prod-us'
conn_str = (f'DRIVER=ODBC Driver 17 for SQL Server;'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'ENCRYPT=yes;'
            f'TRUSTSERVERCERTIFICATE=no;'
            f'connection timeout=30')
credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
token = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
token_struct = struct.pack(f'<I{len(token)}s', len(token), token)
connection_url = URL.create("mssql+pyodbc",
                            query={"odbc_connect": conn_str})
engine = create_engine(connection_url,
                       connect_args={"attrs_before": {1256: token_struct}})

csv = pd.read_csv(r"C:\Users\asorensen\OneDrive - CVRx Inc\Projects\20240726_Datafactory_salesops_datetime_conversion"
                  r"\attribute list csv.csv")

# obtain all table names
tables = []
for table in csv['NEW TABLES'][1:]:
    if table not in tables:
        tables.append(table)

# connect to the database and iterate through each table
conn = engine.connect()
for table in tables[:-1]:
    with open(r"C:\Users\asorensen\OneDrive - CVRx Inc\Projects\20240726_Datafactory_salesops_datetime_conversion"
              r"\iterate_through_tables\conversion_template.sql") as sql:
        script = sql.read()
    query = script.replace('TABLE_NAME', table)
    try:
        conn.execute(text(query))
        print(f"updating {table}...")
        conn.commit()
    except sqlalchemy.exc.DataError:
        print(f"Error with table {table}.")
conn.close()





