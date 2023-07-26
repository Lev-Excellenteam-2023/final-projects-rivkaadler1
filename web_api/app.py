import json

from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

UPLOADS_FOLDER = os.environ.get("UPLOADS_FOLDER_PATH")
OUTPUTS_FOLDER = os.environ.get("OUTPUTS_FOLDER_PATH")


# Define the upload endpoint
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename.'}), 400

    # Generate a unique identifier for the file
    uid = str(uuid.uuid4())

    # Get the original filename
    original_filename = secure_filename(file.filename)

    # Generate the new filename with timestamp, UID, and extension
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{timestamp}_{uid}_{original_filename}"

    # Save the file to the uploads directory
    file.save(os.path.join('data/uploads', new_filename))

    return jsonify({'uid': uid}), 200


# Define the status endpoint
@app.route('/status/<uid>', methods=['GET'])
def get_file_status(uid):
    uploads_folder = 'data/uploads'
    outputs_folder = 'data/outputs'

    # Check if the file exists in the uploads folder
    uploaded_file = next((filename for filename in os.listdir(uploads_folder) if uid in filename), None)

    if uploaded_file:
        # Extract the original filename and timestamp from the file name
        timestamp, _, original_filename = uploaded_file.rsplit('_', 2)
        original_filename = os.path.splitext(original_filename)[0]

        return jsonify({'status': 'pending', 'filename': original_filename, 'timestamp': timestamp})

    # Check if the file exists in the outputs folder
    output_file = next((filename for filename in os.listdir(outputs_folder) if uid in filename), None)
    if output_file:
        # Read the output JSON file and extract the explanation
        output_file_path = os.path.join(outputs_folder, output_file)
        with open(output_file_path, 'r') as file:
            explanation = file.read()

        # Extract the filename and timestamp from the output file name
        timestamp, _, original_filename = output_file.rsplit('_', 2)
        original_filename = os.path.splitext(original_filename)[0]

        return jsonify({'status': 'done', 'filename': original_filename, 'timestamp': timestamp,
                        'explanation': explanation})

    # If the file doesn't exist in either folder, return appropriate response with 404 status
    return jsonify({'status': 'not found'}), 404


if __name__ == '__main__':
    if not os.path.exists(UPLOADS_FOLDER):
        os.makedirs(UPLOADS_FOLDER)
    if not os.path.exists(OUTPUTS_FOLDER):
        os.makedirs(OUTPUTS_FOLDER)
    app.run(debug=True)
