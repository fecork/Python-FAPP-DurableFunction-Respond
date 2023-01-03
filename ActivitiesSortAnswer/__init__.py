import logging

from Dominio.Servicios.calculate import overall_average
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
