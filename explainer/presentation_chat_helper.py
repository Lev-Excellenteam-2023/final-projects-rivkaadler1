import argparse
import asyncio
import os
import pptx_parser
from json_utils import save_list_as_json
from openai_api import OpenAIChatAPI
import time

DEFAULT_CHAT_ROLE = "You’re a kind helpful assistant that helps students understand the lecture's presentation"


async def chat_process(chat: OpenAIChatAPI, presentation_path: str, chat_role: str) -> list:
    """
    Process the chat for each slide in the presentation.

    Args:
        chat (OpenAIChatAPI): An instance of the OpenAIChatAPI class.
        presentation_path (str): Path to the presentation file.
        chat_role (str): Role of the chat.

    Returns:
        list: A list of generated responses for each slide.
    """
    chat.set_system_role(chat_role)
    parsed_content_dict = pptx_parser.parse_content_to_string_dict(presentation_path)
    presentation_subject = next(iter(parsed_content_dict.values()))
    responses = await asyncio.gather(
        *[
            asyncio.create_task(chat.generate_response(f"Could you give your best explanation to this presentation "
                                                       f"slide's content: {content}?(The presentation's subject is"
                                                       f" {presentation_subject})."))
            for content in parsed_content_dict.values()
        ]
    )
    return responses


def main(chat_role: str = DEFAULT_CHAT_ROLE) -> None:
    """
    Main function to continuously process files from the uploads directory and save the output JSON files.

    Args:
        chat_role (str, optional): Role of the chat. Defaults to DEFAULT_CHAT_ROLE.
    """
    chat = OpenAIChatAPI()

    while True:
        # Check for files in the uploads directory
        files = os.listdir('data/uploads')

        for filename in files:
            # Process only .pptx files
            if filename.endswith('.pptx'):
                presentation_path = os.path.join('data/uploads', filename)
                print(f"Processing file: {presentation_path}")

                chat_ans_lst = asyncio.run(chat_process(chat, presentation_path, chat_role))

                output_filename = os.path.splitext(filename)[0]
                output_file_path = f'data/outputs/{output_filename}.json'
                save_list_as_json(chat_ans_lst, output_file_path)
                print(f"Saved output JSON: {output_file_path}")

                # Remove the processed file
                os.remove(os.path.join('data/uploads', filename))

        print("Waiting for new files...")
        # Add a delay between iterations
        time.sleep(10)  # Delay for 10 seconds


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("chat_role", nargs="?", default=DEFAULT_CHAT_ROLE, help="Role of the chat (optional)")
    args = parser.parse_args()
    main(args.chat_role)

