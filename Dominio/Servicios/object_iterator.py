from Dominio.Servicios import handler_select_text


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

    dict_parameters = {
        "text_category_2": result_categories["2"],
        "text_category_3": result_categories["3"],
        "text_category_6": result_categories["6"],
        "text_category_7": result_categories["7"],
        "text_category_8": result_categories["8"],
        "text_category_11": result_categories["11"],
        "text_category_12": result_categories["12"],
        "text_category_16": result_categories["16"],
        "text_category_19": result_categories["19"],
        "name_category_2": result_categories["name_2"],
        "name_category_3": result_categories["name_3"],
        "name_category_6": result_categories["name_6"],
        "name_category_7": result_categories["name_7"],
        "name_category_8": result_categories["name_8"],
        "name_category_11": result_categories["name_11"],
        "name_category_12": result_categories["name_12"],
        "name_category_16": result_categories["name_16"],
        "name_category_19": result_categories["name_19"],
        "list_categories": result_categories["list_categories"],
        "data_information": parameter_information,
        "is_child": is_child,
        "dict_penalty": dict_penalty,
    }

    return dict_parameters
