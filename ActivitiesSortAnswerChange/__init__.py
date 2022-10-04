# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
from Utilities import dto_respond


def main(listRespond: list) -> list:
    """
    This is a function for sort the respond of the GPT in a JSON.
    Args:
        listRespond (list): This is a list with the respond of the GPT.
    Returns:
        list: This is a list with the respond of the GPT sorted.
    """

    logging.warning("Executing ActivitiesSortAnswerChange")
    parameters_dict = listRespond[1]
    questions = listRespond[0]

    is_child = parameters_dict["is_child"]
    text_category_sixteen = parameters_dict["text_category_sixteen"]
    text_category_nineteen = parameters_dict["text_category_nineteen"]
    dict_penalty = parameters_dict["dict_penalty"]

    lista = questions[0]
    logging.info("REVISAR RESPUESTAS")
    logging.warning(lista)

    respuesta = {
        "question_1": lista["question_1"],
        "question_2": lista["question_2"],
        "question_3": lista["question_3"],
        "question_4": lista["question_4"],
        "question_5": lista["question_5"],
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


# def ver_booleans(lista):
#     boolean_1 = lista["question_1"]["boolean"]
#     boolean_2 = lista["question_2"]["boolean"]
#     boolean_3 = lista["question_3"]["boolean"]
#     validate = boolean_1 and boolean_2 and boolean_3
#     if validate:
#         print("Refundable")

#     respond = dto_respond.Respond(
#         question="4. Is refundable?",
#         answer="Refundable" if validate else "Non Refundable",
#         category=16,
#         quote="",
#         freeText=False,
#         numberQuestion=4,
#         boolean=validate,
#         meanProbability=0,
#         value=None,
#         denomination=None,
#     ).__dict__

#     return respond


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


def list_to_string(questions):
    """
    This is a function for convert a list to string.
    Args:
        list (list): This is a list with the text to convert.
    Returns:
        str: This is a string with the text converted.
    """

    questions["quote"] = "---".join(questions["quote"])
    questions["answer"] = "---".join(questions["answer"])
    return questions
