import requests
from datetime import datetime
from dataclasses import dataclass
from pptx import Presentation

@dataclass
class Status:
    status: str
    filename: str
    timestamp: datetime
    explanation: str

    def is_done(self):
        return self.status == 'done'


class WebAppClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path):
        url = f"{self.base_url}/upload"
        files = {'file': open(file_path, 'rb')}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            data = response.json()
            return data['uid']
        else:
            raise Exception(f"Error uploading file: {response.text}")

    def status(self, uid):
        url = f"{self.base_url}/status/{uid}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            status = data['status']
            filename = data['filename']
            timestamp = datetime.strptime(data['timestamp'], "%Y%m%d%H%M%S")
            explanation = data.get('explanation', '')

            return Status(status, filename, timestamp, explanation)
        else:
            raise Exception(f"Error getting status: {response.text}")


def main():
    base_url = 'http://localhost:5000'
    client = WebAppClient(base_url)

    # Upload file
    file_path = 'C:\\Users\\User\\Desktop\\excellenteam\\excellenteam_python\\t.pptx'  # Replace with the actual file path
    uid = client.upload(file_path)
    print(f"File uploaded. UID: {uid}")

    # Check status
    try:
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
        print(f"Error: {str(e)}")


if __name__ == '__main__':
    main()
