import json
from endpoints.app import test_handler

def test_test_handler():
    event = {}
    context = {}
    
    response = test_handler(event, context)
    
    assert response["statusCode"] == 200
    
    body = json.loads(response["body"])
    
    assert isinstance(body, list)
    assert len(body) == 2
    
    assert body[0]["commentId"] == "12345"
    assert body[0]["docketId"] == "EPA-HQ-OAR-2023-0123"
    assert body[0]["commenterName"] == "John Doe"
    assert body[0]["commentText"] == "I fully support stricter air quality standards to improve public health."
    assert body[0]["submittedDate"] == "2024-01-15"
    
    assert body[1]["commentId"] == "67890"
    assert body[1]["docketId"] == "DOT-OST-2024-0001"
    assert body[1]["commenterName"] == "Jane Smith"
    assert body[1]["commentText"] == "Airline passenger rights are long overdue. Please prioritize this rule."
    assert body[1]["submittedDate"] == "2024-02-05"

def test_test_handler_empty_event():
    event = {}
    context = {}
    response = test_handler(event, context)
    assert response["statusCode"] == 200

def test_test_handler_invalid_event():
    event = {"invalid": "data"}
    context = {}
    response = test_handler(event, context)
    assert response["statusCode"] == 200

def test_test_handler_with_context():
    event = {}
    context = {"function_name": "test_function"}
    response = test_handler(event, context)
    assert response["statusCode"] == 200