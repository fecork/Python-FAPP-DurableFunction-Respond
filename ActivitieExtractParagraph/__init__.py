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

from Utilities.load_parameter import load_parameters
from Utilities.clear_respond import format_text
from AdaptadorOpenAI import adapter_gpt


def main(name: dict) -> dict:
    logging.warning("Executing ActivitiesExtractParagraph")
    data_rules = name["text_category_sixteen"]
    parameters = load_parameters()
    question_paragraph = parameters["question_paragraph"]
    formated_text = format_text(data_rules)
    paragraph_text_and_question = formated_text + "\n" * 2 + question_paragraph
    gpt_paragraph = adapter_gpt.ask_openai(
        paragraph_text_and_question, "question"
    )
    logging.warning("gpt_paragraph")
    return gpt_paragraph["text"]