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

    is_child = True if "child" in list_passengers_type else False
    parameter_penalty_text = remove_duplicate_passenger(
        parameter_penalty_text, list_passengers_type)

    parameter_penalty_text = extract_passenger(parameter_penalty_text, 'adult')

    if parameter_task == "CANCELLATION":
        gpt_response = iterate_penalty_text(
            parameter_penalty_text, parameter_information, is_child)
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


def iterate_penalty_text(penalty_text: list, parameter_information: str, is_child: bool) -> list:
    """
    iterate over the penalty text and execute the pipeline
    Args: 
        penalty_text: list of jsons
    Returns:
        list of gpt responses
    """
    lista_respuestas = []
    for dict_penalty in penalty_text:
        dict_response = iterate_categories(
            dict_penalty, parameter_information, is_child)
        lista_respuestas.append(dict_response)
    return lista_respuestas


def iterate_categories(dict_penalty: dict, parameter_information: str, is_child: bool) -> dict:
    """
    iterate over the categories and execute the pipeline
    Args: 
        categories: list of jsons
    Returns:
        dict penalty
    """
    result_categories = extract_categories(dict_penalty)
    text_category_sixteen = result_categories['16']
    text_category_nineteen = result_categories['19']

    dict_respond_categories = {}

    model_response = pipeline.execute_concurrent(
        text_category_sixteen, text_category_nineteen, parameter_information, is_child)
    dict_respond_categories["modelRespond"] = model_response
    dict_penalty.update(dict_respond_categories)
    list_free_text = [
        {"category": 16, "text": text_category_sixteen}, 
        {"category": 19, "text": text_category_nineteen}]
    dict_penalty.update({"freeText": list_free_text})
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


def extract_categories(dict_penalty: dict) -> dict:
    """
    extract categories
    Args:
        dict_penalty: json
    Returns:
        dict of categories
    """

    thereis_sixteen = False
    thereis_nineteen = False
    categorias = dict_penalty["categories"]
    for dict_category in categorias:
        code = dict_category['code']
        if code == '16' and thereis_sixteen == False:
            text_category_sixteen = dict_category['freeText']
            thereis_sixteen = True
        if code == '19' and thereis_nineteen == False:
            text_category_nineteen = dict_category['freeText']
            thereis_nineteen = True
        if thereis_sixteen and thereis_nineteen:
            break
    return {'16': text_category_sixteen, '19': text_category_nineteen}


def extract_passenger(penalty_text: dict, type_passenger: str) -> list:
    """
    extract adult passenger
    Args:
        dict_penalty: json
    Returns:
        dict of adult passenger
    """
    list_clean = []
    for dict_penalty in penalty_text:
        passenger_type = dict_penalty['passengerTypes']
        if passenger_type[0].lower() == type_passenger:
            list_clean.append(dict_penalty)
    return list_clean
