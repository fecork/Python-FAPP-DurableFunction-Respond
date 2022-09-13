import logging
import spacy
import os
import sys

import pandas as pd
from typing import Dict

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)
from validators_respond import (
    validate_charge_number,
    validate_structure_json,
)
from Utilities.load_parameter import load_parameters
from Utilities.clear_respond import execute_clean_json

nlp = spacy.load("en_core_web_sm")
loaded_parameters = load_parameters()
list_questions = loaded_parameters["list_question_fare_rules"].split(",")
number_question = loaded_parameters["number_question"]


def paragraph_segmentation(text: str) -> list:
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
            yield document[start : token.i]
            start = token.i
    yield document[start:]


def iterate_paragraphs(dataset: dict, score: float) -> pd.DataFrame:
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
        dict_questions = text_to_json(list_probe, score)
        dict_responses[partition_id] = dict_questions
        id_file.append(partition_id)

    respond = pd.DataFrame(dict_responses)
    return respond


def individual_paragraphs(text: str, score: float) -> Dict:
    """
    function to iterate over the paragraphs in the dataset
    Args:
        text: text to iterate
    return:
        dictionary with the information of the paragraphs
    """

    paragraph_detected = paragraph_segmentation(text)

    list_probe = split_paragraph(paragraph_detected)
    dict_questions = text_to_json(list_probe, score)
    return dict_questions


def split_paragraph(paragraph_detected: list) -> list:
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


def text_to_json(list_probe: list, score: float) -> dict:
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
        response_clean = execute_clean_json(score, text)
        dict_questions[
            "question_" + str(response_clean["key_number"])
        ] = response_clean["dict_response"]

    dict_questions = validate_charge_number(dict_questions)
    dict_questions = validate_structure_json(dict_questions)
    return dict_questions
