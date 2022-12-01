import sys
import os
import logging


def search_passenger_types(dict_penalty: dict) -> list:
    """
    search passenger types in a json, like adult, child, infant
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
        passenger_type = dict_penalty["passengerTypes"]
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

    thereis_two = False
    thereis_three = False
    thereis_six = False
    thereis_seven = False
    thereis_eight = False
    thereis_eleven = False
    thereis_twelve = False
    thereis_sixteen = False
    thereis_nineteen = False

    text_category_two = ""
    text_category_three = ""
    text_category_six = ""
    text_category_seven = ""
    text_category_eight = ""
    text_category_eleven = ""
    text_category_twelve = ""
    text_category_sixteen = ""
    text_category_nineteen = ""

    categorias = dict_penalty["categories"]
    for dict_category in categorias:
        code = dict_category["code"]
        if code == "16" and thereis_sixteen == False:
            text_category_sixteen = dict_category["freeText"]
            thereis_sixteen = True
        if code == "19" and thereis_nineteen == False:
            text_category_nineteen = dict_category["freeText"]
            thereis_nineteen = True
        if code == "6" and thereis_six == False:
            text_category_six = dict_category["freeText"]
            thereis_six = True
        if code == "7" and thereis_seven == False:
            text_category_seven = dict_category["freeText"]
            thereis_seven = True
        if code == "8" and thereis_eight == False:
            text_category_eight = dict_category["freeText"]
            thereis_eight = True
        if code == "11" and thereis_eleven == False:
            text_category_eleven = dict_category["freeText"]
            thereis_eleven = True
        if code == "2" and thereis_two == False:
            text_category_two = dict_category["freeText"]
            thereis_two = True
        if code == "3" and thereis_three == False:
            text_category_three = dict_category["freeText"]
            thereis_three = True
        if code == "12" and thereis_twelve == False:
            text_category_twelve = dict_category["freeText"]
            thereis_twelve = True

        if (
            thereis_sixteen
            and thereis_nineteen
            and thereis_six
            and thereis_seven
            and thereis_eight
            and thereis_two
            and thereis_three
            and thereis_eleven
            and thereis_twelve
        ):
            break
    return {
        "2": text_category_two,
        "3": text_category_three,
        "6": text_category_six,
        "7": text_category_seven,
        "8": text_category_eight,
        "11": text_category_eleven,
        "12": text_category_twelve,
        "16": text_category_sixteen,
        "19": text_category_nineteen,
    }


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
        passenger_type = dict_penalty["passengerTypes"]
        passenger_type.sort()
        if passenger_type[0].lower() == type_passenger:
            list_clean.append(dict_penalty)
    return list_clean
