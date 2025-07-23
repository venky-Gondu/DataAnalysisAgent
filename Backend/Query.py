import sqlite3
import os




def get_db_schema(db_name):

    conn=None
    schema={}

    try:
        conn=sqlite3.connect(db_name)
        cursor=conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:  # Correct variable name
            table_name = table[0]
            cursor.execute(f'PRAGMA table_info({table_name});')
            columns_info = cursor.fetchall()
            schema[table_name] = [{'name': col[1], 'type': col[2]} for col in columns_info]
        return schema

    except sqlite3.Error as e:
        print(f"error Extracting Schema :{e}")
        return {}
    except Exception as e:
        print(f"other type of Exception: {e}")
    finally:
        if conn:
            conn.close()
import sqlite3

def execute_query(db_name, query):
    if not query:
        return {}

    conn = None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(query)  # use the variable, not a string
        result = cursor.fetchall()
        return result if result else {}
    except sqlite3.Error as e:
        print(f"Error querying database: {e}")
        return {}
    except Exception as e:
        print(f"Other exception occurred: {e}")
        return {}
    finally:
        if conn:
            conn.close()
