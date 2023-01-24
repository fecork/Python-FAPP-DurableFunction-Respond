import os 
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Dominio.Servicios.sort_response import replace_information_children
from Dominio.Servicios.extract_paragraph import extract
from Dominio.Servicios.validators_respond import validate_category_and_questions


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
                child_list_questions = replace_information_children(
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
