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

from shared import pipeline_cancel
from shared import pipeline_change
from Utilities import object_iterator
from Utilities import handler_select_text
from Utilities.load_parameter import load_parameters

parameters = load_parameters()


def orchestrator_function(
    context: df.DurableOrchestrationContext,
) -> dict:
    """
    This is the main orchestrator function.
    Args:
        context (DurableOrchestrationContext): The context object for the
    Returns:
        dict: This is a dictionary with the respond of the GPT
    """
    parameters = context.get_input()
    parameter_task = parameters["task"]
    parameter_information = parameters["information"]
    parameter_penalty_text = parameters["penaltyText"]

    list_passengers_type = []
    for dict_penalty in parameter_penalty_text:
        passenger_type = handler_select_text.search_passenger_types(dict_penalty)
        list_passengers_type.append(passenger_type)
        list_passengers_type = list(set(list_passengers_type))

    is_child = False
    passengers_type = tuple(list_passengers_type)

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

    parameters_object = object_iterator.iterate_penalty_text(
        parameter_penalty_text, parameter_information, is_child
    )

    parameters_object["task"] = parameter_task
    parameters_object["dict_penalty"]["passengerTypes"] = list(passengers_type)
    if parameter_task == "CANCELLATION":

        gpt_response = pipeline_cancel.pipeline(context, parameters_object)

        return gpt_response

    if parameter_task == "CHANGE":

        gpt_response = pipeline_change.pipeline(context, parameters_object)

        return gpt_response


main = df.Orchestrator.create(orchestrator_function)
