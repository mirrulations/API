import psycopg
import os
import json
import logging

# Error classes
class DatabaseConnectionError(Exception):
    pass

class DataRetrievalError(Exception):
    pass



def get_db_connection():
    '''
    Establish connection to the PostgreSQL database
    '''

    try:
        conn = psycopg.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
        logging.info("Database connection successful.")
        return conn

    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        raise DatabaseConnectionError("Database connection failed")


def append_docket_titles(dockets_list, db_conn=None):
    '''
    Append docket titles using docket ids from OpenSearch query results
    '''
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Use provided db_conn or create one for normal operation
    conn = db_conn if db_conn else get_db_connection()
    cursor = conn.cursor()


    try:
        # Extract docket IDs from dockets list
        docket_ids = [item["docketID"] for item in dockets_list]

        # Query to fetch docket titles
        query = """
        SELECT docket_id, docket_title 
        FROM dockets 
        WHERE docket_id = ANY(%s)
        """

        cursor.execute(query, (docket_ids,))

        # Fetch results and format them as JSON
        results = cursor.fetchall()
        docket_titles = {row[0]: row[1] for row in results}

        # Append docket titles to the dockets list
        for item in dockets_list:
            item["docketTitle"] = docket_titles.get(item["docketID"], "Title Not Found")

        dockets_list = [item for item in dockets_list if item["docketTitle"] != "Title Not Found"]

        logging.info("Docket titles successfully appended.")

    except Exception as e:
        logging.error(f"Error executing SQL query: {e}")
        raise DataRetrievalError("Failed to retrieve docket titles")

    finally:
        cursor.close()
        if not db_conn:
            conn.close()
        logging.info("Database connection closed.")

    # Return the updated list, ensuring it is in JSON format
    return json.dumps(dockets_list, indent=None, ensure_ascii=False)