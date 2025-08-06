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

        # --- 2. Create a connection to the SQLite database ---
        # This will create the database file if it doesn't exist.
        print(f"Connecting to SQLite database: {db_name}...")
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        print("Database connection successful.")

        # --- 3. Create tables ---
        print("Creating tables...")
        
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
        
        # Create claim_detail table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS claim_detail (
                id INTEGER PRIMARY KEY,
                claim_id INTEGER,
                denial_reason TEXT,
                cpt_codes TEXT
            )
        ''')
        
        # --- 4. Load claim_list data ---
        if os.path.exists(claim_list_path):
            print("Loading claim_list data...")
            with open(claim_list_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='|')
                for row in reader:
                    cursor.execute('''
                        INSERT OR REPLACE INTO claim_list 
                        (id, patient_name, billed_amount, paid_amount, status, insurer_name, discharge_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        int(row['id']),
                        row['patient_name'],
                        float(row['billed_amount']) if row['billed_amount'] else None,
                        float(row['paid_amount']) if row['paid_amount'] else None,
                        row['status'],
                        row['insurer_name'],
                        row['discharge_date']
                    ))
            print("claim_list data loaded successfully.")
        else:
            print(f"Warning: {claim_list_path} not found")

        # --- 5. Load claim_detail data ---
        if os.path.exists(claim_detail_path):
            print("Loading claim_detail data...")
            with open(claim_detail_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='|')
                for row in reader:
                    cursor.execute('''
                        INSERT OR REPLACE INTO claim_detail 
                        (id, claim_id, denial_reason, cpt_codes)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        int(row['id']),
                        int(row['claim_id']),
                        row['denial_reason'],
                        row['cpt_codes']
                    ))
            print("claim_detail data loaded successfully.")
        else:
            print(f"Warning: {claim_detail_path} not found")

        # --- 6. Commit and close ---
        conn.commit()
        conn.close()
        print("Database operations completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    push_csv_to_sqlite()
