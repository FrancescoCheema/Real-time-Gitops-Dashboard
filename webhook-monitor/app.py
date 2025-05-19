from flask import Flask, request, jsonify
from datetime import datetime
from dateutil import parser as date_parser
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route('/')
def index():
    return "Webhook listener is running..", 200

# Monitor git push, by author, branch and timestamp

@app.route('/webhook', methods=['POST'])
def webhook(): 
    try:
        payload = request.get_json(force=True)
        logging.info(f"Received payload: {payload}")
        
        event_type = request.headers.get('X-GitHub-Event')
        logging.info(f"GitHub event type: {event_type}")

        if event_type == 'push':
            # Validate required keys
            if not all(k in payload for k in ['pusher', 'ref', 'head_commit']):
                return jsonify({'message': 'Missing fields in payload'}), 400

            author = payload['pusher']['name']
            to_branch = payload['ref'].split('/')[-1]
            timestamp = date_parser.parse(payload['head_commit']['timestamp'])

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
        logging.error(f'Error processing webhook: {str(e)}', exc_info=True)
        return jsonify({'message': 'Error processing webhook'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)