import logging
import os
import sys
import concurrent.futures

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)
from data_respond import individual_paragraphs
from data_request import load_parameters
from data_request import ask_openai
from data_processing import format_text

def execute_concurrent(data_rules: str, data_information: str):

    parameters = load_parameters()
    question_fare_rules = parameters["question_fare_rules"]
    structure_fare_rules = parameters["structure_fare_rules"]

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        gpt_paragraph = executor.submit(execute_extract_paragraph, data_rules)
        gpt_paragraph_text = gpt_paragraph.result()['text']
        quiz_text_and_question = (
            data_information + "\n" * 2 + gpt_paragraph_text + "\n" * 2 +
            question_fare_rules + "\n" * 2 + structure_fare_rules
        )

        response_quiz = executor.submit(
            execute_quiz, quiz_text_and_question)
        response_classification = executor.submit(
            execute_classification_refund, gpt_paragraph_text)

        response = response_quiz.result()
        dict_question_4 = response_classification.result()

        response['question_4'] = dict_question_4
        list_response = []
        for key, value in response.items():
            list_response.append(value)
        result = list_response
        return result


def execute_extract_paragraph(data_rules: str) -> dict:
    parameters = load_parameters()
    question_paragraph = parameters["question_paragraph"]
    formated_text = format_text(data_rules)
    paragraph_text_and_question = formated_text + "\n" * 2 + question_paragraph
    gpt_paragraph = ask_openai(paragraph_text_and_question, "question")
    return gpt_paragraph


def execute_classification_refund(gpt_paragraph_text: str) -> dict:
    parameters = load_parameters()
    tag_class = parameters["structure_class_refund"]
    question_class_refund = parameters["question_class_refund"]
    gpt_paragraph_tag = question_class_refund + \
        "\n"*2 + gpt_paragraph_text + "\n"*2 + tag_class

    gpt_text_classification = ask_openai(gpt_paragraph_tag, "classification")
    gpt_text_classification_text = gpt_text_classification["text"]
    gpt_text_classification_text = gpt_text_classification_text.replace(
        'Class=', '').strip()
    return {'question': "4. Is refundable?",
            'answer': gpt_text_classification_text,
            'quote': "",
            'numberQuestion': 4,
            'boolean': False if 'non' in gpt_text_classification_text.lower() else True,
            'meanProbability': gpt_text_classification['meanProbability']
            }


def execute_quiz(quiz_text_and_question: str) -> dict:
    gpt_quiz = ask_openai(quiz_text_and_question, "question")
    gpt_quiz_text = gpt_quiz["text"]

    gpt_quiz_mean_probability = gpt_quiz["meanProbability"]
    return individual_paragraphs(gpt_quiz_text, gpt_quiz_mean_probability)
