import azure.durable_functions as df
import logging
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Dominio.Servicios.load_parameter import load_parameters
from Dominio.Servicios.sort_response import set_category
from Dominio.Servicios.sort_dates import set_days, set_date
from Dominio.Servicios import build_response
from Dominio.Servicios.validators_respond import validate_date
from Dominio.Servicios.join_text import join_question_category

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
    # TODO
    # formato de Charges para dinero
    task = parameters_dict["task"]
    question_category_dict = join_question_category(
        parameters, parameters_dict)
    logging.info("111")
    quiz_text_and_question = question_category_dict["text"]
    logging.warning(quiz_text_and_question)
    logging.info("222")
    list_categories = parameters_dict["list_categories"]
    logging.info("333")

    list_question = question_category_dict["questions_lite"]

    logging.info("444")
    number_questions = len(list_question)
    logging.info(number_questions)
    logging.warning(list_question)
    logging.info("555")

    #LOG
    logging.info("list_question: " + str(list_question))
    logging.info("666")
    logging.error(">>>>>>>>>>>>>>>>>>")
    parameters_quiz = {
        "quiz_text_and_question": quiz_text_and_question,
        "number_questions": number_questions,
        "list_questions": list_question,
        #TODO
        # "task": "flex",
        "task": parameters_dict["task"],
        "list_categories": parameters_dict["list_categories"]
    }

    response_quiz = context.call_activity(
        "ActivitiesExecuteQuiz", parameters_quiz)

    outputs = yield context.task_all([response_quiz])
    list_gpt_responses = outputs[0]

    if len(list_categories) < len(list_gpt_responses):
        logging.warning('len(list_categories) < len (list_gpt_responses)')
        list_categories = list_categories * len(list_gpt_responses)

    set_category(list_gpt_responses, list_categories)
    list_to_format_dates = parameters["category_to_format_date"]
    list_to_days = parameters["category_to_days"]

    # TODO:
    # agregar logica refundable
    # formatear charge
    # extraer del texto solo cancel, change
    # logica is refundable?
    # que solo las categorias 19 tengan el numero 19

    list_free_text = []
    list_categories_unique = list(set(list_categories))
    for category in list_categories_unique:
        dict_category = {"category": category,
                         "text": parameters_dict["text_category_" + str(category)]}
        list_free_text.append(dict_category)

    list_weeks = parameters["weeks"]
    set_date(list_gpt_responses, list_to_format_dates)
    set_days(list_gpt_responses, list_to_days, list_weeks)

    model_respond = []
    numbers = list(range(1, number_questions + 1))
    for number in numbers:
        model_respond.append(list_gpt_responses["question_" + str(number)])

    if task.upper() == "CHANGE":
        departure_date = parameters_dict["data_information"]["departureDate"]
        departure_date_response = build_date_response(
            departure_date, len(model_respond)+1)
        model_respond.append(departure_date_response)

    data_respond = {
        "outputs": outputs,
        "parameters_dict": parameters_dict,
        "list_free_text": list_free_text,
        "model_respond": model_respond
    }
    respuesta = yield context.call_activity(
        "ActivitiesSortAnswer", data_respond)

    return respuesta


def build_date_response(departure_date: str, number_question: int):
    date_formated = validate_date(departure_date)

    respond = build_response.edit_response(
        question_input="Departure date?",
        answer_input=date_formated,
        quote_input=departure_date,
        number_question_input=number_question,
        boolean_input=True,
    )
    return respond