# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging

from Utilities.validators_respond import validate_date
from Utilities.calculate import overall_average
from Utilities import build_response


def main(listRespond: list) -> list:
    """
    This is a function for sort the respond of the GPT in a JSON.
    Args:
        listRespond (list): This is a list with the respond of the GPT.
    Returns:
        list: This is a list with the respond of the GPT sorted.
    """

    logging.warning("Executing ActivitiesSortAnswer")
    parameters_dict = listRespond[1]
    questions = listRespond[0]

    is_child = parameters_dict["is_child"]
    text_category_sixteen = parameters_dict["text_category_sixteen"]
    text_category_nineteen = parameters_dict["text_category_nineteen"]
    dict_penalty = parameters_dict["dict_penalty"]
    question_list = questions[0]
    percent_child = questions[1]
    departure_date = parameters_dict["data_information"]["departureDate"]

    is_refundable = check_booleans(question_list)
    departure_date_response = build_date_response(departure_date)

    respuesta = {
        "question_1": question_list["question_1"],
        "question_2": question_list["question_2"],
        "question_3": question_list["question_3"],
        "question_4": departure_date_response,
        "question_5": percent_child,
        "question_6": is_refundable,
    }

    average = overall_average(respuesta)

    dict_response = {
        "fareBasis": "",
        "passengerTypes": "",
        "modelRespond": "",
        "average": "",
        "freeText": "",
    }

    if is_child:
        list_free_text = [
            {"category": 16, "text": text_category_sixteen},
            {"category": 19, "text": text_category_nineteen},
        ]
    else:
        list_free_text = [{"category": 16, "text": text_category_sixteen}]

    question_list_respuesta = []
    for value in respuesta.values():
        question_list_respuesta.append(value)

    dict_response["modelRespond"] = question_list_respuesta
    dict_response["average"] = average
    dict_response["freeText"] = list_free_text
    dict_response["fareBasis"] = dict_penalty["fareBasis"]
    dict_response["passengerTypes"] = dict_penalty["passengerTypes"]

    return [dict_response]


def check_booleans(question_dic: dict) -> dict:
    boolean_1 = question_dic["question_1"]["boolean"]
    boolean_2 = question_dic["question_2"]["boolean"]

    validate = boolean_1 and boolean_2
    if validate:
        logging.warning("Refundable")

    respond = build_response.edit_response(
        question_i="6. Is refundable?",
        answer_i="Refundable" if validate else "Not Refundable",
        category_i=16,
        numberQuestion_i=6,
        boolean_i=validate,
    )

    return respond


def build_date_response(departure_date: str):

    date_formated = validate_date(departure_date)

    respond = build_response.edit_response(
        question_i="4. Departure date?",
        answer_i=date_formated,
        quote_i=departure_date,
        numberQuestion_i=4,
        boolean_i=True,
    )
    return respond
