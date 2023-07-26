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


def generate_status_response(status: str, original_filename: str, timestamp, explanation):
    """
    Generates a JSON response to represent the status and relevant information related to a file processing operation.

    Parameters:
        status (str): A string representing the status of the file processing operation.
        original_filename (str): The original filename of the processed file.
        timestamp: A timestamp representing the time when the response is generated.
        explanation (str): An optional string providing additional details or context about the status.

    Return Value:
        JSON Response: A JSON object containing the status information and relevant details in the response format.
    """
    return jsonify({'status': status, 'filename': original_filename, 'timestamp': timestamp,
                    'explanation': explanation}), 200


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handles file uploads via a POST request.

    Request:
        Method: POST
        Body: The request body should contain the file to be uploaded using the 'file' key.

    Response:
        Success (HTTP Status 200):
            Content: JSON object containing the generated UID for the uploaded file.
            Example: {"uid": "54f5ef71-5697-4f2f-9024-47875e42e9f1"}

        Error (HTTP Status 400):
            Content: JSON object containing the error message.
            Example: {"error": "No file uploaded."}
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded.'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Empty filename.'}), 400

        # Generate a unique identifier for the file
        uid = str(uuid.uuid4())

        # Get the original filename
        original_filename = secure_filename(file.filename.split('.')[0])

        # Generate the new filename with timestamp, UID, and extension
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"{uid}_{original_filename}_{timestamp}"

        # Save the binary file to the uploads directory
        file.save(os.path.join(UPLOADS_FOLDER, new_filename))

        return jsonify({'uid': uid}), 200

    except Exception as e:
        return f'Error in upload endpoint: {str(e)}', 400


@app.route('/status/<uid>', methods=['GET'])
def get_file_status(uid):
    """
    Retrieves the status and relevant information related to a specific file identified by its unique identifier (UID).

    URL Endpoint:
        /status/<uid>

    HTTP Method:
        GET

    Parameters:
        uid (str): The unique identifier (UID) of the file for which the status is to be retrieved.

    Response:
        Success (HTTP Status 200):
            Content: JSON object containing the status information, original filename, timestamp, and explanation (if applicable).
            Example: {"status": "pending", "filename": "example_file.txt", "timestamp": "2023-07-26 15:30:00", "explanation": null}

        File Not Found (HTTP Status 404):
            Content: JSON object indicating that the requested file was not found.
            Example: {"status": "not found"}
    """
    # Check if the file exists in the uploads folder
    uploaded_file = next((filename for filename in os.listdir(UPLOADS_FOLDER) if uid == filename.split('_')[0]), None)

    if uploaded_file:
        # Extract the original filename and timestamp from the file name
        _, original_filename, timestamp = uploaded_file.rsplit('_', 2)
        return generate_status_response('pending', original_filename, timestamp, None)

    # Check if the file exists in the outputs folder
    output_file = next((filename for filename in os.listdir(OUTPUTS_FOLDER) if uid == filename.split('_')[0]), None)
    if output_file:
        # Read the output JSON file and extract the explanation
        output_file_path = os.path.join(OUTPUTS_FOLDER, output_file)
        with open(output_file_path, 'r') as file:
            data = json.load(file)
            explanation = "".join(data[0])
        # Extract the filename and timestamp from the output file name
        _, original_filename, timestamp = output_file.rsplit('_', 2)
        return generate_status_response('done', original_filename, timestamp, explanation)

    # If the file doesn't exist in either folder, return appropriate response with 404 status
    return jsonify({'status': 'not found'}), 404


if __name__ == '__main__':
    if not os.path.exists(UPLOADS_FOLDER):
        os.makedirs(UPLOADS_FOLDER)
    if not os.path.exists(OUTPUTS_FOLDER):
        os.makedirs(OUTPUTS_FOLDER)
    app.run(debug=True)
