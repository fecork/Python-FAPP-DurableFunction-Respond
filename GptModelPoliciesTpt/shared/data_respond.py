import logging
import spacy
import os
import sys

import pandas as pd
from typing import Dict

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from shared.load_parameter import load_parameters
from validators_respond import (
    validate_boolean,
    validate_charge_number,
    validate_structure_json,
)

nlp = spacy.load("en_core_web_sm")
loaded_parameters = load_parameters()
list_questions = loaded_parameters["list_question_fare_rules"].split(",")
number_question = loaded_parameters["number_question"]


def paragraph_segmentation(text: str):
    """
    Function to segment paragraphs in a text
    Args:
        text: text to segment
    return:
        list of paragraphs in yield
    """
    sentence = []
    doc = nlp(text)
    document = nlp(text)

    for sent in doc.sents:
        sentence.append(sent.text)

    start = 0
    for token in document:

        if token.is_space and token.text.count("\n") > 1:
            yield document[start: token.i]
            start = token.i
    yield document[start:]


def iterate_paragraphs(dataset):
    
    """
    function to iterate over the paragraphs in the dataset
    in Kedro
    Args:
        dataset: dataset to iterate
    return:
        dataframe with the information of the paragraphs
    """

    dict_responses = {}
    id_file = []

    for partition_id, partition_load_func in dataset.items():
        text = partition_load_func()
        text = text.replace("{", "")
        text = text.replace("}", "")
        paragraph_detected = paragraph_segmentation(text)

        list_probe = split_paragraph(paragraph_detected)
        dict_questions = text_to_json(list_probe)
        dict_responses[partition_id] = dict_questions
        id_file.append(partition_id)

    respond = pd.DataFrame(dict_responses)
    return respond


def individual_paragraphs(text: str) -> Dict:
    """
    function to iterate over the paragraphs in the dataset
    Args:
        text: text to iterate
    return:
        dictionary with the information of the paragraphs
    """

    paragraph_detected = paragraph_segmentation(text)

    list_probe = split_paragraph(paragraph_detected)
    dict_questions = text_to_json(list_probe)
    return dict_questions

def split_paragraph(paragraph_detected: list)->list:
    """
    split the paragraphs in the text
    Args:
        paragraph_detected: list of paragraphs
    return:
        list of paragraphs
    """
    list_format_text = []
    for paragraph in paragraph_detected:
        content = paragraph.text
        if "number_question" in content:
            list_format_text.append(content)

    return list_format_text


def text_to_json(list_probe):
    # TODO: Arreglar complejidad
    """
    function to transform the text in json
    Args:
        list_probe: list of paragraphs
    return:
        dictionary with the information of the paragraphs
    """
    dict_questions = {}

    for paragraphs in list_probe:
        text = paragraphs.split("\n")
        dict_response = {"answer": "",
                         "quote": "",
                         "boolean": ""
                         }

        for line in text:

            value = clear_value_json(line, "answer")
            if value is not None:
                dict_response["answer"] = value

            value = clear_value_json(line, "number_question")

            if value is not None:
                if int(value) < int(number_question):
                    key_number = int(value)

                    dict_response["question"] = list_questions[key_number-1]

            value = clear_value_json(line, "quote")
            if value is not None:
                dict_response["quote"] = value

            value = clear_value_json(line, "boolean")
            if value is not None:
                value = validate_boolean(value)
                dict_response["boolean"] = value

        dict_questions["question_" + str(key_number)] = dict_response

    dict_questions = validate_charge_number(dict_questions)
    dict_questions = validate_structure_json(dict_questions)
    logging.warning(dict_questions)
    return dict_questions


def clear_value_json(line, key):
    key_json = key.translate({ord(i): None for i in ":"})

    if "quote" in line:
        line = line.replace("\n", " ")

    if key_json in line:
        res = line.replace(key, "")
        res = res.translate({ord(i): None for i in '",:'})
        res = res.strip()
        return res
