# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging


def main(name: list) -> list:
    parameters_dict = name[1]
    questions = name[0]

    is_child = parameters_dict["is_child"]
    text_category_sixteen = parameters_dict["text_category_sixteen"]
    text_category_nineteen = parameters_dict["text_category_nineteen"]
    logging.info(parameters_dict["dict_penalty"])
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

    dict_response["modelRespond"] = [respuesta]
    dict_response["freeText"] = list_free_text
    dict_response["fareBasis"] = dict_penalty["fareBasis"]
    dict_response["passengerTypes"] = dict_penalty["passengerTypes"]

    return [dict_response]
