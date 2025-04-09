import os
from dotenv import load_dotenv
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

def connect():
    from queries.utils.secrets_manager import get_secret

    env = os.getenv("ENVIRONMENT", "").lower()
    print("[DEBUG] ENVIRONMENT from opensearch:", env)

    if env == 'local':
        print("[DEBUG] Using local environment variables for OpenSearch.")
        load_dotenv()
        host = os.getenv('OPENSEARCH_HOST', 'opensearch-node1')
        port = os.getenv('OPENSEARCH_PORT', '9200')
        password = os.getenv('OPENSEARCH_INITIAL_ADMIN_PASSWORD')

        if not password:
            raise ValueError("Missing OPENSEARCH_INITIAL_ADMIN_PASSWORD in local environment.")

        auth = ('admin', password)
        use_ssl = False
        verify_certs = False
        connection_class = RequestsHttpConnection
    else:
        print("[DEBUG] Using AWS Secrets Manager for OpenSearch.")
        secret_name = os.getenv('OS_SECRET_NAME', 'mirrulationsdb/opensearch/master')
        secret = get_secret(secret_name)
        host = secret.get("host")
        port = secret.get("port")
        region = os.environ.get('AWS_REGION', 'us-east-1')

        auth = AWSV4SignerAuth(boto3.Session().get_credentials(), region, 'aoss')
        use_ssl = True
        verify_certs = False
        connection_class = RequestsHttpConnection

    if not host or not port:
        raise ValueError('Please set the environment variables OPENSEARCH_HOST and OPENSEARCH_PORT')

    client = OpenSearch(
        hosts=[{'host': host, 'port': int(port)}],
        http_compress=True,
        http_auth=auth,
        use_ssl=use_ssl,
        verify_certs=verify_certs,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
        connection_class=connection_class,
        pool_maxsize=20,
        timeout=30
    )

    try:
        print(f"[DEBUG] Attempting to connect to OpenSearch at {host}:{port}")
        client.info(timeout=5)
        print("[DEBUG] Connected successfully")
    except Exception as e:
        print(f"[ERROR] Failed to connect to OpenSearch: {e}")
        raise

    return client
