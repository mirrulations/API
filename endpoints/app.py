import json

def test_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    (Copied from the SAM hello world example. Source: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html)
    """
    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        "body": json.dumps([
            {
                "commentId": "12345",
                "docketId": "EPA-HQ-OAR-2023-0123",
                "commenterName": "John Doe",
                "commentText": "I fully support stricter air quality standards to improve public health.",
                "submittedDate": "2024-01-15"
            },
            {
                "commentId": "67890",
                "docketId": "DOT-OST-2024-0001",
                "commenterName": "Jane Smith",
                "commentText": "Airline passenger rights are long overdue. Please prioritize this rule.",
                "submittedDate": "2024-02-05"
            }
        ]


),
    }