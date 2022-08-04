import logging
import os
import sys
import openai

import numpy as np
from typing import Dict

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)
from shared.load_parameter import load_parameters, load_credentials


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


def ask_openai(text: str, task: str) -> dict:
    """
    This is a function for  
    ask question to GPT API by OpenAI.
    """

    loaded_parameters = load_parameters()
    if task == "question":
        parameters = loaded_parameters["open_ai_parameters"]

    if task == "classification":
        parameters = loaded_parameters["open_ai_parameters_classification"]
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
        logprobs=1,
    )

    with open('response.txt', 'w') as f:
        f.write(str(response.choices[0].logprobs.top_logprobs))

    response_mean_probability = mean_probability(response)

    return {
            "text": response.choices[0].text.lstrip(), 
            "mean_probability": response_mean_probability
            }


def mean_probability(response: object) -> float:
    """
    This is a function for 
    calculate mean probability.
    """
    list_probs = []
    list_top_logprobs = list(response.choices[0].logprobs.top_logprobs)
    for top_logprobs_object in list_top_logprobs:
        for key, logprob in top_logprobs_object.items():
            list_probs.append(np.e**float(logprob))

    mean_probability = sum(list_probs) / len(list_probs)*100

    return mean_probability
