from queries.query import search
import json

def lambda_handler(event, context):
    PARAMETER_NAME = "searchTerm"

    # Initialize default response object
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Accept,Origin,session-id",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Origin": "*"  # This will be updated dynamically
        },
        "body": ""
    }

    # Determine the origin for CORS
    origin = event['headers'].get("origin", "*")
    if origin in ["https://mirrulations.com", "https://mirrulations.org"]:
        allow_origin = origin
    else:
        allow_origin = "https://mirrulations.com"
    response["headers"]["Access-Control-Allow-Origin"] = allow_origin

    # Handle CORS preflight request
    if event['httpMethod'] == 'OPTIONS':
        return response

    # Validate query parameters
    if 'queryStringParameters' not in event or event['queryStringParameters'] is None or PARAMETER_NAME not in event['queryStringParameters']:
        response["statusCode"] = 400
        response["body"] = json.dumps({"error": f"Bad request: Missing query parameter '{PARAMETER_NAME}'"})
        return response

    if event['headers'] is None:
        response["statusCode"] = 400
        response["body"] = json.dumps({"error": "Bad request: Missing headers"})
        return response

    query_parameters = event['queryStringParameters']
    header = event['headers']

    try:
        session_id = header.get("Session-Id", header.get("session-id"))
    except Exception:
        response["statusCode"] = 400
        response["body"] = json.dumps({"error": "Bad request: Session-ID header not found"})
        return response

    input_json = {
        "searchTerm": query_parameters.get("searchTerm"),
        "pageNumber": query_parameters.get("pageNumber"),
        "refreshResults": query_parameters.get("refreshResults"),
        "sessionID": session_id,
        "sortParams": query_parameters.get("sortParams"),
        "filterParams": query_parameters.get("filterParams")
    }

    try:
        response_body = search(input_json)
    except Exception as e:
        print(f"Exception in database query: {e}")
        response["statusCode"] = 500
        response["body"] = json.dumps({"error": "Internal Server Error"})
        return response

    response["body"] = json.dumps(response_body)
    return response
