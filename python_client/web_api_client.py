import requests
from datetime import datetime
from dataclasses import dataclass
import time


@dataclass
class Status:
    """
    Represents the status of a file processing task.

    Attributes:
        status (str): The current status of the processing file.
        filename (str): The name of the file being processed.
        timestamp (datetime): The timestamp when the processing started.
        explanation (str): The presentation's explanation from chat gpt.
    """
    status: str
    filename: str
    timestamp: datetime
    explanation: str

    def is_done(self):
        """Check if the file processing is completed."""
        return self.status == 'done'


class WebAppClient:
    """
    A client for interacting with a web application to upload files and check their processing status.

    Attributes:
        base_url (str): The base URL of the web application's API.
    """
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path):
        """
        Uploads a file to the web application.

        Args:
            file_path (str): The local file path to be uploaded.

        Returns:
            str: The unique identifier (UID) associated with the uploaded file.

        Raises:
            Exception: If an error occurs during the file upload.
        """
        url = f"{self.base_url}/upload"
        files = {'file': open(file_path, 'rb')}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            data = response.json()
            return data['uid']
        else:
            raise Exception(f"Error uploading file: {response.text}")

    def status(self, uid):
        """
        Gets the processing status of a file.

        Args:
            uid (str): The unique identifier (UID) of the file whose status is to be checked.

        Returns:
            Status: An instance of the Status class representing the file's processing status.

        Raises:
            Exception: If an error occurs while getting the status.
        """
        url = f"{self.base_url}/status/{uid}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            status = data['status']
            filename = data['filename']
            timestamp = datetime.strptime(data['timestamp'][:-5], "%Y%m%d%H%M%S")
            explanation = data.get('explanation', '')
            return Status(status, filename, timestamp, explanation)
        else:
            raise Exception(f"Error getting status: {response.text}")


def main():
    """
     Main function to interact with the web application and check the processing status of a file.
     """
    base_url = 'http://localhost:5000'
    client = WebAppClient(base_url)
    # Get user inputs for file path and time to sleep
    file_path = input("Enter the file path: ")
    sleep_time = float(input("Enter the time to sleep till checking for status (in seconds): "))
    uid = client.upload(file_path)
    print(f"File uploaded. UID: {uid}")

    # Check status
    try:
        time.sleep(sleep_time)  # You can change the time sleep to get another answer
        status = client.status(uid)
        if status.is_done():
            print("File processing is done.")
            print(f"Filename: {status.filename}")
            print(f"Timestamp: {status.timestamp}")
            print(f"Explanation: {status.explanation}")
        else:
            print("File is still processing.")
            print(f"Filename: {status.filename}")
            print(f"Timestamp: {status.timestamp}")
    except Exception as e:
        print(f"Error in web_api_client.py: {str(e)}")


if __name__ == '__main__':
    main()
