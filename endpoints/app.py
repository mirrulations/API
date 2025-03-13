import queries.query

def lambda_handler(event, context):
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
    """
    PARAMETER_NAME = "name"
    
    # These headers are always included to fix the CORS Issues
    response = {
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
    }

    
    if event['queryStringParameters'] == None or PARAMETER_NAME not in event['queryStringParameters']:
        response["statusCode"] = 400
        response['body'] = f"Missing query parameter '{PARAMETER_NAME}'"
        return response
    
    search_term =  event['queryStringParameters'][PARAMETER_NAME]

    try:
        body = queries.query.query(search_term)
    except Exception:
        response["statusCode"] = 500
        response['body'] = {"error": "Internal Server Error"}
        return response
    
    if len(body) == 0:
        response["statusCode"] = 404
        response['body'] = "No results for keyword"
        return response

    response["statusCode"] = 200
    response['body'] = body
    return response
