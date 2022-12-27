from Dominio.Servicios.load_parameter import load_parameters
from Dominio.Servicios.clear_respond import format_text
from Adapters import adapter_ls
import logging
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

parameters = load_parameters()


def main(parameters: dict) -> dict:
    """
    Split the text in a list of sentences.
    Args:content: String with the text.
    Returns: List of sentences.
    """
    logging.warning("Executing ActivitiesExtractParagraph")

    task = parameters["task"]
    if task == "CHANGE" or task == "CANCELLATION":
        response = task_change(parameters)
    if task == "FUELSURCHARGE":
        select_text = text_segementation(
            "text_category_twelve", "FUEL", parameters)
        if len(select_text) > 0:
            response = {"FUELSURCHARGE": select_text}
        elif len(parameters["text_category_twelve"]) > 2000:
            response = {
                "FUELSURCHARGE": parameters["text_category_twelve"][:2000]}
        else:
            response = {"FUELSURCHARGE": parameters["text_category_twelve"]}
    if task == "DEPARTUREDATE":
        select_text = text_segementation(
            "text_category_twelve", "DEPARTURE", parameters)
        if len(select_text) > 0:
            response = {"DEPARTUREDATE": select_text}
        else:
            response = {"DEPARTUREDATE": parameters["text_category_twelve"]}

    return response


def task_change(parameters: dict) -> dict:
    """
    Split the text in a list of sentences.
    Args:content: String with the text.
    """
    logging.warning("Executing Change a Cancel Extraction")
    content = format_text(parameters["text_category_sixteen"], False)
    paragraph = parameters["paragraph"]
    index_change = content.index("CHANGE")
    index_cancellation = content.index("CANCELLATION")

    if index_cancellation < index_change:
        cancellations = content[0:index_change]
        changes = content[index_change:]
    else:
        changes = content[0:index_cancellation]
        cancellations = content[index_cancellation:]

    dict_split_text = {"CANCELLATION": cancellations, "CHANGE": changes}
    respond = dict_split_text[paragraph]

    if len(respond) > 5000:
        logging.warning(
            "ActivitiesExtractParagraph: Text is too long, summarizing")
        respond = adapter_ls.main(respond)
    return respond


def text_segementation(
        category: str,
        word_to_search: str,
        parameters: dict) -> str:
    """
    Split the text in a list of sentences.
    Args:content: String
    """
    logging.warning("Executing Fuel Surcharge Extraction")
    content = format_text(parameters[category], False)
    positions = [i for i, word in enumerate(
        content.split()) if word == word_to_search]
    long_text = 20
    list_paragraphs = []
    for position in positions:
        pre = content.split()[position: position - long_text:position]
        words = content.split()[position: position + long_text]
        paragraph = " ".join(pre + words)
        list_paragraphs.append(paragraph)

    full_text = " ".join(list_paragraphs)
    return full_text
