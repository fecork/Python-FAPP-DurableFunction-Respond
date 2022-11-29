import os
import logging
import sys
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)
from validators_respond import validate_boolean
from Utilities.load_parameter import load_parameters
from Utilities.clear_respond import clear_value_json, extract_number
from Utilities import clear_respond
from Utilities import build_response
from Utilities.load_parameter import load_parameters

loaded_parameters = load_parameters()


def execute_clean_json(score, text: str, dict_question: dict) -> dict:
    """
    block to execute the clean json
    Args:
        score: score of the text
        text: text to clean
    return:
        dictionary with the information of the paragraphs
    """
    list_questions = dict_question["list_questions"].split(",")
    number_question = dict_question["number_questions"]
    dict_response = {
        "question": "",
        "answer": "",
        "category": 16,
        "quote": "",
        "freeText": True,
        "boolean": False,
        "numberQuestion": 0,
        "meanProbability": score,
        "value": 0,
        "denomination": None,
    }

    key_number = ""

    for line in text:

        answer_i = clear_value_json(line, "answer")
        if answer_i is not None:
            dict_response["answer"] = answer_i

        numberQuestion_i = clear_value_json(line, "number_question")

        if numberQuestion_i is not None:

            numberQuestion_i = extract_number(numberQuestion_i)[0]

            if int(numberQuestion_i) < int(number_question) + 1:
                key_number = int(numberQuestion_i)

                dict_response["question"] = list_questions[key_number - 1]
                dict_response["numberQuestion"] = key_number

                if key_number == 3:
                    dict_response["freeText"] = False

        quote_i = clear_value_json(line, "quote")
        if quote_i is not None:
            dict_response["quote"] = quote_i

        boolean_i = clear_value_json(line, "boolean")
        if boolean_i is not None:
            boolean_i = validate_boolean(boolean_i)
            dict_response["boolean"] = boolean_i
        data = validate_charge_number(dict_response["answer"])
        other_response = build_response.edit_response(
            question_i=dict_response["question"],
            answer_i=dict_response["answer"],
            category_i=16,
            quote_i=dict_response["quote"],
            freeText_i=True,
            numberQuestion_i=dict_response["numberQuestion"],
            boolean_i=data["boolean"],
            value_i=data["value"],
            denomination_i=data["denomination"],
            meanProbability_i=dict_response["meanProbability"],
        )
    return {"dict_response": other_response, "key_number": key_number}


def validate_charge_number(text: str) -> dict:
    """
    build a dictionary with the information about the charge number, denomination and value
    Args:
        dict_questions: dictionary with the information of the questions
    return:
        dictionary with the formated information of the questions
    """

    list_denomination = loaded_parameters["denomination"].split("\n")

    dict_questions = {"boolean": False, "value": [], "denomination": None}
    number = [float(s) for s in re.findall(r"-?\d+\.?\d*", text)]
    denomination = [value for value in list_denomination if str(value) in text]
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
