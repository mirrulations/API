# AWS SAM Application Setup

## Template Overview

The AWS SAM template (`template.yaml`) defines the resources that AWS CloudFormation will create and manage. Here’s how each component is set up:

### `AWS::Serverless::Api`
This resource defines the API Gateway, specifying its stage name  and other configurations like the domain name, SSL certificate, and endpoint configuration. It's crucial for setting up a custom domain and configuring API Gateway to work under EDGE optimized deployments.

### `AWS::Serverless::Function`
This resource sets up the Lambda function that handles your API requests. The function is linked to the API Gateway through the `Events` property, which maps HTTP methods and paths to this function.

# Lambda Function Documentation

## Overview

The `test_handler` function is a sample AWS Lambda function written in Python. It is designed to integrate with AWS API Gateway using the Lambda Proxy Integration. This setup allows the function to handle HTTP requests directly, responding based on the request details provided by API Gateway.

## Function Description

### `test_handler(event, context)` in app.py

This function serves as an endpoint for HTTP requests processed through AWS API Gateway. It returns a JSON array of comments, simulating a response from a backend

### Parameters

- **event (dict, required)**: Contains data from the API Gateway request. This includes HTTP method, headers, path, query parameters, and body content.
- **Documentation**: [API Gateway Lambda Proxy Input Format](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format)

 - **Documentation**: [Lambda Context Object](https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html)

### Returns

- **dict**: Conforms to the API Gateway Lambda Proxy Output Format. Includes the HTTP status code and a JSON string as the body.
- **Documentation**: [API Gateway Lambda Proxy Output Format](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html)

