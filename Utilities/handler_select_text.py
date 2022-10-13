import sys
import os


def search_passenger_types(dict_penalty: dict) -> list:
    """
    search passenger types in a json, like adult, child, infant
    Args:
        dict_penalty: json
    Returns:
        list of passenger types
    """
    for key, value in dict_penalty.items():
        if key == "PassengerTypes":
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
        passenger_type = dict_penalty["PassengerTypes"]
        if passenger_type[0] in list_passenger_type:
            list_passenger_type.pop(list_passenger_type.index(passenger_type[0]))
            list_clean.append(dict_penalty)
    return list_clean


def extract_categories(dict_penalty: dict) -> dict:
    """
    extract categories from dict_penalty json and return a dict with categories
    Args:
        dict_penalty: json
    Returns:
        dict of categories
    """

    thereis_sixteen = False
    thereis_nineteen = False
    categorias = dict_penalty["Categories"]
    for dict_category in categorias:
        code = dict_category["Code"]
        if code == "16" and thereis_sixteen == False:
            text_category_sixteen = dict_category["FreeText"]
            thereis_sixteen = True
        if code == "19" and thereis_nineteen == False:
            text_category_nineteen = dict_category["FreeText"]
            thereis_nineteen = True
        if thereis_sixteen and thereis_nineteen:
            break
    return {"16": text_category_sixteen, "19": text_category_nineteen}


def extract_passenger(penalty_text: dict, type_passenger: str) -> list:
    """
    extract dict_penalty by passenger type
    Args:
        dict_penalty: json
    Returns:
        list of adult passenger
    """
    list_clean = []
    for dict_penalty in penalty_text:
        passenger_type = dict_penalty["PassengerTypes"]
        if passenger_type[0].lower() == type_passenger:
            list_clean.append(dict_penalty)
    return list_clean
