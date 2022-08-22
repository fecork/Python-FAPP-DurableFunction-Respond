import os
import sys
import concurrent.futures

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from dto_respond import Respond
from handler_respond import individual_paragraphs
from shared.load_parameter import load_parameters
from adapter_gpt import ask_openai
from clear_respond import format_text

parameters = load_parameters()


def execute_concurrent_cancellation(text_category_sixteen: str, text_category_nineteen: str, data_information: str, is_child: bool) -> dict:

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
        response_child_discount = executor.submit(
            execute_child_discount, text_category_nineteen, is_child)
        dict_question_five = response_child_discount.result()

        response = response_quiz.result()
        dict_question_4 = response_classification.result()

        response['question_4'] = dict_question_4

        if dict_question_five is not None:
            response['question_5'] = dict_question_five

        list_response = []
        for key, value in response.items():
            list_response.append(value)
        result = list_response
        return result


def execute_extract_paragraph(data_rules: str) -> dict:
    question_paragraph = parameters["question_paragraph"]
    formated_text = format_text(data_rules)
    paragraph_text_and_question = formated_text + "\n" * 2 + question_paragraph
    gpt_paragraph = ask_openai(paragraph_text_and_question, "question")
    return gpt_paragraph


def execute_classification_refund(gpt_paragraph_text: str) -> dict:
    tag_class = parameters["structure_class_refund"]
    question_class_refund = parameters["question_class_refund"]
    gpt_paragraph_tag = question_class_refund + \
        "\n"*2 + gpt_paragraph_text + "\n"*2 + tag_class

    gpt_text_classification = ask_openai(gpt_paragraph_tag, "classification")
    gpt_text_classification_text = gpt_text_classification["text"]
    gpt_text_classification_text = gpt_text_classification_text.replace(
        'Class=', '').strip()

    return Respond(
        question="4. Is refundable?",
        answer=gpt_text_classification_text,
        category=16,
        quote='',
        numberQuestion=4,
        boolean=True if gpt_text_classification_text == "Yes" else False,
        meanProbability=gpt_text_classification['meanProbability']).__dict__


def execute_child_discount(text_category_nineteen: str, is_child: bool) -> dict:
    if is_child:
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

            if flag is True:
                list_quote.append(text.replace("Quote", "").lstrip())
            if flag is False:
                list_answer.append(text.replace("Answer", "").lstrip())

        list_quote = list(filter(None, list_quote))
        list_answer = list(filter(None, list_answer))

        return Respond(
            question="5. List all the charges shown in the text",
            answer=list_answer,
            category=19,
            quote=list_quote,
            numberQuestion=5,
            boolean=False if len(list_answer) == 0 else True,
            meanProbability=gpt_text_five['meanProbability']).__dict__
    else:
        return None


def execute_quiz(quiz_text_and_question: str) -> dict:
    gpt_quiz = ask_openai(quiz_text_and_question, "question")
    gpt_quiz_text = gpt_quiz["text"]

    gpt_quiz_mean_probability = gpt_quiz["meanProbability"]
    return individual_paragraphs(gpt_quiz_text, gpt_quiz_mean_probability)
