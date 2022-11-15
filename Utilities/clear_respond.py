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
from Utilities import clear_respond, build_response

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
    text = text.replace(str("\\n"), "\n")
    text = text.replace(str("/"), " ")
    text = re.sub(r"[^a-zA-Z0-9\s\n;]", "", text)
    return text
