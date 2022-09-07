# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import os
import sys

import azure.durable_functions as df

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from shared import handler_select_text
from Utilities.load_parameter import load_parameters

parameters = load_parameters()


def orchestrator_function(
    context: df.DurableOrchestrationContext,
):
    parameters = context.get_input()
    parameter_task = parameters["task"]
    parameter_information = parameters["information"]
    parameter_penalty_text = parameters["penaltyText"]

    list_passengers_type = []
    for dict_penalty in parameter_penalty_text:
        passenger_type = handler_select_text.search_passenger_types(
            dict_penalty
        )
        list_passengers_type.append(passenger_type)
        list_passengers_type = list(set(list_passengers_type))

    is_child = False
    if "child" in list_passengers_type:
        is_child = True
    if "infant" in list_passengers_type:
        is_child = True

    parameter_penalty_text = handler_select_text.remove_duplicate_passenger(
        parameter_penalty_text, list_passengers_type
    )

    parameter_penalty_text = handler_select_text.extract_passenger(
        parameter_penalty_text, "adult"
    )
    if parameter_task == "CANCELLATION":
        parameters_cancellation = iterate_penalty_text(
            parameter_penalty_text, parameter_information, is_child
        )

        gpt_response = pipeline(context, parameters_cancellation)

        return gpt_response


main = df.Orchestrator.create(orchestrator_function)


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
        dict_response = iterate_categories(
            dict_penalty, parameter_information, is_child
        )
    return dict_response


def iterate_categories(
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


def pipeline(context: df.DurableOrchestrationContext, parameters_dict: dict):

    question_fare_rules = parameters["question_fare_rules"]
    structure_fare_rules = parameters["structure_fare_rules"]
    data_information = parameters_dict["data_information"]

    logging.warning("wait for gpt_paragraph")
    gpt_paragraph_text = yield context.call_activity(
        "ActivitieExtractParagraph", parameters_dict
    )

    logging.warning("extract text")
    logging.warning("define question")
    quiz_text_and_question = (
        data_information
        + "\n" * 2
        + gpt_paragraph_text
        + "\n" * 2
        + question_fare_rules
        + "\n" * 2
        + structure_fare_rules
    )

    logging.warning("response quiz")
    response_quiz = context.call_activity(
        "ActivitiesExecuteQuiz", quiz_text_and_question
    )

    response_classification = context.call_activity(
        "ActivitiesClassificationRefund", gpt_paragraph_text
    )

    response_child_discount = context.call_activity(
        "ActivitiesChildDiscount", parameters_dict
    )

    outputs = yield context.task_all(
        [response_quiz, response_classification, response_child_discount]
    )

    data_respond = [outputs, parameters_dict]

    respuesta = yield context.call_activity(
        "ActivitiesSortAnswer", data_respond
    )
    return respuesta
