# Flask Comments and Dockets API

## Overview
This repository contains a Flask application that serves as an API for accessing comment and docket information. The API allows users to retrieve comments and dockets, filter comments by dockets, and search for comments and dockets based on a query string.

## Files
- `app.py`: The Flask server that defines all the API endpoints.
- `comments.json`: A JSON file containing mock data for comments.
- `dockets.json`: A JSON file containing mock data for dockets.
- `health_check.json`: A JSON file used to report the health status of the application.

## Installation

To run this application, you'll need Python and Flask installed. You can set up the project environment with the following steps:

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Create Virtual Enviroment 
python -m venv venv
source venv/bin/activate  

# Install dependencies
pip install flask

# Fetching all comments:
curl http://127.0.0.1:5000/comments

# Filtering comments by docket ID:
curl "http://127.0.0.1:5000/comments?docketId=EPA-HQ-OAR-2023-0123"

# Searching comments and dockets:
curl "http://127.0.0.1:5000/search?query=air"

# Health check 
curl http://127.0.0.1:5000/health_check







