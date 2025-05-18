from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Monitor git push, by author, branch and timestamp
@app.route('/webhook', methods=['POST'])
def webhook(): 
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == 'push':
        author = data['pusher']['name']
        to_branch = data['ref'].split('/')
        timestamp = datetime.strptime(data['head_commit']['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
        data = {
            "type": "push",
            "author": author,
            "to_branch": to_branch,
            "timestamp": timestamp
        }
        else:
            return jsonify({'message': 'Push not received or supported'}), 400

        collection.insert_one(event_data)
        return jsonify({'message': 'Push received'}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find().sort("timestamp", -1).limit(10))
    for event in events:
        event['_id'] = str(event['_id'])
    return jsonify(events), 200

if __name__ = '__main__':
    app.run(host='0.0.0.0', port=8080)