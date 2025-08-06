import pandas as pd
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

        # --- 2. Load CSV files into pandas DataFrames ---
        # The delimiter is specified as '|' based on the file structure.
        print("Reading CSV files from 'Data' folder...")
        claim_detail_df = pd.read_csv(claim_detail_path, delimiter='|')
        claim_list_df = pd.read_csv(claim_list_path, delimiter='|')
        print("Successfully loaded CSV files.")

        # --- 3. Create a connection to the SQLite database ---
        # This will create the database file if it doesn't exist.
        print(f"Connecting to SQLite database: {db_name}...")
        conn = sqlite3.connect(db_name)
        print("Database connection successful.")

        # --- 4. Write the DataFrames to tables in the database ---
        # 'claim_detail' and 'claim_list' will be the names of the tables.
        # if_exists='replace': If the table already exists, it will be dropped and recreated.
        # index=False: The DataFrame index will not be written into the table as a column.
        print("Writing 'claim_detail_df' to 'claim_detail' table...")
        claim_detail_df.to_sql('claim_detail', conn, if_exists='replace', index=False)
        print("'claim_detail' table created successfully.")

        print("Writing 'claim_list_df' to 'claim_list' table...")
        claim_list_df.to_sql('claim_list', conn, if_exists='replace', index=False)
        print("'claim_list' table created successfully.")

    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure the 'Data' folder exists and contains the CSV files.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # --- 5. Close the database connection ---
        # It's important to close the connection to save the changes.
        if 'conn' in locals() and conn:
            conn.close()
            print(f"Database connection closed. Data has been saved to '{db_name}'.")
            # Provide the absolute path for clarity
            print(f"Database file located at: {os.path.abspath(db_name)}")

# --- Execute the function ---
if __name__ == "__main__":
    push_csv_to_sqlite()
