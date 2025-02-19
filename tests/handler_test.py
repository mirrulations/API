import json
from endpoints.app import lambda_handler

def test_lambda():
    event = {}
    context = {}
    
    response = lambda_handler(event, context)
    
    assert response["statusCode"] == 200
    
    body = json.loads(response["body"])
    
    assert isinstance(body, list)
    assert len(body) > 0  # Ensuring at least one comment exists

    required_keys = {"commentId", "docketId", "commenterName", "commentText", "submittedDate"}

    for comment in body:
        assert isinstance(comment, dict)
        assert required_keys.issubset(comment.keys())  # Ensure all required keys are present
        assert isinstance(comment["commentId"], str)
        assert isinstance(comment["docketId"], str)
        assert isinstance(comment["commenterName"], str)
        assert isinstance(comment["commentText"], str)
        assert isinstance(comment["submittedDate"], str)


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