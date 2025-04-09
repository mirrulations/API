import psycopg
import os
from queries.utils.secrets_manager import get_secret

conn = None
def connect():
    global conn
    if conn is not None: 
        return conn
    secret_name = os.environ.get('DB_SECRET_NAME')
    secret = get_secret(secret_name)

    conn_params = {
        "dbname": secret['db'],
        "user": secret['username'],
        "password": secret['password'],
        "host": secret['host'],
        "port": secret['port'],
    }

    conn = psycopg.connect(**conn_params)
    return conn