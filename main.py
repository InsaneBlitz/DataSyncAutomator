import gspread
from google.cloud import secretmanager
import json
from oauth2client.service_account import ServiceAccountCredentials
import oracledb
import os
import platform
from datetime import datetime

def init_oracle_client():
    """
    Initializes the Oracle client for different operating systems.
    """
    d = None  # Default suitable for Linux
    if platform.system() == "Darwin" and platform.machine() == "x86_64":  # macOS
        d = os.environ.get("HOME") + ("/path/to/instantclient")
    elif platform.system() == "Windows":
        d = r"path\to\oracle\instantclient"  # Update with the actual path
    oracledb.init_oracle_client(lib_dir=d)

print("Starting Script...")
script_start = datetime.now()
print(f"({script_start.strftime('%m/%d/%y %I:%M %p')})")

def getSecret(PROJECT_ID, SECRET_ID, SERVICE_ACCOUNT):
    """
    Retrieves credentials stored in Google Secret Manager.
    """
    try:
        client = secretmanager.SecretManagerServiceClient.from_service_account_file(SERVICE_ACCOUNT)
        secretName = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/latest"
        response = client.access_secret_version(request={"name": secretName})
        secretValues = json.loads(response.payload.data.decode("UTF-8"))
        return secretValues
    except Exception as e:
        print(f"Error occurred while retrieving credentials: {str(e)}")
        return None

def initialize_google_sheets(service_account_file):
    """
    Initializes the connection to Google Sheets API.
    """
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(service_account_file, SCOPES)
    gc = gspread.authorize(credentials)
    return gc

def connect_to_oracle(secret_values):
    """
    Connects to the Oracle database using credentials from Google Secret Manager.
    """
    init_oracle_client()
    try:
        print('Connecting to Oracle database...')
        connection = oracledb.connect(user=secret_values['user'],
                                      password=secret_values['password'],
                                      dsn=secret_values['dsn'])
        return connection
    except oracledb.DatabaseError as e:
        print(f"Error connecting to Oracle: {e}")
        return None

def fetch_data_from_database(oracle_conn, sql_query_path):
    """
    Fetches data from an Oracle database based on a given SQL query.
    """
    print('Gathering data...')
    with open(sql_query_path, 'r') as sqlfile:
        query = sqlfile.read()

    cursor = oracle_conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    column_names = [col[0] for col in cursor.description]
    cursor.close()

    return data, column_names

def get_data_from_spreadsheet(gc, spreadsheet_id, worksheet_name):
    """
    Retrieves data from a specified Google Spreadsheet worksheet.
    """
    try:
        print("Retrieving data from spreadsheet...")
        spreadsheet = gc.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(worksheet_name)
        data = worksheet.get_all_records()
        print(f"Retrieved {len(data)} records.")
        return data
    except Exception as e:
        print(f"Error occurred while connecting to spreadsheet: {str(e)}")
        return None

def generate_oracle_queries(data_from_sheet, data_from_db, column_names):
    """
    Generates Oracle SQL update queries based on data from a Google Spreadsheet and existing database records.
    """
    # Example implementation goes here. Adjust according to your specific logic and data structures.

    queries = []  # List of queries to be executed
    modified_records = []  # List of records to be modified
    # Generate your queries based on comparing 'data_from_sheet' and 'data_from_db'

    return queries, modified_records

def execute_oracle_queries(connection, queries):
    """
    Executes a list of Oracle SQL queries.
    """
    if not queries:
        print("No queries to execute.")
        return

    cursor = connection.cursor()
    try:
        for query in queries:
            cursor.execute(query)
        connection.commit()
        print(f"Executed {len(queries)} queries successfully.")
    except Exception as e:
        print(f"Error executing query: {e}")
        connection.rollback()
    finally:
        cursor.close()

def main():
    """
    Main function to orchestrate the entire process.
    """
    # Placeholder values for project ID and secret ID.
    PROJECT_ID = 'your-google-cloud-project-id'
    SECRET_ID = 'your-secret-id'
    service_account = 'path/to/your/service-account-file.json'

    secret_values = getSecret(PROJECT_ID, SECRET_ID, service_account)
    gc = initialize_google_sheets(service_account)
    oracle_conn = connect_to_oracle(secret_values)

    spreadsheet_id = 'your-spreadsheet-id'
    worksheet_name = 'your-worksheet-name'
    data_from_sheet = get_data_from_spreadsheet(gc, spreadsheet_id, worksheet_name)

    sql_query_path = 'path/to/your/sql-query-file.sql'
    data_from_db, column_names = fetch_data_from_database(oracle_conn, sql_query_path)

    queries, modified_records = generate_oracle_queries(data_from_sheet, data_from_db, column_names)

    if queries:
        execute_oracle_queries(oracle_conn, queries)

    oracle_conn.close()
    print("Script completed.")

if __name__ == "__main__":
    main()
