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


def main(listRespond: list) -> list:
    """
    This is a function for sort the respond of the GPT in a JSON.
    Args:
        listRespond (list): This is a list with the respond of the GPT.
    Returns:
        list: This is a list with the respond of the GPT sorted.
    """

    logging.warning("Executing ActivitiesSortAnswerChange")
    parameters_dict = listRespond[1]
    questions = listRespond[0]

    is_child = parameters_dict["is_child"]
    text_category_sixteen = parameters_dict["text_category_sixteen"]
    text_category_nineteen = parameters_dict["text_category_nineteen"]
    dict_penalty = parameters_dict["dict_penalty"]
    question_with_date = "question_5"

    question_list = questions[0]

    question_list[question_with_date]["Answer"] = validate_date(
        question_list[question_with_date]["Answer"]
    )

    respuesta = {
        "question_1": question_list["question_1"],
        "question_2": question_list["question_2"],
        "question_3": question_list["question_3"],
        "question_4": question_list["question_4"],
        "question_5": question_list["question_5"],
    }

    average = overall_average(respuesta)

    dict_response = {
        "FareBasis": "",
        "PassengerTypes": "",
        "ModelRespond": "",
        "Average": "",
        "FreeText": "",
    }

    if is_child:
        list_free_text = [
            {"Category": 16, "Text": text_category_sixteen},
            {"Category": 19, "Text": text_category_nineteen},
        ]
    else:
        list_free_text = [{"Category": 16, "Text": text_category_sixteen}]
    # dict_penalty.update({"freeText": list_free_text})

    question_list_respuesta = []
    for value in respuesta.values():
        question_list_respuesta.append(value)

    dict_response["ModelRespond"] = question_list_respuesta
    dict_response["Average"] = average
    dict_response["FreeText"] = list_free_text
    dict_response["FareBasis"] = dict_penalty["FareBasis"]
    dict_response["PassengerTypes"] = dict_penalty["passengerTypes"]

    return [dict_response]
