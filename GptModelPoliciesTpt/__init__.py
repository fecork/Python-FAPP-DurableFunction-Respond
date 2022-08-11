import logging
import os
import sys
import json

import azure.functions as func

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)
from shared import pipeline


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    main function to execute the pipeline
    Args: 
        func.HttpRequest
    Returns: 
        func.HttpResponse
    """
    logging.info("Python HTTP trigger function processed a request.")
    parameter_task = get_parameter(req, "task")
    parameter_information = get_parameter(req, "information")
    parameter_penalty_text = get_parameter(req, "penaltyText")

    list_passengers_type = []
    for dict_penalty in parameter_penalty_text:
        passenger_type = search_passenger_types(dict_penalty)
        list_passengers_type.append(passenger_type)
        list_passengers_type = list(set(list_passengers_type))

    parameter_penalty_text = remove_duplicate_passenger(
        parameter_penalty_text, list_passengers_type)

    if parameter_task == "CANCELLATION":
        gpt_response = iterate_penalty_text(
            parameter_penalty_text, parameter_information)
        for elements in gpt_response:
            logging.info(elements["fareBasis"])

        return func.HttpResponse(json.dumps(gpt_response), mimetype="application/json", status_code=200,)
    else:
        return func.HttpResponse(
            """
            This HTTP triggered function executed successfully. 
            Pass a task, rules and information in the query string 
            or in the request body for a gpt response.
            """,
            status_code=200,
        )


def get_parameter(req: object, parameter: str) -> str:
    """
    get the parameter from the request
    Args:
        req: request, parameter: parameter to get
    Returns:
        parameter string
    """
    parameter_string = req.params.get(parameter)
    if not parameter_string:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            parameter_string = req_body.get(parameter)
    return parameter_string


def iterate_penalty_text(penalty_text: list, parameter_information: str) -> list:
    """
    iterate over the penalty text and execute the pipeline
    Args: 
        penalty_text: list of jsons
    Returns:
        list of gpt responses
    """
    lista_respuestas = []
    for dict_penalty in penalty_text:
        dict_response = iterate_categories(dict_penalty, parameter_information)
        lista_respuestas.append(dict_response)
    return lista_respuestas


def iterate_categories(dict_penalty: dict, parameter_information: str) -> dict:
    """
    iterate over the categories and execute the pipeline
    Args: 
        categories: list of jsons
    Returns:
        dict penalty
    """
    categorias = dict_penalty["categories"]
    dict_respond_categories = {}
    for dict_category in categorias:
        code = dict_category['code']
        if code == '16':
            text_category_sixteen = dict_category['freeText']
            model_response = pipeline.execute_concurrent(
                text_category_sixteen, parameter_information)
            dict_respond_categories["modelRespond"] = model_response
            dict_penalty.update(dict_respond_categories)
            dict_penalty.update({"freeText": text_category_sixteen})
            del dict_penalty["categories"]
    return dict_penalty


def search_passenger_types(dict_penalty: dict) -> list:
    """
    search passenger types
    Args:
        dict_penalty: json
    Returns:
        list of passenger types
    """
    for key, value in dict_penalty.items():
        if key == "passengerTypes":
            return value[0]


def remove_duplicate_passenger(penalty_text: list, list_passenger_type: list) -> list:
    """
    remove duplicate passenger types
    Args:
        penalty_text: list of jsons
        list_passenger_type: list of passenger types
    Returns:
        list of jsons
    """

    list_clean = []
    for dict_penalty in penalty_text:
        passenger_type = dict_penalty['passengerTypes']
        if passenger_type[0] in list_passenger_type:
            list_passenger_type.pop(
                list_passenger_type.index(passenger_type[0]))
            list_clean.append(dict_penalty)
    return list_clean
