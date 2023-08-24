import os
import unittest
import subprocess
import time

from Excellenteam.final_project_excellenteam.python_client.web_api_client import WebAppClient

# Put here your default path to the .pptx file
DEFAULT_FILE_PATH = "C:\\Users\\User\\Desktop\\excellenteam\\excellenteam_python\\t.pptx"
BASE_URL = 'http://localhost:5000'

client = WebAppClient(BASE_URL)


class TestSystem(unittest.TestCase):
    """
    A test class to perform system tests for the web application and presentation chat helper.

    Note:
        This test class relies on the `web_api_client.WebAppClient` to interact with the web application API.

    """
    @classmethod
    def setUpClass(cls):
        # Start the Web API and Explainer in separate subprocesses
        cls.web_api_process = subprocess.Popen(["python", r"C:\Networks\Excellenteam\final_project_excellenteam\web_api\app.py"])
        cls.explainer_process = subprocess.Popen(["python", r"C:\Networks\Excellenteam\final_project_excellenteam\explainer\presentation_chat_helper.py"])

        # Wait a few seconds for the servers to start up
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        # Terminate the subprocesses for the Web API and Explainer
        cls.web_api_process.terminate()
        cls.explainer_process.terminate()

    def test_successful_end_to_end(self):
        # Upload the file
        uid = client.upload(DEFAULT_FILE_PATH)
        self.assertIsNotNone(uid, "UID should not be None")
        time.sleep(20)
        status = client.status(uid)
        self.assertIsNotNone(status.filename, "status.filename should not be None")
        self.assertIsNotNone(status.timestamp, "status.timestamp should not be None")
        self.assertIsNotNone(status.explanation, "status.explanation should not be None")

    def test_check_status_for_nonexistent_file(self):
        uid = 'nonexistent_uid'
        with self.assertRaises(Exception) as context:
            client.status(uid)
        self.assertIsInstance(context.exception, Exception)

    def test_upload_for_nonexistent_file(self):
        file_path = 'nonexistent_file_path'
        with self.assertRaises(Exception) as context:
            client.upload(file_path)
        self.assertIsInstance(context.exception, Exception)


if __name__ == '__main__':
    unittest.main()
