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
from Utilities import dto_respond_backend

def main(dictRespond: list) -> list:
    logging.warning("Executing ActivitiesSortAnswer")
    parameters_dict = dictRespond["parameters_dict"]
    dict_penalty = parameters_dict["dict_penalty"]
    model_respond = dictRespond['model_respond']
    average = overall_average(model_respond)
    list_free_text = dictRespond['list_free_text']
    dict_response = build_response_backend(
        model_respond, average, list_free_text, dict_penalty)

    return dict_response

def build_date_response(departure_date: str):
    date_formated = validate_date(departure_date)
    respond = build_response.edit_response(
        question_i="Departure date?",
        answer_i=date_formated,
        quote_i=departure_date,
        numberQuestion_i=6,
        boolean_i=True,
    )
    return respond


def build_response_backend(model_respond: list, average: float, list_free_text: list, dict_penalty: dict):
    dict_response = dto_respond_backend.Respond(
        modelRespond=model_respond,
        average=average,
        freeText=list_free_text,
        fareBasis=dict_penalty["fareBasis"],
        passengerTypes=dict_penalty["passengerTypes"],
    ).__dict__ 
    return [dict_response]
