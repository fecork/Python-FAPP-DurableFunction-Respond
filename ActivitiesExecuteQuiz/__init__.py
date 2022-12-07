# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)


from Utilities.handler_respond import individual_paragraphs
from Adapters import adapter_azure_gpt as adapter


from Utilities.load_parameter import load_parameters

loaded_parameters = load_parameters()


def main(parameters: dict) -> dict:
    """
    This is a function for send a GPT a text and get a respond.
    Args:
        parametersCancellation (dict): This is a dictionary with text and task.
    Returns:
        dict: This is a dictionary with text and mean probability.
    """
    
    logging.warning("Executing ActivitiesExtractParagraph")
    quiz_text_and_question = parameters["quiz_text_and_question"]
    list_question_charge = parameters["list_question_charge"]
    task = parameters["task"]
    gpt_quiz = adapter.ask_openai(quiz_text_and_question, task)
    gpt_quiz_text = gpt_quiz["text"]

    gpt_quiz_mean_probability = gpt_quiz["meanProbability"]

    respond = individual_paragraphs(
        gpt_quiz_text, gpt_quiz_mean_probability, parameters, list_question_charge, task
    )

    logging.warning("<<<<<<<<<<<<<<<<<<")
    logging.warning("Respuesta de GPT")
    logging.info(respond)
    logging.warning(">>>>>>>>>>>>>>>>>>")
    return respond
