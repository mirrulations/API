from queries.query import search
import json

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
    PARAMETER_NAME = "searchTerm"
    
    # These headers are always included to fix the CORS Issues
    response = {
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
    }

    if 'queryStringParameters' not in event or event['queryStringParameters'] == None or PARAMETER_NAME not in event['queryStringParameters']:
        response["statusCode"] = 400
        response['body'] = f"Bad request: Missing query parameter '{PARAMETER_NAME}'"
        return response
    
    if event['headers'] == None:
        response["statusCode"] = 400
        response['body'] = "Bad request: missing header"
        return response
    
    query_parameters = event['queryStringParameters']
    header = event['headers']
    
    input_json = {
        "searchTerm": query_parameters["searchTerm"],
        "pageNumber": query_parameters["pageNumber"],
        "refreshResult": query_parameters["refreshResult"],
        "Session-Id": header["Session-Id"],
        "sortParams": query_parameters["sortParams"],
        "filterParams": query_parameters["filterParams"]
    }

    try:
        response_body = search(input_json)
        
    except Exception as e:
        print(f"Exception in database query: {e}")
        response["statusCode"] = 500
        response['body'] = "Internal Server Error"
        return response
    
    if len(response_body["dockets"]) == 0:
        response["statusCode"] = 404
        response['body'] = "No results for keyword"
        return response

    response["statusCode"] = 200
    response['body'] = json.dumps(response_body)
    return response
