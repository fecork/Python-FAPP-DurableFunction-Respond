import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)
from validators_respond import (
    validate_boolean
)
from shared.load_parameter import load_parameters

loaded_parameters = load_parameters()
list_questions = loaded_parameters["list_question_fare_rules"].split(",")
number_question = loaded_parameters["number_question"]

def clear_value_json(line: str, key: str) -> str:
    """
    clear the text from the value
    Args:
        line: line to clear the value
        key: key to clear the value
    return:
        value of the key
    """
    key_json = key.translate({ord(i): None for i in ":"})

    if "quote" in line:
        line = line.replace("\n", " ")

    if key_json in line:
        res = line.replace(key, "")
        res = res.translate({ord(i): None for i in '",:'})
        res = res.strip()
        return res


def extract_number(sentence: str) -> list:
    """
    function to extract the number from the sentence
    Args:
        sentence: sentence to extract the number
    return:
        list with the numbers
    """

    list_number = []
    for text in sentence.split():
        try:
            list_number.append(float(text))
        except ValueError:
            pass
    return list_number


def execute_clean_json(score, text) -> dict:
    """
    block to execute the clean json
    Args:
        score: score of the text
        text: text to clean
    return:
        dictionary with the information of the paragraphs
    """
    dict_response = {"answer": "",
                     "quote": "",
                     "boolean": "",
                     "number_question": "",
                     "mean_probability": score
                     }
    key_number = ''

    for line in text:

        value = clear_value_json(line, "answer")
        if value is not None:
            dict_response["answer"] = value

        value = clear_value_json(line, "number_question")

        if value is not None:

            value = extract_number(value)[0]

            if int(value) < int(number_question)+1:
                key_number = int(value)

                dict_response["question"] = list_questions[key_number-1]
                dict_response["number_question"] = key_number

        value = clear_value_json(line, "quote")
        if value is not None:
            dict_response["quote"] = value

        value = clear_value_json(line, "boolean")
        if value is not None:
            value = validate_boolean(value)
            dict_response["boolean"] = value
    return {"dict_response": dict_response, "key_number": key_number}
