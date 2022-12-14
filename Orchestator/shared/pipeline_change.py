from Utilities.load_parameter import load_parameters
from Utilities.validators_respond import validate_date
from Utilities import build_response

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
        context (DurableOrchestrationContext): The context object for durable function
        parameters_dict (dict): This is a dictionary with the parameters
    Returns:
        parameters_dict: This is a dictionary with the respond of the GPT
    """
    task = parameters_dict["task"].lower()
    question_fare_rules = parameters["question_fare_rules_{0}".format(task)]
    structure_fare_rules = parameters["structure_fare_rules"]
    structure_questions = parameters["structure_fare_rules_{0}".format(task)]

    parameters_dict["question_paragraph"] = parameters["question_paragraph_{0}".format(task)]

    parameters_dict["paragraph"] = parameters_dict["task"]

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
        "number_questions": parameters["number_question_{0}".format(task)],
        "list_questions": parameters["list_question_fare_rules_{0}".format(task)],
        "list_question_charge": parameters["list_question_charge_{0}".format(task)],
        "task": "{0}".format(task),
    }

    response_quiz = context.call_activity("ActivitiesExecuteQuiz", parameters_quiz)
    
    response_child_discount = context.call_activity(
        "ActivitiesChildDiscount", parameters_dict
    )

    outputs = yield context.task_all([response_quiz, response_child_discount])
    question_list = outputs[0]
    percent_child = outputs[1]
    
    text_category_sixteen = parameters_dict["text_category_six"]
    text_category_nineteen = parameters_dict["text_category_nineteen"]
    is_child = parameters_dict["is_child"]
    
    set_category(question_list, 16) 
    departure_date = parameters_dict["data_information"]["departureDate"]
    departure_date_response = build_date_response(departure_date, task)
    
    if is_child:
        list_free_text = [
            {"category": 16, "text": text_category_sixteen},
            {"category": 19, "text": text_category_nineteen}]
    else:
        list_free_text = [{"category": 16, "text": text_category_sixteen}]
  
    model_respond = set_model_respond(
        question_list, percent_child, departure_date_response, task)
    
    data_respond = {
        "outputs": outputs, 
        "parameters_dict": parameters_dict, 
        "list_free_text": list_free_text,
        "model_respond": model_respond
        }

    respuesta = yield context.call_activity("ActivitiesSortAnswer", data_respond)
    return respuesta


def build_date_response(departure_date: str, task: str):
    
    date_formated = validate_date(departure_date)

    respond = build_response.edit_response(
        question_i="Departure date?",
        answer_i=date_formated,
        quote_i=departure_date,
        numberQuestion_i=6 if task == "change" else 4,
        boolean_i=True,
    )
    return respond


def set_category(question_list: dict, category: int):
    for key, value in question_list.items():
        value["category"] = category


def check_booleans(question_dic: dict) -> dict:
    # boolean_1 = question_dic["question_1"]["boolean"]
    boolean_2 = question_dic["question_2"]["boolean"]
    # is_anytime = True if "ANY" in question_dic["question_1"]["quote"][0].upper()
    is_anytime = False
    text_to_validate = question_dic["question_1"]["quote"][0].upper()
    if 'ANY' in text_to_validate:
        is_anytime = True
    if 'BEFORE' in text_to_validate:
        is_anytime = True

    validate = boolean_2 and is_anytime
    if validate:
        logging.warning("Refundable")

    respond = build_response.edit_response(
        question_i="Is refundable?",
        answer_i="Refundable" if validate else "Not Refundable",
        category_i=16,
        numberQuestion_i=6,
        boolean_i=validate,)
    return respond


def set_model_respond(question_list, percent_child, departure_date_response, task):
    if 'change' in task:
        model_respond = [
            question_list["question_1"],
            question_list["question_2"],
            question_list["question_3"],
            question_list["question_4"],
            percent_child,
            departure_date_response
        ]
    if 'cancel' in task:
        is_refundable = check_booleans(question_list)
        model_respond = [
            question_list["question_1"],
            question_list["question_2"],
            question_list["question_3"],
            departure_date_response,
            percent_child,
            is_refundable
        ]
    return model_respond
