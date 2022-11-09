# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging

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
    text_category_six = parameters_dict["text_category_six"]
    text_category_seven = parameters_dict["text_category_seven"]
    dict_penalty = parameters_dict["dict_penalty"]

    question_list = questions[0]

    respuesta = {
        "question_1": question_list["question_1"],
        "question_2": question_list["question_2"],
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
            {"category": 6, "text": text_category_six},
            {"category": 7, "text": text_category_seven},
        ]
    else:
        list_free_text = [{"category": 6, "text": text_category_six}]
    # dict_penalty.update({"freeText": list_free_text})

    question_list_respuesta = []
    for value in respuesta.values():
        question_list_respuesta.append(value)

    dict_response["modelRespond"] = question_list_respuesta
    dict_response["average"] = average
    dict_response["freeText"] = list_free_text
    dict_response["fareBasis"] = dict_penalty["fareBasis"]
    dict_response["passengerTypes"] = dict_penalty["passengerTypes"]

    return [dict_response]
