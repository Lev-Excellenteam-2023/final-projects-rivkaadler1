import os
import openai
from dotenv import load_dotenv

load_dotenv()


class OpenAIChatAPI:
    def __init__(self):
        self.system_role = ""
        openai.api_key = os.getenv("OPENAI_API_KEY")

    async def generate_response(self, prompt: str):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": self.system_role}, {"role": "user", "content": prompt}]
        )
        chat_response = completion.choices[0].message.content
        return chat_response

    def set_system_role(self, role: str):
        self.system_role = role
