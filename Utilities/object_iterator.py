import logging
from Utilities import handler_select_text


def iterate_penalty_text(
    penalty_text: list, parameter_information: str, is_child: bool
) -> list:
    """
    iterate over the penalty text and execute the pipeline
    Args:
        penalty_text: list of jsons
    Returns:
        list of gpt responses
    """
    for dict_penalty in penalty_text:
        dict_response = iterate_categories_in_penalties(
            dict_penalty, parameter_information, is_child
        )

    return dict_response


def iterate_categories_in_penalties(
    dict_penalty: dict, parameter_information: str, is_child: bool
) -> dict:
    """
    iterate over the categories and execute the pipeline
    Args:
        categories: list of jsons
    Returns:
        dict penalty
    """
    result_categories = handler_select_text.extract_categories(dict_penalty)
    text_category_sixteen = result_categories["16"]
    text_category_nineteen = result_categories["19"]

    dict_parameters = {
        "text_category_sixteen": text_category_sixteen,
        "text_category_nineteen": text_category_nineteen,
        "data_information": parameter_information,
        "is_child": is_child,
        "dict_penalty": dict_penalty,
    }
    return dict_parameters
