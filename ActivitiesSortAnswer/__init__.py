# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging

from numpy import number
from Utilities import dto_respond

from Utilities.validators_respond import validate_date
from Utilities.clear_respond import list_to_string
from Utilities.calculate import overall_average


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
    question_with_date = "question_3"
    question_list = questions[0]
    answer_5 = questions[1]

    question_list[question_with_date]["answer"] = validate_date(
        question_list[question_with_date]["quote"]
    )

    answer_5 = list_to_string(answer_5)
    answer_4 = check_booleans(question_list)

    question_list["question_4"]["numberQuestion"] = question_list["question_4"][
        "numberQuestion"
    ] = 6
    answer_6 = question_list["question_4"]

    respuesta = {
        "question_1": question_list["question_1"],
        "question_2": question_list["question_2"],
        "question_3": question_list["question_3"],
        "question_4": answer_4,
        "question_5": answer_5,
        "question_6": answer_6,
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

    # sort dict_response by key
    # dict_response = dict(sorted(dict_response.items(), key=lambda item: item[0]))

    return [dict_response]


def check_booleans(question_list: dict) -> dict:
    boolean_1 = question_list["question_1"]["boolean"]
    boolean_2 = question_list["question_2"]["boolean"]
    boolean_3 = question_list["question_3"]["boolean"]
    validate = boolean_1 and boolean_2 and boolean_3
    if validate:
        print("Refundable")

    respond = dto_respond.Respond(
        question="4. Is refundable?",
        answer="Refundable" if validate else "Not Refundable",
        category=16,
        quote="",
        freeText=False,
        numberQuestion=4,
        boolean=validate,
        meanProbability=0,
        value=None,
        denomination=None,
    ).__dict__

    return respond
