# Get Emails From cloudmailin.net
# Run this script to start the server
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/email', methods=['POST'])
def receive_email():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    # Extract subject and body from the JSON payload
    # Json Structure reference: https://docs.cloudmailin.com/http_post_formats/json_normalized/
    subject = data.get('headers', {}).get('subject', 'No Subject')
    body = data.get('plain', 'No Body')

    # Print the subject and body
    print(f'Subject: {subject}')
    print(f'Body: {body}')

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    api_key = os.getenv('API_KEY')
    print(f'API Key: {api_key}')
    # app.run(host='0.0.0.0', port=5000)