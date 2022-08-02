import os
import sys
import openai

from typing import Dict

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from shared.load_parameter import load_parameters, load_credentials

def ask_openai(text: str) -> str:
    """
    This is a function for  ask question to GPT API by OpenAI.
    """

    loaded_parameters = load_parameters()
    parameters = loaded_parameters["open_ai_parameters"]
    openai = login_openai()
    prompt = parameters["prompt"]
    prompt = f"{prompt}:\n\n{text}"
    response = openai.Completion.create(
        engine=parameters["model"],
        prompt=prompt,
        temperature=parameters["temperature"],
        max_tokens=parameters["max_tokens"],
        top_p=parameters["top_p"],
        frequency_penalty=parameters["frequency_penalty"],
        presence_penalty=parameters["presence_penalty"],
    )

    return response.choices[0].text.lstrip()


def login_openai() -> Dict:
    """
    This is a function for  login to openai.
    """

    credentials = load_credentials()

    if "open_ai" in credentials:
        openai_credentials = credentials["open_ai"]["KEY"]
    else:
        print("No credentials for openai")

    openai.api_key = openai_credentials
    return openai
