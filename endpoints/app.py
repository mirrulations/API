
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
    PARAMETER_NAME = "name"
    
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
    
    if event['header'] == None:
        response["statusCode"] = 400
        response['body'] = "Bad request: missing header"
        return response
    
    if event['body'] == None:
        response["statusCode"] = 400
        response['body'] = "Bad request: missing body"
        return response
    
    query_parameters = event['queryStringParameters']
    header = event['header']
    body = json.dumps(event['body'])

    
    input_json = {
        "searchTerm": query_parameters["searchTerm"],
        "pageNumber": query_parameters["pageNumber"],
        "refreshResult": query_parameters["refreshResults"],
        "sessionID": header["sessionID"],
        "sortParams": body["sortParams"],
        "filterParams": body["filterParams"]
    }

    try:
        # body = search(search_term)
        body = json.dumps([
            {
                "docketId": "BIS-2024-0053",
                "numComments": "70/100",
                "docketTitle": "Public Briefing on Revisions to Space Related Export Controls Under Export Administration Regulations and International Traffic in Arms Regulations",
                "matchQuality": ".85 "
            },
            {
                "docketId": "DOS-2022-0004",
                "numComments": "24/100",
                "docketTitle": "International Traffic in Arms Regulations: Consolidation and Restructuring of Purposes and Definitions",
                "matchQuality": ".6"
            },
            {
                "docketId": "DOS-2010-0194",
                "numComments": "2/50",
                "docketTitle": "2008 - Amendment to the International Arms Traffic in Arms Regulations: Eritrea",
                "matchQuality": ".2"
            }
        ])
    except Exception as e:
        print(f"Exception in database query: {e}")
        response["statusCode"] = 500
        response['body'] = "Internal Server Error"
        return response
    
    if len(body) == 0:
        response["statusCode"] = 404
        response['body'] = "No results for keyword"
        return response

    response["statusCode"] = 200
    response['body'] = body
    return response
