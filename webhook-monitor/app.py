from flask import Flask, request, jsonify
from datetime import datetime
import os
import logging

app = Flask(__name__)

# Monitor git push, by author, branch and timestamp
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route('/')
def index():
    return "Webhook listener is running..", 200

@app.route('/webhook', methods=['POST'])
def webhook(): 
    try:
        payload = request.json
        event_type = request.headers.get('X-GitHub-Event')

        if event_type == 'push':
            author = payload['pusher']['name']
            to_branch = payload['ref'].split('/')[-1]
            timestamp = datetime.strptime(payload['head_commit']['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
            
            event_data = {
                "type": "push",
                "author": author,
                "to_branch": to_branch,
                "timestamp": timestamp
            }

            logging.info(f"Push received: {event_data}")
            return jsonify({'message': 'Push received', 'data': event_data}), 200
        
        return jsonify({'message': 'Unsupported event type'}), 400

    except Exception as e:
        logging.error(f'Error processing webhook: {(e)}')
        return jsonify({'message': 'Error processing webhook'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)