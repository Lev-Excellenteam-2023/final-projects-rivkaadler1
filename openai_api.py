import os
import openai
from dotenv import load_dotenv

load_dotenv()


class OpenAIChatAPI:
    def __init__(self):
        self.messages = []
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_response(self, prompt: str):
        self.messages.append({"role": "user", "content": prompt})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        chat_response = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": chat_response})
        return chat_response

    def set_system(self, content: str):
        self.messages.append({"role": "system", "content": content})