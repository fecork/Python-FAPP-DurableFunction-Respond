import azure.durable_functions as df
import logging
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Utilities.load_parameter import load_parameters

parameters = load_parameters()


def pipeline(context: df.DurableOrchestrationContext, parameters_dict: dict):
    """
    This is the main pipeline function. Execute in parallel the activities
    Args:
        context (DurableOrchestrationContext): The context object for durable function
        parameters_dict (dict): This is a dictionary with the parameters
    Returns:
        parameters_dict: This is a dictionary with the respond of the GPT
    """

    parameters_quiz_group_one = build_text(parameters_dict)
    response_quiz_group_one = context.call_activity(
        "ActivitiesExecuteQuiz", parameters_quiz_group_one
    )

    outputs = yield context.task_all([response_quiz_group_one])

    data_respond = [outputs, parameters_dict]

    respuesta = yield context.call_activity(
        "ActivitiesSortAnswerChangeManual", data_respond
    )
    return respuesta


def build_text(parameters_dict: dict) -> dict:
    question_fare_rules = parameters["question_fare_rules_change_manual_group_one"]
    structure_fare_rules = parameters["structure_fare_rules"]
    structure_questions = parameters["structure_fare_rules_change_manual_group_one"]
    text_category_six = parameters_dict["text_category_six"]
    text_category_seven = parameters_dict["text_category_seven"]
    parameters_dict["question_paragraph"] = parameters[
        "question_paragraph_change_manual_group_one"
    ]

    gpt_paragraph_text = (
        "MAXIMUM STAY "
        + "\n"
        + text_category_six
        + "\n"
        + "MINIMUN STAY "
        + text_category_seven
    )

    quiz_text_and_question = (
        gpt_paragraph_text
        + "\n" * 2
        + question_fare_rules
        + "\n" * 2
        + structure_fare_rules
        + "\n" * 2
        + structure_questions
    )

    parameters_quiz = {
        "quiz_text_and_question": quiz_text_and_question,
        "number_questions": parameters["number_question_change_manual_group_one"],
        "list_questions": parameters[
            "list_question_fare_rules_change_manual_group_one"
        ],
        "list_question_charge": parameters[
            "list_question_charge_change_manual_group_one"
        ],
        "task": "change",
    }

    return parameters_quiz
