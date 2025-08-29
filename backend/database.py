import csv
import sqlite3
import os

def push_csv_to_sqlite(db_name='claims.db'):
    """
    Reads two CSV files from a 'Data' subfolder, 'claim_detail_data.csv' and 'claim_list_data.csv',
    and pushes their contents to two separate tables in a single SQLite database.

    Args:
        db_name (str): The name of the SQLite database file to be created.
    """
    try:
        # --- 1. Define File Paths ---
        # This makes the script look for the files in a "Data" sub-directory.
        data_folder = 'Data'
        claim_detail_path = os.path.join(data_folder, 'claim_detail_data.csv')
        claim_list_path = os.path.join(data_folder, 'claim_list_data.csv')

        # --- 2. Load CSV files ---
        print("Reading CSV files from 'Data' folder...")
        
        # Read claim detail data
        claim_detail_data = []
        with open(claim_detail_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='|')
            for row in reader:
                claim_detail_data.append(row)
        
        # Read claim list data
        claim_list_data = []
        with open(claim_list_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='|')
            for row in reader:
                claim_list_data.append(row)
        
        print("Successfully loaded CSV files.")

        # --- 3. Create a connection to the SQLite database ---
        # This will create the database file if it doesn't exist.
        print(f"Connecting to SQLite database: {db_name}...")
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        print("Database connection successful.")

        # --- 4. Create tables and insert data ---
        # Create claim_detail table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS claim_detail (
                id INTEGER PRIMARY KEY,
                claim_id INTEGER,
                denial_reason TEXT,
                cpt_codes TEXT
            )
        ''')
        
        # Insert claim detail data
        print("Writing claim detail data to 'claim_detail' table...")
        for row in claim_detail_data:
            cursor.execute('''
                INSERT OR REPLACE INTO claim_detail (id, claim_id, denial_reason, cpt_codes)
                VALUES (?, ?, ?, ?)
            ''', (row['id'], row['claim_id'], row['denial_reason'], row['cpt_codes']))
        
        print("'claim_detail' table created successfully.")

        # Create claim_list table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS claim_list (
                id INTEGER PRIMARY KEY,
                patient_name TEXT,
                billed_amount REAL,
                paid_amount REAL,
                status TEXT,
                insurer_name TEXT,
                discharge_date TEXT
            )
        ''')
        
        # Insert claim list data
        print("Writing claim list data to 'claim_list' table...")
        for row in claim_list_data:
            cursor.execute('''
                INSERT OR REPLACE INTO claim_list 
                (id, patient_name, billed_amount, paid_amount, status, insurer_name, discharge_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['id'], row['patient_name'], row['billed_amount'], 
                row['paid_amount'], row['status'], row['insurer_name'], row['discharge_date']
            ))
        
        print("'claim_list' table created successfully.")

    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure the 'Data' folder exists and contains the CSV files.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # --- 5. Close the database connection ---
        # It's important to close the connection to save the changes.
        if 'conn' in locals() and conn:
            conn.commit()
            conn.close()
            print(f"Database connection closed. Data has been saved to '{db_name}'.")
            # Provide the absolute path for clarity
            print(f"Database file located at: {os.path.abspath(db_name)}")

# --- Execute the function ---
if __name__ == "__main__":
    push_csv_to_sqlite()
