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


def validate_category_and_questions(task: str, number_questions: list, question_dict: dict) -> list:
    """
    This function is used to validate the category and the questions
    Args: task: task of the question
    Returns: list of questions
    """

    list_questions = []
    list_no_questions = []
    for number in number_questions:
        if task in question_dict["question_category_" + str(number)].keys():
            list_questions.append(number)
        else:
            list_no_questions.append(number)
    logging.warning("Questions with category: " + str(list_questions))
    logging.warning("Questions without category: " + str(list_no_questions))
    return list_questions
