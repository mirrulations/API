import os
import json
import boto3
import traceback 

def get_secret(secret_name):
    env = os.getenv("ENVIRONMENT", "").lower()
    print("[DEBUG] ENVIRONMENT from secrets_manager:", env)

    if env == "local":
        try:
            if "postgres" in secret_name:
                return {
                    "username": os.getenv("POSTGRES_USER"),
                    "password": os.getenv("POSTGRES_PASSWORD"),
                    "engine": "postgres",
                    "host": os.getenv("POSTGRES_HOST"),
                    "port": int(os.getenv("POSTGRES_PORT")),
                    "db": os.getenv("POSTGRES_DB")
                }
            elif "opensearch" in secret_name:
                return {
                    "host": os.getenv("OPENSEARCH_HOST"),
                    "port": int(os.getenv("OPENSEARCH_PORT")),
                    "password": os.getenv("OPENSEARCH_INITIAL_ADMIN_PASSWORD")
                }
            else:
                raise ValueError(f"[ERROR] Unknown secret name for local: {secret_name}")
        except Exception as e:
            print(f"[ERROR] Exception while loading local secrets: {e}")
            traceback.print_exc() 
            raise e  

    print("[DEBUG] Fetching secret from AWS Secrets Manager.")
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])

    if "username" in secret:
        return {
            "username": secret["username"],
            "password": secret["password"],
            "engine": secret["engine"],
            "host": secret["host"],
            "port": int(secret["port"]),
            "db": secret.get("db", "postgres")
        }
    else:
        return {
            "host": secret["host"],
            "port": int(secret["port"]),
            "password": secret.get("password")
        }
