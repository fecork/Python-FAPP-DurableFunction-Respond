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

    text_category_two = parameters_dict["text_category_two"]
    text_category_three = parameters_dict["text_category_three"]
    text_category_six = parameters_dict["text_category_six"]
    text_category_seven = parameters_dict["text_category_seven"]
    text_category_eight = parameters_dict["text_category_eight"]
    text_category_eleven = parameters_dict["text_category_eleven"]
    text_category_twelve = parameters_dict["text_category_twelve"]

    dict_penalty = parameters_dict["dict_penalty"]

    question_list_group_1 = questions[0]
    question_list_group_2 = questions[1]
    question_list_group_3 = questions[2]

    question_list_group_1["question_1"]["numberQuestion"] = 1
    question_list_group_1["question_2"]["numberQuestion"] = 2
    question_list_group_2["question_1"]["numberQuestion"] = 3
    question_list_group_2["question_2"]["numberQuestion"] = 4
    question_list_group_3["question_1"]["numberQuestion"] = 5
    question_list_group_3["question_2"]["numberQuestion"] = 6

    question_list_group_1["question_1"]["category"] = 6
    question_list_group_1["question_2"]["category"] = 7
    question_list_group_2["question_1"]["category"] = 8
    question_list_group_2["question_2"]["category"] = 11
    question_list_group_3["question_1"]["category"] = 2
    question_list_group_3["question_2"]["category"] = 3

    # TODO: agregar categoria 4 y 12 tal cual
    respuesta = {
        "question_1": question_list_group_1["question_1"],
        "question_2": question_list_group_1["question_2"],
        "question_3": question_list_group_2["question_1"],
        "question_4": question_list_group_2["question_2"],
        "question_5": question_list_group_3["question_1"],
        "question_6": question_list_group_3["question_2"],
    }

    average = overall_average(respuesta)

    dict_response = {
        "fareBasis": "",
        "passengerTypes": "",
        "modelRespond": "",
        "average": "",
        "freeText": "",
    }

    list_free_text = [
        {"category": 2, "text": text_category_two},
        {"category": 3, "text": text_category_three},
        {"category": 6, "text": text_category_six},
        {"category": 7, "text": text_category_seven},
        {"category": 8, "text": text_category_eight},
        {"category": 11, "text": text_category_eleven},
        {"category": 12, "text": text_category_twelve},
    ]

    question_list_respuesta = []
    for value in respuesta.values():
        question_list_respuesta.append(value)

    dict_response["modelRespond"] = question_list_respuesta
    dict_response["average"] = average
    dict_response["freeText"] = list_free_text
    dict_response["fareBasis"] = dict_penalty["fareBasis"]
    dict_response["passengerTypes"] = dict_penalty["passengerTypes"]

    return [dict_response]
