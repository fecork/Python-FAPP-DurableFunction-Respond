import logging
import os
import sys
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Adapters import adapter_azure_gpt as adapter
from Dominio.Servicios import build_response
from Dominio.Servicios.load_parameter import load_parameters

loaded_parameters = load_parameters()


def main(parameterscancellation: dict) -> dict:

    logging.warning("Executing ActivitiesChildDiscount")
    parameters = load_parameters()
    is_child = parameterscancellation["is_child"]
    information = parameterscancellation["data_information"]
    text_category_nineteen = parameterscancellation["text_category_nineteen"]
    if is_child:
        question_fare_rules_nineteen = parameters[
                "question_fare_rules_nineteen"
                ]
        question_fare_rules_nineteen = replace_data(
            question_fare_rules_nineteen, information
        )

        structure_fare_rules_nineteen = parameters[
            "structure_fare_rules_nineteen"
            ]
        quiz_text_and_question_five = (
            text_category_nineteen
            + "\n" * 2
            + question_fare_rules_nineteen
            + "\n" * 2
            + structure_fare_rules_nineteen
        )

        gpt_text_five = adapter.ask_openai(
            quiz_text_and_question_five, "list")
        list_answer = []
        gpt_text_five_text = gpt_text_five["text"]
        data = validate_data(gpt_text_five_text)
        respond = build_response.edit_response(
            question_input=question_fare_rules_nineteen,
            number_question_input=5,
            answer_input=data["answer"],
            category_input=19,
            quote_input=data["quote"],
            free_text_input=True,
            boolean_input=False if len(list_answer) == 0 else True,
            mean_probability_input=gpt_text_five["meanProbability"],
            value_input=data["value"],
            denomination_input=data["denomination"],
        )

        return respond
    else:

        respond = build_response.edit_response(
            question_input="List all the charges shown in the text",
            category_input=19,
            number_question_input=5,
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
        list_percents.append(answer[index - 4: index + 7])

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
    passengerchild = data["passengerChild"]

    list_questions = []
    for child in passengerchild:

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
