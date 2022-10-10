import re
import os
import sys
import logging
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Utilities.load_parameter import load_parameters
from Utilities import clear_respond

loaded_parameters = load_parameters()
number_questions = loaded_parameters["number_question_cancellation"]
list_questions = loaded_parameters["list_question_fare_rules_cancellation"].split(",")


def validate_boolean(text: str) -> bool:
    """
    convert the text to boolean
    Args:
        text: text to convert
    return:
        boolean
    """
    text = str(text).lower()
    if "true" in text:
        return True
    if "false" in text:
        return False
    return None


def validate_charge_number(dict_questions: dict, question_charge_list: list) -> dict:
    """
    build a dictionary with the information about the charge number
    Args:
        dict_questions: dictionary with the information of the questions
    return:
        dictionary with the formated information of the questions
    """

    list_denomination = loaded_parameters["denomination"].split("\n")
    for question_charge in question_charge_list:
        if question_charge in dict_questions:
            text = dict_questions[question_charge]["answer"]
            number = [float(s) for s in re.findall(r"-?\d+\.?\d*", text)]
            # select text with the denomination in denomination list
            denomination = [value for value in list_denomination if value in text]
            denomination = denomination[0] if len(denomination) > 0 else text

            if len(number) > 0:
                dict_questions[question_charge]["boolean"] = True
                dict_questions[question_charge]["value"] = number[0]
                dict_questions[question_charge][
                    "denomination"
                ] = clear_respond.format_denomination(denomination).strip()
            if len(number) == 0:
                dict_questions[question_charge]["boolean"] = False
                dict_questions[question_charge]["value"] = None
                dict_questions[question_charge]["denomination"] = None
    return dict_questions


def validate_structure_json(dict_questions: dict) -> dict:
    """
    build a dictionary with the information of the questions
    Args:
        dict_questions: dictionary with the information of the questions
    return:
        dictionary with the formated information of the questions
    """
    list_numbers = range(number_questions - 1)

    for number in list_numbers:
        number = number + 1
        if "question_" + str(number) not in dict_questions:
            dict_questions["question_" + str(number)] = {
                "answer": "",
                "category": "",
                "quote": "",
                "boolean": False,
                "numberQuestion": number,
                "question": list_questions[int(number) - 1],
                "score": 0,
                "value": None,
                "denomination": None,
            }

    return dict_questions


def validate_date(date: str) -> str:
    """
    This is a function for validate if the date is in the correct format.
    Args: string with the date to validate.
    Return: string with the date in the correct format.
    """
    try:
        date_format_base = "%Y-%m-%dT%H%M%S"
        date_format = "%d/%m/%Y, %H:%M:%S"

        return datetime.strptime(date, date_format_base).strftime(date_format)
    except ValueError:
        logging.error(ValueError)
        return date


def validate_number(text):
    """
    This is a function for validate if the text is a number.
    Args:
        txt (str): This is a string with the text to validate.
    Returns:
        bool: This is a boolean with the result of the validation.
    """
    for words in text.split():
        if words.isdigit():
            return True
        else:
            return False
