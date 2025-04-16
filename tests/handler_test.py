import json
from endpoints.app import lambda_handler
from unittest.mock import patch

def validate_200_response(response):
    body = json.loads(response["body"])
    assert isinstance(body, list)

    required_keys = {"docketId", "numComments", "docketTitle", "matchQuality"}

    for item in body:
        assert isinstance(item, dict)
        assert required_keys.issubset(item.keys())
        assert isinstance(item["docketId"], str)
        assert isinstance(item["numComments"], str)
        assert isinstance(item["docketTitle"], str)
        assert isinstance(item["matchQuality"], str)

def raise_exception():
    raise Exception("A database exception for testing")

@patch('endpoints.app.search')
def test_lambda_happy_path(mock_database):
    mock_database.return_value = json.dumps([
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

    event = { 'queryStringParameters': {'name': 'default'} }
    context = {}

    response = lambda_handler(event, context)
    validate_200_response(response)


def test_lambda_empty_event():
    event = {}
    context = {}
    response = lambda_handler(event, context)

    assert response["statusCode"] == 400
    assert response['body'] == "Missing query parameter 'name'"

def test_no_query_params():
    event = { 'queryStringParameters': {} }
    context = {}
    response = lambda_handler(event, context)

    assert response["statusCode"] == 400
    assert response['body'] == "Missing query parameter 'name'"

def test_wrong_query_params():
    event = { 'queryStringParameters': {'wrong_param': 'hello'} }
    context = {}
    response = lambda_handler(event, context)

    assert response["statusCode"] == 400
    assert response['body'] == "Missing query parameter 'name'"

@patch('endpoints.app.search')
def test_error_in_db_code(mock_database):
    mock_database.side_effect = raise_exception

    event = { 'queryStringParameters': {'name': 'default'} }
    context = {}
    response = lambda_handler(event, context)

    assert response["statusCode"] == 500
    assert response['body'] == "Internal Server Error"

@patch('endpoints.app.search')
def test_no_results_from_db(mock_database):
    mock_database.return_value = []

    event = { 'queryStringParameters': {'name': 'default'} }
    context = {}
    response = lambda_handler(event, context)

    assert response["statusCode"] == 404
    assert response['body'] == "No results for keyword"
