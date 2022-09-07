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
from AdaptadorOpenAI import adapter_gpt


def main(name: str) -> dict:
    logging.warning("Executing ActivitiesExtractParagraph")
    quiz_text_and_question = name
    gpt_quiz = adapter_gpt.ask_openai(quiz_text_and_question, "question")
    gpt_quiz_text = gpt_quiz["text"]

    gpt_quiz_mean_probability = gpt_quiz["meanProbability"]
    logging.warning("gpt_quiz")
    return individual_paragraphs(gpt_quiz_text, gpt_quiz_mean_probability)
