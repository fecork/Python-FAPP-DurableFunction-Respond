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


    logging.warning("Executing ActivitiesSortAnswerDepartureDate")
    parameters_dict = listRespond[1]
    questions = listRespond[0]

    # is_child = parameters_dict["is_child"]
    text_category_twelve = parameters_dict["text_category_twelve"]
    # text_category_sixteen = parameters_dict["text_category_sixteen"]
    # text_category_nineteen = parameters_dict["text_category_nineteen"]
    dict_penalty = parameters_dict["dict_penalty"]

    question_list = questions[0]

    # departure_date = parameters_dict["data_information"]["departureDate"]
    # departure_date_response = build_date_response(departure_date)
    

    for key,value in question_list.items():
        value["category"] = 12

    respuesta = {
        "question_1": question_list["question_1"],
        "question_2": question_list["question_2"],
        # "question_3": question_list["question_3"],
        # "question_4": question_list["question_4"],
        # "question_5": departure_date_response,
    }

    average = overall_average(respuesta)
    # dict_answer_to_list(respuesta)

    dict_response = {
        "fareBasis": "",
        "passengerTypes": "",
        "modelRespond": "",
        "average": "",
        "freeText": "",
    }
    
    list_free_text = [{"category": 12, "text": text_category_twelve}]

    question_list_respuesta = []
    for value in respuesta.values():
        question_list_respuesta.append(value)

    dict_response["modelRespond"] = question_list_respuesta
    dict_response["average"] = average
    dict_response["freeText"] = list_free_text
    dict_response["fareBasis"] = dict_penalty["fareBasis"]
    dict_response["passengerTypes"] = dict_penalty["passengerTypes"]

    return [dict_response]
