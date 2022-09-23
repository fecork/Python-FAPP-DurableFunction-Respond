# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging


def main(listRespond: list) -> list:
    """
    This is a function for sort the respond of the GPT in a JSON.
    Args:
        listRespond (list): This is a list with the respond of the GPT.
    Returns:
        list: This is a list with the respond of the GPT sorted.
    """

    logging.warning("Executing ActivitiesSortAnswer")
    parameters_dict = listRespond[1]
    questions = listRespond[0]

    is_child = parameters_dict["is_child"]
    text_category_sixteen = parameters_dict["text_category_sixteen"]
    text_category_nineteen = parameters_dict["text_category_nineteen"]
    dict_penalty = parameters_dict["dict_penalty"]

    lista = questions[0]

    respuesta = {
        "question_1": lista["question_1"],
        "question_2": lista["question_2"],
        "question_3": lista["question_3"],
        "question_4": questions[1],
        "question_5": questions[2],
    }

    dict_response = {
        "fareBasis": "",
        "passengerTypes": "",
        "modelRespond": "",
        "freeText": "",
    }

    if is_child:
        list_free_text = [
            {"category": 16, "text": text_category_sixteen},
            {"category": 19, "text": text_category_nineteen},
        ]
    else:
        list_free_text = [{"category": 16, "text": text_category_sixteen}]
    # dict_penalty.update({"freeText": list_free_text})

    lista_respuesta = []
    for value in respuesta.values():
        lista_respuesta.append(value)

    dict_response["modelRespond"] = lista_respuesta
    dict_response["freeText"] = list_free_text
    dict_response["fareBasis"] = dict_penalty["fareBasis"]
    dict_response["passengerTypes"] = dict_penalty["passengerTypes"]

    return [dict_response]


def validate_number(text):
    """
    This is a function for validate if the text is a number.
    Args:
        txt (str): This is a string with the text to validate.
    Returns:
        bool: This is a boolean with the result of the validation.
    """
    for words in text.split():
        if words.isdigit():
            return True
        else:
            return False
