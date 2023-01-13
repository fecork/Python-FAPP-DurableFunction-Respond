from Dominio.Servicios.load_parameter import load_parameters
from Dominio.Servicios.sort_response import set_category

import azure.durable_functions as df
import logging
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)


parameters = load_parameters()


def pipeline(context: df.DurableOrchestrationContext, parameters_dict: dict):
    """
    This is the main pipeline function. Execute in parallel the activities
    Args:
        context (DurableOrchestrationContext):
        The context object for durable function
        parameters_dict (dict): This is a dictionary with the parameters
    Returns:
        parameters_dict: This is a dictionary with the respond of the GPT
    """

    question_fare_rules = parameters["question_fare_rules_fuel_surcharge"]
    structure_fare_rules = parameters["structure_fare_rules"]
    structure_questions = parameters["structure_fare_rules_fuel_surcharge"]

    parameters_dict["task"] = "FUELSURCHARGE"

    try:
        gpt_paragraph_text = yield context.call_activity(
            "ActivitieExtractParagraphIndex", parameters_dict
        )
    except Exception as e:
        logging.error("Error in ActivitieExtractParagraphIndex")
        logging.error(e)

    quiz_text_and_question = (
        'SURCHARGES'
        + "\n"*2
        + gpt_paragraph_text['FUELSURCHARGE']
        + "\n" * 2
        + question_fare_rules
        + "\n" * 2
        + structure_fare_rules
        + "\n" * 2
        + structure_questions
    )
    logging.warning(quiz_text_and_question)

    parameters_quiz = {
        "quiz_text_and_question": quiz_text_and_question,
        "number_questions": parameters["number_question_fuel_surcharge"],
        "list_questions": parameters[
            "list_question_fare_rules_fuel_surcharge"],
        "list_question_charge": parameters[
            "list_question_charge_fuel_surcharge"],
        "task": "change",
    }

    response_quiz = context.call_activity(
        "ActivitiesExecuteQuiz", parameters_quiz)

    outputs = yield context.task_all([response_quiz])
    question_list = outputs[0]
    set_category(question_list, [12, 12])
    list_free_text = [{
        "category": 12,
        "text": parameters_dict["text_category_12"]
    }]
    model_respond = [question_list["question_1"], question_list["question_2"]]
    data_respond = {
        "outputs": outputs,
        "parameters_dict": parameters_dict,
        "list_free_text": list_free_text,
        "model_respond": model_respond
    }
    respuesta = yield context.call_activity(
        "ActivitiesSortAnswer", data_respond)

    return respuesta
