import json

def handler(event, context):
    return {
        "statusCode": 200,
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
        ])
    }