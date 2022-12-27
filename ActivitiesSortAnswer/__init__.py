import logging

from Dominio.Servicios.validators_respond import validate_date
from Dominio.Servicios.calculate import overall_average
from Dominio.Servicios import build_response
from Dominio.Entidades import dto_respond_backend


def main(dictrespond: list) -> list:
    logging.warning("Executing ActivitiesSortAnswer")
    parameters_dict = dictrespond["parameters_dict"]
    dict_penalty = parameters_dict["dict_penalty"]
    model_respond = dictrespond['model_respond']
    average = overall_average(model_respond)
    list_free_text = dictrespond['list_free_text']
    dict_response = build_response_backend(
        model_respond, average, list_free_text, dict_penalty)

    return dict_response


def build_date_response(departure_date: str):
    date_formated = validate_date(departure_date)
    respond = build_response.edit_response(
        question_input="Departure date?",
        answer_input=date_formated,
        quote_input=departure_date,
        number_question_input=6,
        boolean_input=True,
    )
    return respond


def build_response_backend(
        model_respond: list,
        average: float,
        list_free_text: list,
        dict_penalty: dict):
    dict_response = dto_respond_backend.Respond(
        model_respond=model_respond,
        average=average,
        free_text=list_free_text,
        fare_basis=dict_penalty["fareBasis"],
        passenger_types=dict_penalty["passengerTypes"],
    ).__dict__
    return [dict_response]
