import logging
import sys
import os
import re
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)
from Utilities.dto_respond import Respond
from validators_respond import validate_boolean
from Utilities.load_parameter import load_parameters

loaded_parameters = load_parameters()


def clear_value_json(line: str, key: str) -> str:
    """
    clear the text from the value
    Args:
        line: line to clear the value
        key: key to clear the value
    return:
        value of the key
    """
    # logging.info("clear_value_json")
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
    # logging.info("extract_number")
    list_number = []
    for text in sentence.split():
        try:
            list_number.append(float(text))
        except ValueError:
            pass
    return list_number


def execute_clean_json(score, text: str, dict_question: dict) -> dict:
    """
    block to execute the clean json
    Args:
        score: score of the text
        text: text to clean
    return:
        dictionary with the information of the paragraphs
    """
    logging.info("execute_clean_json")
    list_questions = dict_question["list_questions"].split(",")
    number_question = dict_question["number_questions"]
    logging.info(list_questions)
    logging.info(number_question)
    dict_response = Respond(
        question="",
        answer="",
        category=16,
        quote="",
        freeText=True,
        boolean=False,
        numberQuestion=0,
        meanProbability=score,
        value=None,
        denomination=None,
    ).__dict__
    key_number = ""

    for line in text:

        value = clear_value_json(line, "answer")
        if value is not None:
            dict_response["answer"] = value

        value = clear_value_json(line, "number_question")

        if value is not None:

            value = extract_number(value)[0]

            if int(value) < int(number_question) + 1:
                key_number = int(value)

                dict_response["question"] = list_questions[key_number - 1]
                dict_response["numberQuestion"] = key_number

                if key_number == 3:
                    dict_response["freeText"] = False

        value = clear_value_json(line, "quote")
        if value is not None:
            dict_response["quote"] = value

        value = clear_value_json(line, "boolean")
        if value is not None:
            value = validate_boolean(value)
            dict_response["boolean"] = value
    return {"dict_response": dict_response, "key_number": key_number}


def format_text(text: str) -> str:
    """Preprocesses the data text, clean it.

    Args:
        text: String Raw data.
    Returns:
        Preprocessed data text, without stranger character.
    """
    logging.info("format_text")
    text = text.replace(str("\\n"), "\n")
    text = text.replace(str("/"), " ")
    text = re.sub(r"[^a-zA-Z0-9\s\n.,;]", "", text)
    return text


def format_denomination(text: str) -> str:
    """Preprocesses the data text, clean it.

    Args:
        text: String Raw data.
    Returns:
        Preprocessed data text, without stranger character.
    """
    logging.info("format_denomination")
    text = text.replace(str("\\n"), "\n")
    text = text.replace(str("/"), " ")
    text = re.sub(r"[^a-zA-Z0-9\s\n;]", "", text)
    return text


def list_to_string(questions):
    """
    This is a function for convert a list to string.
    Args:
        list (list): This is a list with the text to convert.
    Returns:
        str: This is a string with the text converted.
    """

    questions["quote"] = "---".join(questions["quote"])
    questions["answer"] = "---".join(questions["answer"])
    return questions
