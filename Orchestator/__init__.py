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

from Utilities.load_parameter import load_parameters
from Utilities import handler_select_text
from Utilities import object_iterator
from shared import pipeline_change_manual
from shared import pipeline_change
from shared import pipeline_fuel_surcharge

parameters = load_parameters()


def orchestrator_function(
    context: df.DurableOrchestrationContext,
) -> dict:

    parameters = context.get_input()
    parameter_task = parameters["task"]
    parameter_information = parameters["information"]
    parameter_penalty_text = parameters["penaltyText"]

    list_passengers_type = []
    list_passengers = []
    list_farebasis = []
    for dict_penalty in parameter_penalty_text:

        passenger_type = handler_select_text.search_key(dict_penalty, 'passengerTypes')
       
        for passenger in passenger_type:
            list_passengers.append(passenger)
            list_passengers_type.append(passenger)
            is_child = validate_child(passenger)
            if is_child:
                break
       
        farebasis = handler_select_text.search_key(dict_penalty, 'fareBasis')
        list_farebasis.append(farebasis)
        list_passengers_type = list(set(list_passengers_type))


    passengers_type = tuple(list_passengers_type)
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
    parameters_object["dict_penalty"]["fareBasis"] = list_farebasis
    parameters_object["dict_penalty"]["listPassengers"] = list_passengers
    
    if parameter_task == "CANCELLATION":
        gpt_response = pipeline_change.pipeline(context, parameters_object)
        return gpt_response

    if parameter_task == "CHANGE":
        gpt_response = pipeline_change.pipeline(context, parameters_object)
        return gpt_response

    if parameter_task == "AVAILABILITY":

        gpt_response = pipeline_change_manual.pipeline(
            context, parameters_object)

        return gpt_response

    if parameter_task == "FUELSURCHARGE":

        gpt_response = pipeline_fuel_surcharge.pipeline(
            context, parameters_object)

        return gpt_response


main = df.Orchestrator.create(orchestrator_function)


def validate_child(passenger_type: str) -> bool:
    
    if "child" in passenger_type.lower():
        return True
    if "infant" in passenger_type.lower():
        return True
    return False
