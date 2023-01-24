from Dominio.Servicios import build_response
from Dominio.Servicios import clear_respond
from Dominio.Servicios.clear_respond import clear_value_json, extract_number
from Dominio.Servicios.load_parameter import load_parameters
from validators_respond import validate_boolean
import os
import sys
import re
import logging

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

loaded_parameters = load_parameters()


def execute_clean_json(score, text: str, dict_parameter: dict) -> dict:
    """
    block to execute the clean json
    Args:
        score: score of the text
        text: text to clean
    return:
        dictionary with the information of the paragraphs
    """
    list_questions = dict_parameter["list_questions"]
    number_question = dict_parameter["number_questions"]
    dict_response = {
        "numberQuestion": 0,
        "question": "",
        "answer": "",
        "category": 0,
        "quote": "",
        "freeText": True,
        "boolean": False,
        "mean_probability": score,
        "value": 0,
        "denomination": None,
    }

    key_number = ""

    for line in text:

        answer_i = clear_value_json(line, "answer")
        if answer_i is not None:
            dict_response["answer"] = answer_i

        number_question_input = clear_value_json(line, "number_question")

        if number_question_input is not None:

            number_question_input = extract_number(number_question_input)[0]

            if int(number_question_input) < int(number_question) + 1:
                key_number = int(number_question_input)

                dict_response["question"] = list_questions[key_number - 1]
                dict_response["numberQuestion"] = key_number

        quote_i = clear_value_json(line, "quote")
        if quote_i is not None:
            dict_response["quote"] = quote_i

        boolean_i = clear_value_json(line, "boolean")
        if boolean_i is not None:
            boolean_i = validate_boolean(boolean_i)
            dict_response["boolean"] = boolean_i
        data = validate_charge_number(dict_response["answer"])
        other_response = build_response.edit_response(
            question_input=dict_response["question"],
            answer_input=dict_response["answer"],
            quote_input=dict_response["quote"],
            free_text_input=True,
            number_question_input=dict_response["numberQuestion"],
            boolean_input=data["boolean"],
            value_input=data["value"],
            denomination_input=data["denomination"],
            mean_probability_input=dict_response["mean_probability"],
        )
    return {"dict_response": other_response, "key_number": key_number}


def validate_charge_number(text: str) -> dict:
    """
    build a dictionary with the information about
    the charge number, denomination and value
    Args:
        dict_questions: dictionary with the information of the questions
    return:
        dictionary with the formated information of the questions
    """

    list_denomination = loaded_parameters["denomination"].split("\n")

    dict_questions = {"boolean": False, "value": [], "denomination": None}
    number = [float(s) for s in re.findall(r"-?\d+\.?\d*", text)]
    denomination = [
        value for value in list_denomination if str(value) in text.upper()]
    denomination = denomination[0] if len(denomination) > 0 else text

    if len(number) > 0:
        dict_questions["boolean"] = True
        dict_questions["value"] = number[0]
        dict_questions["denomination"] = clear_respond.format_denomination(
            denomination
        ).strip()
    if len(number) == 0:
        dict_questions["boolean"] = False
        dict_questions["value"] = None
        dict_questions["denomination"] = None
    return dict_questions


def set_category(question_list: dict, category: list):
    category_count = 0
    for key, value in question_list.items():
        value["category"] = category[category_count]
        category_count = category_count + 1


def replace_information_children(question_fare_rules_nineteen: str, passenger_child: dict) -> list:
    """
    This is a function for replace data to put in text
    Args:
        str (str): This is a string with the text to convert.
        data (dict): This is a dictionary with the data to replace.
    Returns:
        str: This is a string with the text converted.

    """
    list_questions = []
    for data in passenger_child:
        age = str(data["age"])
        seat = data["seat"]
        accompanied = data["isAccompanied"]

        if seat is True:
            seat = "with a seat"
        else:
            seat = "without a seat"

        if accompanied is True:
            accompanied = "and accompanied"
        else:
            accompanied = ""
        logging.info(age)
        logging.info(seat)
        logging.info(accompanied)
        text_question = question_fare_rules_nineteen.replace("#{AGE}#", age)
        text_question = text_question.replace("#{SEAT}#", seat)
        text_question = text_question.replace("#{ACCOMPANIED}#", accompanied)
        list_questions.append(text_question)
    return list_questions
