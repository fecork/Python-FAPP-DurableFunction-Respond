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


from Utilities import dto_respond
from Utilities.load_parameter import load_parameters
from AdaptadorOpenAI import adapter_gpt


def main(name: str) -> dict:
    logging.warning("Executing ActivitiesExtractParagraph")

    gpt_paragraph_text = name
    parameters = load_parameters()

    tag_class = parameters["structure_class_refund"]
    question_class_refund = parameters["question_class_refund"]
    gpt_paragraph_tag = (
        question_class_refund
        + "\n" * 2
        + gpt_paragraph_text
        + "\n" * 2
        + tag_class
    )

    gpt_text_classification = adapter_gpt.ask_openai(
        gpt_paragraph_tag, "classification"
    )
    gpt_text_classification_text = gpt_text_classification["text"]
    gpt_text_classification_text = gpt_text_classification_text.replace(
        "Class=", ""
    ).strip()

    logging.warning("gpt_text_classification_text")

    return dto_respond.Respond(
        question="4. Is refundable?",
        answer=gpt_text_classification_text,
        category=16,
        quote="",
        numberQuestion=4,
        boolean=True if gpt_text_classification_text == "Yes" else False,
        meanProbability=gpt_text_classification["meanProbability"],
    ).__dict__