import json
from endpoints.app import lambda_handler

def validate_response(response):
    assert response["statusCode"] == 200
    
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

def test_lambda():
    event = {}
    context = {}
    
    response = lambda_handler(event, context)
    validate_response(response)


def test_lambda_empty_event():
    event = {}
    context = {}
    response = lambda_handler(event, context)
    assert response["statusCode"] == 200

def test_lambda_invalid_event():
    event = {"invalid": "data"}
    context = {}
    response = lambda_handler(event, context)
    assert response["statusCode"] == 200

def test_lambda_with_context():
    event = {}
    context = {"function_name": "test_function"}
    response = lambda_handler(event, context)
    assert response["statusCode"] == 200