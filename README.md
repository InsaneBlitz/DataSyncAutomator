# DataSyncAutomator

Automate the synchronization of data from Google Spreadsheets to an Oracle database with Python. `DataSyncAutomator` is designed to fetch data from specified Google Spreadsheet worksheets, perform necessary calculations or data transformations, and update records in an Oracle database accordingly. This script showcases the integration of Google Cloud APIs, Oracle Database operations, and data processing tasks in Python.

## Features

- **Google Sheets API Integration**: Fetch data from specific worksheets in a Google Spreadsheet.
- **Oracle Database Updates**: Update Oracle database records based on data retrieved from Google Sheets.
- **Secure Credential Management**: Leverages Google Cloud Secret Manager for managing sensitive credentials securely.
- **Customizable Data Processing**: Template for custom data transformation and query generation based on spreadsheet data.

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/InsaneBlitz/DataSyncAutomator.git
   ```

2. **Install Required Libraries**:
   Navigate to the repository directory and install the required Python libraries using:
   ```bash
   pip install -r requirements.txt
   ```

3. **Google Cloud Setup**:
   Ensure you have a Google Cloud project with the Secret Manager API and Google Sheets API enabled. Follow the appropriate documentation to set up service accounts and secret keys for both APIs.

4. **Oracle Client Setup**:
   Install the Oracle Instant Client and configure the script to locate the client libraries based on your operating system.

## Configuration

Edit the script to include your Google Cloud project ID, secret IDs for database credentials, service account JSON path, target spreadsheet ID, and worksheet name. Additionally, customize the SQL query file path as needed for your database operations.

## Usage

1. **Execute the Script**:
   Run the script with Python:
   ```bash
   python DataSyncAutomator.py
   ```
   Follow any on-screen prompts to ensure data is fetched and processed as expected.

## Contributing

Contributions to enhance `DataSyncAutomator` are welcome! Please feel free to fork the repository, make your improvements, and submit a pull request.

## License

This project is open-sourced under the MIT License. See the LICENSE file for more details.

## About the Author

This script was created by Alexis, a developer passionate about automating data processes and integrating different technologies to streamline business operations. Check out [InsaneBlitz](https://github.com/InsaneBlitz) for more interesting projects.
