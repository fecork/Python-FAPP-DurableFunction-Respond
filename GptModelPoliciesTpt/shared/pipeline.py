import logging
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from data_processing import format_text
from data_request import ask_openai
from data_request import load_parameters
from data_respond import individual_paragraphs

def execute(data_rules: str, data_information: str):
    """Pipeline that clean the text and consult GPT

    Args:
        data_rules: rules' string
        data_information: information's text

    Returns:
        GPT response
    """
    parameters = load_parameters()
    question_paragraph = parameters["question_paragraph"]
    question_fare_rules = parameters["question_fare_rules"]
    structure_fare_rules = parameters["structure_fare_rules"]
    tag = parameters["tag_structure"]
    formated_text = format_text(data_rules)
    paragraph_text_and_question = formated_text + "\n" * 2 + question_paragraph
    gpt_paragraph = ask_openai(paragraph_text_and_question)
    quiz_text_and_question = (
        data_information + "\n" * 2 + gpt_paragraph + "\n" * 2 +
        question_fare_rules + "\n" * 2 + structure_fare_rules
    )

    gpt_quiz = ask_openai(quiz_text_and_question)
    gpt_quiz = tag + gpt_quiz
    response = individual_paragraphs(gpt_quiz)
    return response
