import re
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from shared.load_parameter import load_parameters


loaded_parameters = load_parameters()
number_questions = loaded_parameters["number_question"]
list_questions = loaded_parameters["list_question_fare_rules"].split(",")


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


def validate_charge_number(dict_questions: dict) -> dict:
    """
    build a dictionary with the information about the charge number
    Args:
        dict_questions: dictionary with the information of the questions
    return:
        dictionary with the formated information of the questions
    """
    question_charge = "question_2"
    if question_charge in dict_questions:
        text = dict_questions[question_charge]["answer"]
        number = [float(s) for s in re.findall(r'-?\d+\.?\d*', text)]
        denomination = ''.join([i for i in text if not i.isdigit()])
        if len(number) > 1:
            dict_questions[question_charge]["value"] = number[0]
        if len(number) < 1:
            dict_questions[question_charge]["value"] = None
        dict_questions[question_charge]["denomination"] = denomination
    return dict_questions


def validate_structure_json(dict_questions: dict) -> dict:
    """
    build a dictionary with the information of the questions
    Args:
        dict_questions: dictionary with the information of the questions
    return:
        dictionary with the formated information of the questions
    """
    list_numbers = range(number_questions-1)

    for number in list_numbers:
        number = number + 1
        if "question_" + str(number) not in dict_questions:
            dict_questions["question_" + str(number)] = {"answer": "",
                                                         "category": "",
                                                         "quote": "",
                                                         "boolean": "",
                                                         "numberQuestion": number,
                                                         "question": list_questions[int(number)-1],
                                                         "score": 0,
                                                         }
    return dict_questions
