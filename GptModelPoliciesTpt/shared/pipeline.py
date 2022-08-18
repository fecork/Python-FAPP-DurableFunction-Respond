import logging
import os
import sys
import concurrent.futures

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)
from data_processing import format_text
from data_request import ask_openai
from data_request import load_parameters
from data_respond import individual_paragraphs

def execute_concurrent(text_category_sixteen: str, text_category_nineteen: str, data_information: str, is_child: bool) -> dict:

    parameters = load_parameters()
    question_fare_rules = parameters["question_fare_rules"]
    structure_fare_rules = parameters["structure_fare_rules"]

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        gpt_paragraph = executor.submit(
            execute_extract_paragraph, text_category_sixteen)
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
        if is_child:
            response_child_discount = executor.submit(
                execute_child_discount, text_category_nineteen)
            dict_question_five = response_child_discount.result()
            response['question_5'] = dict_question_five

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
            'category': 16,
            'quote': "",
            'numberQuestion': 4,
            'boolean': False if 'non' in gpt_text_classification_text.lower() else True,
            'meanProbability': gpt_text_classification['meanProbability']
            }


def execute_child_discount(text_category_nineteen: str) -> dict:
    parameters = load_parameters()
    question_fare_rules_nineteen = parameters["question_fare_rules_nineteen"]
    structure_fare_rules_nineteen = parameters["structure_fare_rules_nineteen"]
    quiz_text_and_question_five = (
        text_category_nineteen + question_fare_rules_nineteen + "\n" * 2 + structure_fare_rules_nineteen)
    gpt_text_five = ask_openai(quiz_text_and_question_five, "question")
    list_quote = []
    list_answer = []
    gpt_text_five_text = gpt_text_five["text"].split("\n")
    flag = False
    for text in gpt_text_five_text:
        text = text.replace('\n', '\\n')
        text = text.translate({ord(i): None for i in '",:/\\'})

        if "quote" in text.lower():
            flag = True

        if flag == True:
            list_quote.append(text.replace("Quote", "").lstrip())
        if flag == False:
            list_answer.append(text.replace("Answer", "").lstrip())

    list_quote = list(filter(None, list_quote))
    list_answer = list(filter(None, list_answer))

    return {'question': "5. List all the charges shown in the text",
            'answer': list_answer,
            'category': 19,
            'quote': list_quote,
            'numberQuestion': 5,
            'boolean': False if len(list_answer) == 0 else True,
            'meanProbability': gpt_text_five['meanProbability']
            }


def execute_quiz(quiz_text_and_question: str) -> dict:
    gpt_quiz = ask_openai(quiz_text_and_question, "question")
    gpt_quiz_text = gpt_quiz["text"]

    gpt_quiz_mean_probability = gpt_quiz["meanProbability"]
    return individual_paragraphs(gpt_quiz_text, gpt_quiz_mean_probability)
