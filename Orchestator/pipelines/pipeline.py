from Dominio.Servicios.load_parameter import load_parameters
from Dominio.Servicios.sort_response import set_category, set_question
from Dominio.Servicios.sort_dates import build_dates
from Dominio.Servicios.clear_respond import format_text
from Dominio.Servicios.extract_paragraph import extract


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
 
    question_category_dict = join_question_category(parameters, parameters_dict)
    logging.info("111")    
    quiz_text_and_question = question_category_dict["text"]
    logging.warning(quiz_text_and_question)
    logging.info("222")
    list_categories = parameters_dict["list_categories"]
    logging.info("333")
    #TODO: list question no trae todas las preguntas.
    list_question = count_questions(
        parameters, list_categories, parameters_dict)
    logging.info("444")
    number_questions = len(list_question)
    logging.info("555")
    # list_question = ', '.join(list_question)
    
    #LOG
    logging.info("list_question: " + str(list_question))
    logging.info("666")
    logging.error(">>>>>>>>>>>>>>>>>>")
    parameters_quiz = {
        "quiz_text_and_question": quiz_text_and_question,
        "number_questions": number_questions,
        "list_questions": list_question,
        "task": "flex",
        "list_categories": parameters_dict["list_categories"]
    }

    response_quiz = context.call_activity(
        "ActivitiesExecuteQuiz", parameters_quiz)

    outputs = yield context.task_all([response_quiz])
    list_gpt_responses = outputs[0]

    #TODO:
    logging.error('DDDDDDDDDDDDDD')
    logging.warning('len(list_gpt_responses): ' + str(len(list_gpt_responses)))
    logging.warning(len(list_categories))
    if len(list_categories) < len (list_gpt_responses):
        logging.warning('len(list_categories) < len (list_gpt_responses)')
        # resize list categories to list gpt responses, add repeat the list_categories[0]
        list_categories = list_categories * len(list_gpt_responses)

    set_category(list_gpt_responses, list_categories)
    list_to_format_dates = parameters["category_to_format_date"]
    list_to_days = parameters["category_to_days"]

    # TODO: 
    # formatear charge
    # cat 16 y 19
    # extraer del texto solo cancel, change
    # logica is refundable?

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
        
    logging.warning(category_dict["list_categories"])
    number_questions = category_dict["list_categories"]
    logging.error(number_questions)
    structure_paragraph_question = question_dict["question_paragraph_general"]
    structure_fare_rules = question_dict["structure_fare_rules"]
    question_category_dict = {}
    list_questions = []
    list_texts = []
    questions_lite_list = []

    #-------------------
    task = category_dict["task"].lower()
            
    number_questions = validate_category_and_questions(
        task, number_questions, question_dict)

    #-------------------

    logging.error('<<<<<<<<<<<<<<<<<<<<')
    logging.warning(number_questions)
    
    
    category_dict["list_categories"] = number_questions
    #LOG:
    logging.error('oioioioioioioi')
    logging.warning(task)
    for number in number_questions:
        text = "text_category_" + str(number)
        # text = extract(text, task)
        title = "name_category_" + str(number)
        if text in category_dict and category_dict[text] != "":
            questions = question_dict["question_category_" + str(number)][task]
            questions_lite = question_dict["qlite_category_" + str(number)][task]
            text_category = category_dict[text]
            text_category = extract(text_category, task)
            title_category = category_dict[title]
            question_and_category = title_category + "\n" + \
                text_category + "\n" + questions + 2*"\n"
            logging.error('================')
            logging.warning(question_and_category)
            logging.error('================')
            question_category_dict["question_category_" +
                                   str(number)] = question_and_category
            question_category_dict["length_category_" +
                                   str(number)] = len(question_and_category)
            list_texts.append(title_category + "\n" + text_category)
            list_questions.append(questions)
            questions_lite_list.append(questions_lite)
    #LOG
    logging.error(questions_lite_list)
    questions_lite_list = questions_lite_list[0].split("\n")
    
    logging.error('BBBBBBBBBBBBBBBB')
    text = "\n".join(list_texts)
    logging.error('CCCCCCCCCCCCCCCC')
    questions_text = "\n".join(list_questions)
    logging.error('DDDDDDDDDDDDDDDD')
    prueba = {}
    logging.error(type(text))
    logging.error(type(questions_text))
    logging.error(type(structure_paragraph_question))
    logging.error(type(structure_fare_rules))
    prueba["text"] = text + "\n" + structure_paragraph_question + questions_text + \
        "\n" * 2 + structure_fare_rules + "\n" * 2 + \
        "SOLUTION QUESTIONS 1 to {0}".format(len(questions_lite_list))
    logging.warning('AAAAAAAAAAAAAAAA')
    logging.error(list_questions)
    return prueba


def count_questions(parameters: dict, list_categories: list, parameters_dict: dict):
    list_questions = []
    task = parameters_dict["task"].lower()
    key = "qlite_category_"
    for categorie in list_categories:
        text = parameters[key + str(categorie)][task]
        #TODO:
        # list_questions.append(text)
        list_split = text.split('\n')
        logging.error('.,.,.,.,.,.,.,')
        logging.warning(list_questions)
        list_split = list(filter(None, list_split))
        list_questions.extend(list_split)
        logging.error('.,.,.,.,.,.,.,')
        logging.warning(list_questions)
    return list_questions


def set_data(dict_question: dict, list_question_date: list):
    """
    This functios is used to extract the dates in the questions
    Args: list_question: list of questions
    list_question_date: list of questions with dates
    """
    for key, value in dict_question.items():
        if value["category"] in list_question_date:
            logging.error(value["category"])
            logging.error('^^^^^^^^^^')
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
            logging.warning(value["category"])
            logging.warning('^^^^^^^^^^')
            text_split = value["answer"][0].split(" ")
            for text in text_split:
                if text in list_weeks:
                    response.append(text)
            value["value"] = response


# def extract_paragraph(parameters: dict) -> dict:
#     """
#     Split the text in a list of sentences.
#     Args:content: String with the text.
#     Returns: List of sentences.
#     """
#     logging.warning("Executing ActivitiesExtractParagraph")

#     # task = parameters["task"]
#     task = "FLEX"
#     logging.warning(task)
#     # if task == "CHANGE" or task == "CANCELLATION":
#     #     response = task_change(parameters)
#     if task == "FUELSURCHARGE" or task == "FLEX":
#         select_text = text_segementation(
#             "text_category_12", "FUEL", parameters)
#         if len(select_text) > 0:
#             response = select_text
#         elif len(parameters["text_category_12"]) > 2000:
#             response = parameters["text_category_12"][:2000]
#         else:
#             response = parameters["text_category_12"]
#     if task == "DEPARTUREDATE":
#         select_text = text_segementation(
#             "text_category_12", "DEPARTURE", parameters)
#         if len(select_text) > 0:
#             response = select_text
#         else:
#             response = parameters["text_category_12"]

#     return response

def extract_paragraph(text: str) -> str:
    logging.warning(len(text))
    logging.error('zzzzzzzzzzzz')
    if len(text) > 1500:
        return text[:1500]
    else:
        return text
    

def text_segementation(
        category: str,
        word_to_search: str,
        parameters: dict) -> str:
    """
    Split the text in a list of sentences.
    Args:content: String
    """
    logging.warning("Executing Fuel Surcharge Extraction")
    content = format_text(parameters[category], False)
    positions = [i for i, word in enumerate(
        content.split()) if word == word_to_search]
    long_text = 20
    list_paragraphs = []
    for position in positions:
        pre = content.split()[position: position - long_text:position]
        words = content.split()[position: position + long_text]
        paragraph = " ".join(pre + words)
        list_paragraphs.append(paragraph)

    full_text = " ".join(list_paragraphs)
    return full_text


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
