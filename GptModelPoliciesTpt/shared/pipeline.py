
import logging
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)
from data_respond import individual_paragraphs
from data_request import load_parameters
from data_request import ask_openai
from data_processing import format_text

def execute(data_rules: str, data_information: str) -> list:
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
    gpt_paragraph = ask_openai(paragraph_text_and_question, "question")
    gpt_paragraph_text = gpt_paragraph['text']
    quiz_text_and_question = (
        data_information + "\n" * 2 + gpt_paragraph_text + "\n" * 2 +
        question_fare_rules + "\n" * 2 + structure_fare_rules
    )

    gpt_quiz = ask_openai(quiz_text_and_question, "question")
    logging.warning('-----------------------------------------------------')
    logging.warning('GPT response:')
    logging.warning(gpt_quiz)
    logging.warning('-----------------------------------------------------')

    # gpt_quiz_text = tag + gpt_quiz["text"]
    gpt_quiz_text = gpt_quiz["text"]

    gpt_quiz_mean_probability = gpt_quiz["mean_probability"]
    response = individual_paragraphs(gpt_quiz_text, gpt_quiz_mean_probability)

    tag_class = parameters["structure_class_refund"]
    question_class_refund = parameters["question_class_refund"]
    gpt_paragraph_tag = question_class_refund + \
        "\n"*2 + gpt_paragraph_text + "\n"*2 + tag_class
    gpt_text_classification = ask_openai(gpt_paragraph_tag, "classification")
    gpt_text_classification_text = gpt_text_classification["text"]
    gpt_text_classification_text = gpt_text_classification_text.replace(
        'Class=', '').strip()
    dict_question_4 = {'question': "4. Is refundable?",
                       'answer': gpt_text_classification_text,
                       'quote': "",
                       'number_question': 4,
                       'boolean': False if 'non' in gpt_text_classification_text.lower() else True,
                       'mean_probability': gpt_text_classification['mean_probability']
                       }

    response['question_4'] = dict_question_4
    list_response = []
    for key, value in response.items():
        list_response.append({"question": value})
    return list_response
