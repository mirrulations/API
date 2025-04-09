import os
import json
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name):
    """
    Retrieve a secret from AWS Secrets Manager
    Args:
        secret_name: Name of the secret to retrieve
    Returns:
        dict: The secret key/value pairs
    """
    region_name = os.environ.get('AWS_REGION', 'us-east-1')

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        # Get the secret value
        response = client.get_secret_value(SecretId=secret_name)
        print(response)

        # Decode and parse the secret string JSON
        if 'SecretString' in response:
            secret = json.loads(response['SecretString'])
            return secret
        else:
            print("Secret not found in expected format")
            raise Exception("Secret not found in expected format")

    except ClientError as e:
        print(f"Error retrieving secret: {str(e)}")
        raise e