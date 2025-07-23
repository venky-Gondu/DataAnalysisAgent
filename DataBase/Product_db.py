import pandas as pd
import sqlite3
import os

# --- Configuration ---
DATABASE_NAME = 'ecommerce_data.db' # Our SQLite database file
CSV_FILES = {
    'product_eligibility': 'D:\DataAnalysisAgent\DataBase\Product-Level Eligibility Table (mapped) - Product-Level Eligibility Table (mapped).csv',
    'product_ad_sales': 'D:\DataAnalysisAgent\DataBase\Product-Level Ad Sales and Metrics (mapped) - Product-Level Ad Sales and Metrics (mapped).csv',
    'product_total_sales': 'D:\DataAnalysisAgent\DataBase\Product-Level Total Sales and Metrics (mapped) - Product-Level Total Sales and Metrics (mapped).csv'
}

# --- Database Schema Definitions ---
# This schema includes the necessary corrections and column renames for ALL tables
SQL_SCHEMAS = {
    'product_eligibility': """
        CREATE TABLE IF NOT EXISTS product_eligibility (
            Product_ID INTEGER,
            Eligibility_Date TEXT,
            Is_Eligible_for_Promo INTEGER,
            message TEXT,
            PRIMARY KEY (Product_ID, Eligibility_Date) -- Composite primary key for eligibility
        );
    """,
    'product_ad_sales': """
        CREATE TABLE IF NOT EXISTS product_ad_sales (
            Product_ID INTEGER,
            date TEXT, -- Keeping date as TEXT
            ad_sales REAL,
            impressions INTEGER,
            ad_spend REAL,
            clicks INTEGER,
            units_sold INTEGER,
            PRIMARY KEY (Product_ID, date) -- Composite primary key for ad sales
        );
    """,
    'product_total_sales': """
        CREATE TABLE IF NOT EXISTS product_total_sales (
            Product_ID INTEGER,
            date TEXT, -- Keeping date as TEXT
            total_sales REAL,
            total_units_ordered INTEGER,
            Profit_Margin REAL, -- Assuming this column might be calculated or derived later
            PRIMARY KEY (Product_ID, date) -- Composite primary key for total sales
        );
    """
}

def create_database_and_tables(db_name, schemas):
    """Creates the SQLite database file and defines tables based on schemas.
       This will drop and recreate tables if they exist.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        for table_name, schema_sql in schemas.items():
            print(f"Creating/Recreating table: {table_name}")
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};") # Ensure clean slate for each table
            cursor.execute(schema_sql)
        conn.commit()
        print(f"Database '{db_name}' and tables created successfully.")
    except sqlite3.Error as e:
        print(f"Database error during table creation: {e}")
    finally:
        if conn:
            conn.close()

def import_csv_to_sqlite(db_name, csv_filepath, table_name):
    """Reads a CSV file into a pandas DataFrame and imports its data into a specified SQLite table."""
    conn = None
    try:
        print(f"\n--- Processing '{csv_filepath}' for table '{table_name}' ---")
        df = pd.read_csv(csv_filepath)

        # --- Data Cleaning/Transformation and Column Renaming ---
        # Perform renames first, so subsequent transformations use new names
        if table_name == 'product_eligibility':
            df.rename(columns={
                'item_id': 'Product_ID',
                'eligibility_datetime_utc': 'Eligibility_Date',
                'eligibility': 'Is_Eligible_for_Promo'
            }, inplace=True)
            df['Is_Eligible_for_Promo'] = df['Is_Eligible_for_Promo'].astype(int)
            df['message'] = df['message'].replace({pd.NA: None, '': None})
            print("DataFrame columns after renaming and initial transformation for product_eligibility:")
            print(df.columns.tolist())

        elif table_name == 'product_ad_sales':
            df.rename(columns={'item_id': 'Product_ID'}, inplace=True)
            print("DataFrame columns after renaming for product_ad_sales:")
            print(df.columns.tolist())

        elif table_name == 'product_total_sales':
            df.rename(columns={'item_id': 'Product_ID'}, inplace=True)
            # Add a dummy Profit_Margin for now if it's not in CSV, or ensure it's handled.
            # Assuming Profit_Margin will be calculated or it's a new column based on a previous schema.
            # If not in CSV, add it with NULLs or a default.
            if 'Profit_Margin' not in df.columns:
                df['Profit_Margin'] = None # Or 0.0, depending on expected default
            print("DataFrame columns after renaming for product_total_sales:")
            print(df.columns.tolist())
            
        conn = sqlite3.connect(db_name)
        df.to_sql(table_name, conn, if_exists='replace', index=False) 
        conn.commit()
        print(f"Successfully imported '{csv_filepath}' into table '{table_name}'.")
    except FileNotFoundError:
        print(f"Error: CSV file not found at '{csv_filepath}'")
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file '{csv_filepath}' is empty.")
    except sqlite3.Error as se:
        print(f"SQLite error during import of '{csv_filepath}' to '{table_name}': {se}")
    except Exception as e:
        print(f"An unexpected error occurred while importing '{csv_filepath}' to '{table_name}': {e}")
    finally:
        if conn:
            conn.close()

def verify_data(db_name, table_name):
    """Verifies data by selecting a few rows from the specified table."""
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
        rows = cursor.fetchall()
        print(f"\n--- First 5 rows from {table_name} in SQLite ---")
        if rows:
            col_names = [description[0] for description in cursor.description]
            print(col_names)
            for row in rows:
                print(row)
            total_rows = cursor.execute(f'SELECT COUNT(*) FROM {table_name}').fetchone()[0]
            print(f"Total rows in {table_name}: {total_rows}")
        else:
            print(f"No data found in {table_name}.")
    except sqlite3.Error as e:
        print(f"Error verifying data in {table_name}: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Remove existing DB for a FULL, clean start to resolve 'file is not a database' error
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print(f"Removed existing database: {DATABASE_NAME}")

    # 1. Create database and tables based on predefined schemas (all tables)
    create_database_and_tables(DATABASE_NAME, SQL_SCHEMAS)

    # 2. Import data from CSVs into pandas DataFrames and then into SQLite (all tables)
    for table_name, csv_path in CSV_FILES.items():
        import_csv_to_sqlite(DATABASE_NAME, csv_path, table_name)

    # 3. Verify data import for all tables
    print("\n--- Verifying data in ALL SQLite tables ---")
    for table_name in CSV_FILES.keys():
        verify_data(DATABASE_NAME, table_name)

    print(f"\nAll CSVs processed. Database '{DATABASE_NAME}' is ready with tables populated.")