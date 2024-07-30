import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

from call_charra_v2 import process_request  # Import your script

app = Flask(__name__)
CORS(app)
# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

def save_to_file(data):
    file_path = os.path.join('data', 'requests_data.txt')
    with open(file_path, 'a') as file:
        file.write(f"{data['name']}, {data['email']}, {data['phone']}, {data['company']}, {data['role']}, {data['use_case']}\n")

@app.route('/request_services', methods=['POST'])
def request_services():
    try:
        data = request.json
        print("Received data:", data)  # Log the received data

        # Save the data to a local file
        save_to_file(data)

        # Integrate your script's processing logic
        process_response = process_request(data)

        if process_response.status_code != 200:
            print("Failed to process request:", process_response.text)
            return jsonify({'message': 'Failed to process request', 'error': process_response.text}), 500
        
        return jsonify({'message': 'Request submitted successfully'})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
