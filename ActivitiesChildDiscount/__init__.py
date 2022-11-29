# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import os
import sys
import re
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Utilities.load_parameter import load_parameters
from Utilities import clear_respond
from Utilities import build_response
from Adapters import adapter_gpt
from Utilities.load_parameter import load_parameters

loaded_parameters = load_parameters()


def main(parametersCancellation: dict) -> dict:

    """
    This is a function for extract child discount of the text
    Args:
        parametersCancellation (dict): This is a dictionary with text and task.
    Returns:
        dict: This is a dictionary with text and mean probability.
    """
    
    logging.warning("Executing ActivitiesChildDiscount")
    parameters = load_parameters()
    is_child = parametersCancellation["is_child"]
    information = parametersCancellation["data_information"]
    text_category_nineteen = parametersCancellation["text_category_nineteen"]
    if is_child:
        question_fare_rules_nineteen = parameters["question_fare_rules_nineteen"]
        question_fare_rules_nineteen = replace_data(
            question_fare_rules_nineteen, information
        )

        structure_fare_rules_nineteen = parameters["structure_fare_rules_nineteen"]
        quiz_text_and_question_five = (
            text_category_nineteen
            + "\n" * 2
            + question_fare_rules_nineteen
            + "\n" * 2
            + structure_fare_rules_nineteen
        )
        
   

        gpt_text_five = adapter_gpt.ask_openai(quiz_text_and_question_five, "list")
        list_answer = []
        gpt_text_five_text = gpt_text_five["text"]
        
        logging.error("!!!!!!!!!!!!!!!!")
        logging.info('Respuesta GPT Porcentaje')
        logging.warning(gpt_text_five_text)
        logging.error("!!!!!!!!!!!!!!!!")

        data = validate_data(gpt_text_five_text)
        respond = build_response.edit_response(
            question_i="5. "
            + question_fare_rules_nineteen.replace(
                '(NOTE: if there is no information in the text respond, "There is no information about it")',
                " ",
            ),
            answer_i=data["answer"],
            category_i=19,
            quote_i=data["quote"],
            freeText_i=True,
            numberQuestion_i=5,
            boolean_i=False if len(list_answer) == 0 else True,
            meanProbability_i=gpt_text_five["meanProbability"],
            value_i=data["value"],
            denomination_i=data["denomination"],
        )

        return respond
    else:

        respond = build_response.edit_response(
            question_i="5. List all the charges shown in the text",
            category_i=19,
            numberQuestion_i=5,
        )
        return respond


def validate_data(gpt_text_five_text: str) -> dict:
    """
    This is a function for validate data to put in Json.
    Args:
        list (list): This is a list with the text to convert.
    Returns:
        str: This is a string with the text converted.
    """
    logging.info("list_to_string")

    text = gpt_text_five_text

    answer = text.upper()
    answer = answer.replace("%", "PERCENT")
    quote = answer.split("QUOTE")
    list_index = [m.start() for m in re.finditer("PERCENT", answer)]

    list_percents = []
    for index in list_index:
        list_percents.append(answer[index - 4 : index + 7])

    list_denomination = loaded_parameters["denomination"].split("\n")

    list_answer = quote[0].split("##")
    percents = [float(s) for s in re.findall(r"-?\d+\.?\d*", str(quote[0]))]

    denomination = [
        value
        for value in list_denomination
        for answer in list_answer
        if value in answer
    ]

    return {
        "quote": quote[1] if len(quote) > 1 else "",
        "answer": list_answer,
        "value": percents,
        "denomination": denomination,
    }


def replace_data(question_fare_rules_nineteen: str, data: dict) -> str:
    """
    This is a function for replace data to put in text
    Args:
        str (str): This is a string with the text to convert.
        data (dict): This is a dictionary with the data to replace.
    Returns:
        str: This is a string with the text converted.

    """
    passengerChild = data["passengerChild"]

    list_questions = []
    for child in passengerChild:

        age = str(child["age"])
        seat = child["seat"]
        accompanied = child["isAccompanied"]

        if seat is True:
            seat = "with a seat"
        else:
            seat = "without a seat"
            
        if accompanied is True:
            accompanied = "and accompanied"
        else:
            accompanied = ""

        text_question = question_fare_rules_nineteen.replace("#{AGE}#", age)
        text_question = text_question.replace("#{SEAT}#", seat)
        text_question = text_question.replace("#{ACCOMPANIED}#", accompanied)
        list_questions.append(text_question)

    question_fare_rules_nineteen = " and ".join(list_questions)

    return question_fare_rules_nineteen
