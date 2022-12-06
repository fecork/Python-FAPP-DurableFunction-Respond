# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt




from Utilities.load_parameter import load_parameters
from Utilities.clear_respond import format_text
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
        response = task_fuel_surcharge(parameters)
        
    return response


def task_change(parameters: dict) -> dict:
    """
    Split the text in a list of sentences.
    Args:content: String with the text.
    """
    logging.warning("Executing Change a Cancel Extraction")
    content = format_text(parameters["text_category_sixteen"])
    paragraph = parameters["paragraph"]
    index_change = content.index("CHANGE")
    index_cancellation = content.index("CANCELLATION")

    # when cancellation pilicies go first
    if index_cancellation < index_change:
        cancellations = content[0:index_change]
        changes = content[index_change:]
    # when changes policies go first
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


def task_fuel_surcharge(parameters: dict) -> dict:
    """
    Split the text in a list of sentences.
    Args:content: String with the text.
    """
    logging.warning("Executing Fuel Surcharge Extraction")
    content = format_text(parameters["text_category_twelve"])
    positions = [i for i, word in enumerate(content.split()) if word == "FUEL"]
    long_text = 20
    list_paragraphs = []
    for position in positions:
        pre = content.split()[position: position - long_text:position]
        words = content.split()[position: position + long_text]
        paragraph = " ".join(pre + words)
        list_paragraphs.append(paragraph)

    fuel_text = " ".join(list_paragraphs)
    logging.warning(fuel_text)
    return {"FUELSURCHARGE": fuel_text}
