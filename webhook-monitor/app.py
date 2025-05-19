from flask import Flask, request, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from dateutil import parser as date_parser
import os
import logging

app = Flask(__name__)

# Prometheus counter
push_counter = Counter('github_push_total', 'Total Github push events', ['author', 'branch'])

# Python logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Webhook listener
@app.route('/')
def index():
    return "Webhook listener is running..", 200

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Monitor git push, by author, branch and timestamp

@app.route('/webhook', methods=['POST'])
def webhook(): 
    try:
        payload = request.get_json(force=True)
        logging.info(f"Received payload: {payload}")

        event_type = request.headers.get('X-GitHub-Event')
        logging.info(f"GitHub event type: {event_type}")

        if event_type == 'push':

            author = payload['pusher']['name']
            to_branch = payload['ref'].split('/')[-1]
            timestamp = date_parser.parse(payload['head_commit']['timestamp'])

            event_data = {
                "type": "push",
                "author": author,
                "to_branch": to_branch,
                "timestamp": timestamp
            }
            push_counter.labels(author=author, branch=to_branch).inc()

            logging.info(f"Push received: {event_data}")
            return jsonify({'message': 'Push received', 'data': event_data}), 200

        return jsonify({'message': 'Unsupported event type'}), 400

    except Exception as e:
        logging.error(f'Error processing webhook: {str(e)}', exc_info=True)
        return jsonify({'message': 'Error processing webhook'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)