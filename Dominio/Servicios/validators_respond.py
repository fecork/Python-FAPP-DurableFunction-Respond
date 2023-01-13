import os
import sys
import logging
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Dominio.Servicios.load_parameter import load_parameters

loaded_parameters = load_parameters()


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


def validate_structure_json(dict_questions: dict, task: str, number_questions: int, list_questions: list) -> dict:
    """
    build and sort a dictionary with the information of each question
    Args:
        dict_questions: dictionary with the information of the questions
    return:
        dictionary with the formated information of the questions
    """

    if "cancel" in task.lower():
        list_questions = loaded_parameters[
            "list_question_fare_rules_cancellation"
        ].split(",")
        number_questions = loaded_parameters["number_question_cancellation"]

    if "change" in task.lower():
        list_questions = loaded_parameters[
            "list_question_fare_rules_change"].split(
            ",")
        number_questions = loaded_parameters["number_question_change"]
    if "manual_group_one" in task.lower():
        list_questions = loaded_parameters[
            "list_question_fare_rules_change_manual_group_one"
        ].split(",")
        number_questions = loaded_parameters[
            "number_question_change_manual_group_one"]
    if "manual_group_two" in task.lower():
        list_questions = loaded_parameters[
            "list_question_fare_rules_change_manual_group_two"
        ].split(",")
        number_questions = loaded_parameters[
            "number_question_change_manual_group_two"]
    if "manual_group_three" in task.lower():
        list_questions = loaded_parameters[
            "list_question_fare_rules_change_manual_group_three"
        ].split(",")
        number_questions = loaded_parameters[
            "number_question_change_manual_group_three"
        ]
        
    if "flex" in task.lower():
        #TODO
        # list_questions = loaded_parameters[
        #     "list_question_fare_rules_change_manual_group_three"
        # ].split(",")
        # list_questions = loaded_parameters[
        #     "list_question_fare_rules_change_flex"
        # ].split(",")
        list_questions = list_questions
        number_questions = number_questions

    # list_numbers = range(number_questions)
    # for number in list_numbers:
    #     number = number + 1
    #     if "question_" + str(number) not in dict_questions:
    #         dict_questions["question_" + str(number)] = {
    #             "number_question": number,
    #             "answer": [],
    #             "category": "",
    #             "quote": "",
    #             "boolean": False,
    #             "question": list_questions[int(number) - 1],
    #             "score": 0,
    #             "value": [],
    #             "denomination": None,
    #         }

    return dict_questions


def validate_date(date: dict) -> str:
    """
    This is a function for validate if the date is in the correct format.
    Args: string with the date to validate.
    Return: string with the date in the correct format.
    """
    date_format_base = "%Y-%m-%dT%H:%M:%S"
    date_format = "%d/%m/%Y, %H:%M:%S"
    response = None
    try:
        date_quote = date.upper()
        date_quote = clean_text(date_quote)
        response = datetime.strptime(
            date_quote, date_format_base).strftime(date_format)
        return response
    except Exception as e:
        logging.warning("Error: " + str(e))
        return None


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


def clean_text(date_quote: str) -> str:
    """
    This is a function for clean the text.
    Args: string with the text to clean.
    Return: string with the text cleaned.
    """
    date_quote = date_quote.replace("DEPARTUREDATE", "")
    date_quote = date_quote.replace("DEPARTURE DATE", "")
    date_quote = date_quote.replace("DEPARTURE", "")
    date_quote = date_quote.replace("DATE", "")
    date_quote = date_quote.replace("THE", "")
    date_quote = date_quote.replace("IS", "")
    date_quote = date_quote.replace("=", "")
    date_quote = date_quote.strip()
    return date_quote
