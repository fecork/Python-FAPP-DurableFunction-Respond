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

parameters = load_parameters()


def orchestrator_function(context: df.DurableOrchestrationContext) -> dict:

    parameters_dict = context.get_input()

    question_fare_rules = parameters["question_fare_rules_cancellation"]
    structure_fare_rules = parameters["structure_fare_rules"]
    structure_questions = parameters["structure_fare_rules_cancellation"]
    data_information = parameters_dict["data_information"]
    parameters_dict["question_paragraph"] = parameters[
        "question_paragraph_cancellation"
    ]
    parameters_dict["paragraph"] = "CANCELLATION"

    try:
        gpt_paragraph_text = yield context.call_activity(
            "ActivitieExtractParagraphIndex", parameters_dict
        )
    except Exception as e:
        logging.error("Error in ActivitieExtractParagraphIndex")
        logging.error(e)

    quiz_text_and_question = (
        data_information
        + "\n" * 2
        + gpt_paragraph_text
        + "\n" * 2
        + question_fare_rules
        + "\n" * 2
        + structure_fare_rules
        + "\n" * 2
        + structure_questions
    )

    parameters_quiz = {
        "quiz_text_and_question": quiz_text_and_question,
        "number_questions": parameters["number_question_cancellation"],
        "list_questions": parameters["list_question_fare_rules_cancellation"],
        "list_question_charge": parameters["list_question_charge_cancellation"],
        "task": "cancellation",
    }

    response_quiz = context.call_activity("ActivitiesExecuteQuiz", parameters_quiz)

    response_child_discount = context.call_activity(
        "ActivitiesChildDiscount", parameters_dict
    )

    outputs = yield context.task_all([response_quiz, response_child_discount])

    data_respond = [outputs, parameters_dict]

    respuesta = yield context.call_activity("ActivitiesSortAnswer", data_respond)
    return respuesta


main = df.Orchestrator.create(orchestrator_function)