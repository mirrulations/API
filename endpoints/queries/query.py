import os
import psycopg
import boto3
import json

def main():
    # Idea for a local version of this
    # load_dotenv()
    #
    # dbname = os.getenv("POSTGRES_DB")
    # username = os.getenv("POSTGRES_USER")
    # password = os.getenv("POSTGRES_PASSWORD")
    # host = os.getenv("POSTGRES_HOST")
    # port = os.getenv("POSTGRES_PORT")

    client = boto3.client('secretsmanager')

    conn_params = client.get_secret_value(
        SecretId='arn:aws:secretsmanager:us-east-1:936771282063:secret:mirrulationsdb/postgres/master-uA4mKl',
        VersionStage='AWSCURRENT'
    )
    conn_params = json.loads(conn_params["SecretString"])
    conn_params["dbname"] = conn_params["username"]
    del conn_params["engine"]
    del conn_params["dbClusterIdentifier"]

    print(conn_params)
    try:
        conn = psycopg.connect(**conn_params)
        conn.close()
        print("Done!")
    except psycopg.Error as e:
        print(e)

    return 200

if __name__ == "__main__":
    main()