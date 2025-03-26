import os
from dotenv import load_dotenv
import certifi
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

'''
This function creates an OpenSearch client. If the environment variables OPENSEARCH_HOST if OPENSEARCH_PORT are not
set, an error is raised. If the host is set to 'localhost', the client is created with basic authentication. Otherwise,
the client is created with AWS request signing. The function returns the OpenSearch client.

All code that depends on whether we are connecting to a local or production OpenSearch instance is inside of this function.
Outside of the function, interaction with the client is the same regardless of the environment.
'''
def connect():
    load_dotenv()

    host = os.getenv('OPENSEARCH_HOST', 'opensearch-node1')
    port = os.getenv('OPENSEARCH_PORT', '9200')
    region = 'us-east-1'

    if host is None or port is None:
        raise ValueError('Please set the environment variables OPENSEARCH_HOST and OPENSEARCH_PORT')
    
    if host in ['localhost', 'opensearch-node1']:
        auth = ('admin', os.getenv('OPENSEARCH_INITIAL_ADMIN_PASSWORD'))

        ca_certs_path = certifi.where()
        # Create the client with SSL/TLS enabled, but hostname verification disabled.
        client = OpenSearch(
            hosts = [{'host': host, 'port': port}],
            http_compress = True, # enables gzip compression for request bodies
            http_auth = auth,
            use_ssl = False,
            verify_certs = False,
            ssl_assert_hostname = False,
            ssl_show_warn = False,
            ca_certs = ca_certs_path
        )

        return client
    
    service = 'aoss'
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, region, service)

    # Create the client using AWS request signing
    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_compress = True, # enables gzip compression for request bodies
        http_auth=auth,
        use_ssl=True,
        verify_certs=False,
        connection_class=RequestsHttpConnection,
        pool_maxsize=20,
        timeout=60
    )

    return client