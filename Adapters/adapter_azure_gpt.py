import os
import requests
import json
import openai
import logging

from Utilities.load_parameter import load_parameters


def login_openai() -> Dict:
    """
    This is a function for  login to openai.
    """
    logging.warning("Executing login_openai")
    try:

        openai.api_key = "REPLACE_WITH_YOUR_API_KEY_HERE"
        openai.api_base = "REPLACE_WITH_YOUR_ENDPOINT_HERE"  # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
        openai.api_type = "azure"
        openai.api_version = "2022-06-01-preview"  # this may change in the future

    except Exception as e:
        print("No credentials for openai")
        print(e)


def ask_openai(text: str, task: str) -> dict:
    """
    This is a function for
    ask question to AZURE GPT by OpenAI.
    """
    logging.warning("Executing ask_openai")
    login_openai()
    loaded_parameters = load_parameters()
    if task == "cancellation":
        parameters = loaded_parameters["open_ai_parameters"]

    if task == "change":
        parameters = loaded_parameters["open_ai_parameters_change"]
    if "manual" in task:
        parameters = loaded_parameters["open_ai_parameters_change_manual"]

    if task == "classification":
        parameters = loaded_parameters["open_ai_parameters_classification"]

    if task == "list":
        parameters = loaded_parameters["open_ai_parameters_list"]

    # NOTE:
    # deployment_id = "REPLACE_WITH_YOUR_DEPLOYMENT_NAME"  # This will correspond to the custom name you chose for your deployment when you deployed a model.

    # Send a completion call to generate an answer
    # print("Sending a test completion job")
    # start_phrase = "Write a tagline for an ice cream shop. "

    prompt = parameters["prompt"]
    prompt = f"{prompt}:\n\n{text}"
    response = openai.Completion.create(
        # engine=deployment_id
        engine=parameters["model"],
        prompt=prompt,
        temperature=parameters["temperature"],
        max_tokens=parameters["max_tokens"],
        top_p=parameters["top_p"],
        frequency_penalty=parameters["frequency_penalty"],
        presence_penalty=parameters["presence_penalty"],
        logprobs=1,
    )
    # text = response["choices"][0]["text"].replace("\n", "").replace(" .", ".").strip()
    # print(start_phrase + text)

    response_mean_probability = mean_probability(response)

    return {
        "text": response.choices[0].text.lstrip(),
        "meanProbability": response_mean_probability,
    }


def mean_probability(response: object) -> float:
    """
    This is a function for
    calculate mean probability.
    """
    logging.warning("Executing mean_probability")
    list_probs = []
    list_top_logprobs = list(response.choices[0].logprobs.top_logprobs)
    for top_logprobs_object in list_top_logprobs:
        for key, logprob in top_logprobs_object.items():
            list_probs.append(np.e ** float(logprob))

    mean_probability = sum(list_probs) / len(list_probs) * 100

    return mean_probability
