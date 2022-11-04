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
from Utilities import clear_respond

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
    list_questions = dict_question["list_questions"].split(",")
    number_question = dict_question["number_questions"]
    # NOTE
    dict_response = Respond(
        question="",
        answer="",
        category=16,
        quote="",
        freeText=True,
        boolean=False,
        numberQuestion=0,
        meanProbability=score,
        value=[],
        denomination=None,
    ).__dict__
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
    return {"dict_response": dict_response, "key_number": key_number}


def format_text(text: str) -> str:
    """Preprocesses the data text, clean it.

    Args:
        text: String Raw data.
    Returns:
        Preprocessed data text, without stranger character.

    add activate value to test text format from front end
    """
    activate = False
    if activate:
        logging.info("format_text ACTIVATE")
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


def list_to_string(questions: dict) -> dict:
    """
    This is a function for convert a list to string.
    Args:
        list (list): This is a list with the text to convert.
    Returns:
        str: This is a string with the text converted.
    """
    logging.info("list_to_string")
    logging.info(questions["answer"])
    quote = " ".join(questions["quote"])
    answer = ", ".join(questions["answer"][0]).upper().replace("%", "PERCENT")
    list_index = [m.start() for m in re.finditer("PERCENT", answer)]
    logging.error("list_index: %s", list_index)

    list_percents = []
    for index in list_index:
        list_percents.append(answer[index - 4 : index + 7])

    if answer.count(",") < 1:
        for index in list_index:
            answer = answer[: index - 4] + "," + answer[index - 4 :]

    logging.error("answer: %s", answer)
    logging.info("list_percents: %s", list_percents)
    percents = [float(s) for s in re.findall(r"-?\d+\.?\d*", str(list_percents))]
    list_denomination = loaded_parameters["denomination"].split("\n")
    denomination = [value for value in list_denomination if value in list_percents]
    denomination = denomination[0] if len(denomination) > 0 else "PERCENT"
    questions["quote"] = quote
    questions["answer"] = answer.split(",")
    questions["value"] = percents
    questions["denomination"] = clear_respond.format_denomination(denomination).strip()
    return questions


def dict_answer_to_list(question_dic: dict) -> dict:
    """
    This is a function for convert the answer in a list.
    Args:
        question_dic (dict): This is a dictionary with the answer.
    Returns:
        dict: This is a dictionary with the answer in a list.
    """
    logging.info("dict_answer_to_list")

    for key, value in question_dic.items():
        if isinstance(value, dict):
            if isinstance(value["answer"], str):
                question_dic[key]["answer"] = [value["answer"]]
            if value["answer"] == [""]:
                question_dic[key]["answer"] = []
            if type(value["value"]) is not list:
                question_dic[key]["value"] = [value["value"]]

    logging.warning(question_dic)
