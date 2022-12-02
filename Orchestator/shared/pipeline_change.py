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

    question_fare_rules = parameters["question_fare_rules_change"]
    structure_fare_rules = parameters["structure_fare_rules"]
    structure_questions = parameters["structure_fare_rules_change"]

    parameters_dict["question_paragraph"] = parameters["question_paragraph_change"]

    parameters_dict["paragraph"] = "CHANGE"

    try:
        gpt_paragraph_text = yield context.call_activity(
            "ActivitieExtractParagraphIndex", parameters_dict
        )
    except Exception as e:
        logging.error("Error in ActivitieExtractParagraphIndex")
        logging.error(e)

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
        "number_questions": parameters["number_question_change"],
        "list_questions": parameters["list_question_fare_rules_change"],
        "list_question_charge": parameters["list_question_charge_change"],
        "task": "change",
    }

    response_quiz = context.call_activity("ActivitiesExecuteQuiz", parameters_quiz)
    
    response_child_discount = context.call_activity(
        "ActivitiesChildDiscount", parameters_dict
    )

    outputs = yield context.task_all([response_quiz, response_child_discount])

    data_respond = [outputs, parameters_dict]

    respuesta = yield context.call_activity("ActivitiesSortAnswerChange", data_respond)
    return respuesta
