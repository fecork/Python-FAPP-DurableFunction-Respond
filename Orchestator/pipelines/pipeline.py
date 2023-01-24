import azure.durable_functions as df
import logging
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Dominio.Servicios.load_parameter import load_parameters
from Dominio.Servicios.sort_response import set_category, set_question
from Dominio.Servicios.sort_dates import build_dates
from Dominio.Servicios.clear_respond import format_text
from Dominio.Servicios.extract_paragraph import extract
from Dominio.Servicios import build_response
from Dominio.Servicios.validators_respond import validate_date

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
    set_data(list_gpt_responses, list_to_format_dates)
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


def join_question_category(question_dict: dict, category_dict: dict) -> dict:
    """
    This join the question and category
    Args: question_dict (dict): This is a dictionary with the questions
          category_dict (dict): This is a dictionary with the categories
    Returns:
        question_category_dict: This is a dictionary with the questions and
        categories
    """

    number_questions = category_dict["list_categories"]
    structure_paragraph_question = question_dict["question_paragraph_general"]
    structure_fare_rules = question_dict["structure_fare_rules"]
    question_category_dict = {}
    list_questions = []
    list_texts = []

    task = category_dict["task"].lower()

    number_questions = validate_category_and_questions(
        task, number_questions, question_dict)

    category_dict["list_categories"] = number_questions

    questions_lite_list_end = []
    for number in number_questions:
        text = "text_category_" + str(number)
        title = "name_category_" + str(number)
        if text in category_dict and category_dict[text] != "":
            questions = question_dict["question_category_" + str(number)][task]
            questions_lite = question_dict["qlite_category_" +
                                           str(number)][task]
            questions_lite_list = questions_lite.split("\n")

            text_category = category_dict[text]
            # TODO: logica para extraer solo cancel, change
            if number == 16:
                text_category = extract(text_category, task)
            # TODO: loogica para crear preguntas de la categoria 19
            if number == 19:
                child_list_questions = []
                passenger_child = category_dict["data_information"]["passengerChild"]
                child_list_questions = replace_data(
                    questions, passenger_child)
                list_questions.extend(child_list_questions)
                questions = ""
                questions_lite_list_end.extend(child_list_questions)

            questions_lite_list_end.extend(questions_lite_list)
            title_category = category_dict[title]
            question_and_category = title_category + "\n" + \
                text_category + "\n" + questions + 2*"\n"

            question_category_dict["question_category_" +
                                   str(number)] = question_and_category
            question_category_dict["length_category_" +
                                   str(number)] = len(question_and_category)
            list_texts.append(title_category + "\n" + text_category)
            list_questions.append(questions)

    list_questions = list(filter(None, list_questions))
    questions_lite_list_end = list(filter(None, questions_lite_list_end))
    questions_lite_list_end = [
        x for x in questions_lite_list_end if "#" not in x]

    text = "\n".join(list_texts)
    questions_text = "\n".join(list_questions)
    questions_dict = {}
    questions_dict["text"] = text + "\n" + structure_paragraph_question + questions_text + \
        "\n" * 2 + structure_fare_rules + "\n" * 2 + \
        "SOLUTION QUESTIONS 1 to {0}".format(len(questions_lite_list_end))
    questions_dict["questions_lite"] = questions_lite_list_end
    questions_dict["len_questions_lite"] = len(questions_lite_list_end)
    questions_dict["list_questions"] = list_questions
    questions_dict["len_list_questions"] = len(list_questions)
    return questions_dict


def set_data(dict_question: dict, list_question_date: list):
    """
    This functios is used to extract the dates in the questions
    Args: list_question: list of questions
    list_question_date: list of questions with dates
    """
    for key, value in dict_question.items():
        if value["category"] in list_question_date:
            if len(value["quote"]) > len(value["answer"][0]):
                list_format_dates = build_dates(value["quote"])
            else:
                list_format_dates = build_dates(value["answer"][0])
            value["value"] = list_format_dates


def set_days(dict_question: dict, list_question_week: list, list_weeks: list):
    """
    This function is used to extract the weeks in the questions
    Args: list_question: list of questions
    list_question_week: list of questions with weeks
    """
    response = []
    for key, value in dict_question.items():
        if value["category"] in list_question_week:
            text_split = value["answer"][0].split(" ")
            for text in text_split:
                if text in list_weeks:
                    response.append(text)
            value["value"] = response


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


def validate_category_and_questions(task: str, number_questions: list, question_dict: dict) -> list:
    """
    This function is used to validate the category and the questions
    Args: task: task of the question
    Returns: list of questions
    """

    list_questions = []
    list_no_questions = []
    for number in number_questions:
        if task in question_dict["question_category_" + str(number)].keys():
            list_questions.append(number)
        else:
            list_no_questions.append(number)
    logging.warning("Questions with category: " + str(list_questions))
    logging.warning("Questions without category: " + str(list_no_questions))
    return list_questions


def replace_data(question_fare_rules_nineteen: str, passenger_child: dict) -> list:
    """
    This is a function for replace data to put in text
    Args:
        str (str): This is a string with the text to convert.
        data (dict): This is a dictionary with the data to replace.
    Returns:
        str: This is a string with the text converted.

    """
    list_questions = []
    for data in passenger_child:
        age = str(data["age"])
        seat = data["seat"]
        accompanied = data["isAccompanied"]

        if seat is True:
            seat = "with a seat"
        else:
            seat = "without a seat"

        if accompanied is True:
            accompanied = "and accompanied"
        else:
            accompanied = ""
        logging.info(age)
        logging.info(seat)
        logging.info(accompanied)
        text_question = question_fare_rules_nineteen.replace("#{AGE}#", age)
        text_question = text_question.replace("#{SEAT}#", seat)
        text_question = text_question.replace("#{ACCOMPANIED}#", accompanied)
        list_questions.append(text_question)
    return list_questions
