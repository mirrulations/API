import pytest
from endpoints.app import test_handler

def test_dummy():
    assert test_handler({}, {}) == {"statusCode": 200, "body": "Hello, world!"}


