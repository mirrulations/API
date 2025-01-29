from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Update paths to include the 'mock' directory
with open('mock/comments.json') as f:
    comments = json.load(f)

with open('mock/dockets.json') as f:
    dockets = json.load(f)

@app.route('/comments', methods=['GET'])
def get_comments():
    docket_id = request.args.get('docketId')
    if docket_id:
        filtered_comments = [comment for comment in comments if comment['docketId'] == docket_id]
        return jsonify(filtered_comments)
    return jsonify(comments)

@app.route('/dockets', methods=['GET'])
def get_dockets():
    return jsonify(dockets)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    filtered_comments = [comment for comment in comments if query in comment['commentText'].lower()]
    filtered_dockets = [docket for docket in dockets if query in docket['description'].lower()]
    return jsonify({'comments': filtered_comments, 'dockets': filtered_dockets})

if __name__ == '__main__':
    app.run(debug=True)

