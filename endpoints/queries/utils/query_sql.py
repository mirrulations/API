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
    Append additional fields using docket ids from OpenSearch query results
    '''
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Use provided db_conn or create one for normal operation
    conn = db_conn if db_conn else get_db_connection()
    cursor = conn.cursor()


    try:
        # Extract docket IDs from dockets list
        docket_ids = [item["id"] for item in dockets_list]

        # Query to fetch docket titles
        query = """
        SELECT d.docket_id, d.docket_title, d.modify_date, a.agency_id, a.agency_name
        FROM dockets d 
        JOIN agencies a 
        ON d.agency_id = a.agency_id 
        WHERE d.docket_id = ANY(%s)
        """

        cursor.execute(query, (docket_ids,))

        # Fetch results and format them as JSON
        results = cursor.fetchall()
        docket_titles = {row[0]: row[1] for row in results}
        modify_dates = {row[0]: row[2].isoformat() for row in results}
        agency_ids = {row[0]: row[3] for row in results}
        agency_names = {row[0]: row[4] for row in results}

        # Append additional fields to the dockets list
        for item in dockets_list:
            item["title"] = docket_titles.get(item["id"], "Title Not Found")
            item["dateModified"] = modify_dates.get(item["id"], "Date Not Found")
            item["agencyID"] = agency_ids.get(item["id"], "Agency Not Found")
            item["agencyName"] = agency_names.get(item["id"], "Agency Name Not Found")

        dockets_list = [item for item in dockets_list if item["title"] != "Title Not Found"]

        logging.info("Successfully appended additional fields.")

    except Exception as e:
        logging.error(f"Error executing SQL query: {e}")
        raise DataRetrievalError("Failed to retrieve additional fields.")

    finally:
        cursor.close()
        if not db_conn:
            conn.close()
        logging.info("Database connection closed.")

    # Return the updated list
    return dockets_list