import azure.durable_functions as df
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Dominio.Servicios.load_parameter import load_parameters
from Dominio.Servicios.sort_dates import build_dates

parameters = load_parameters()


def pipeline(context: df.DurableOrchestrationContext, parameters_dict: dict):
    """
    This is the main pipeline function. Execute in parallel the activities
    Args:
        context (DurableOrchestrationContext): The context object
        for durable function
        parameters_dict (dict): This is a dictionary with the parameters
    Returns:
        parameters_dict: This is a dictionary with the respond of the GPT
    """

    parameters_quiz_group_one = build_text(parameters_dict, "group_1")
    parameters_quiz_group_two = build_text(parameters_dict, "group_2")
    parameters_quiz_group_three = build_text(parameters_dict, "group_3")
    response_quiz_group_one = context.call_activity(
        "ActivitiesExecuteQuiz", parameters_quiz_group_one
    )

    response_quiz_group_two = context.call_activity(
        "ActivitiesExecuteQuiz", parameters_quiz_group_two
    )

    response_quiz_group_three = context.call_activity(
        "ActivitiesExecuteQuiz", parameters_quiz_group_three
    )

    outputs = yield context.task_all(
        [response_quiz_group_one,
         response_quiz_group_two,
         response_quiz_group_three]
    )
    question_list_group_1 = outputs[0]
    question_list_group_2 = outputs[1]
    question_list_group_3 = outputs[2]

    text_category_two = parameters_dict["text_category_two"]
    text_category_three = parameters_dict["text_category_three"]
    text_category_six = parameters_dict["text_category_six"]
    text_category_seven = parameters_dict["text_category_seven"]
    text_category_eight = parameters_dict["text_category_eight"]
    text_category_eleven = parameters_dict["text_category_eleven"]
    text_category_twelve = parameters_dict["text_category_twelve"]

    question_list_group_1["question_1"]["category"] = 6
    question_list_group_1["question_2"]["category"] = 7
    question_list_group_2["question_1"]["category"] = 8
    question_list_group_2["question_2"]["category"] = 11
    question_list_group_3["question_1"]["category"] = 2
    question_list_group_3["question_2"]["category"] = 3

    question_list_group_1["question_1"]["numberQuestion"] = 1
    question_list_group_1["question_2"]["numberQuestion"] = 2
    question_list_group_2["question_1"]["numberQuestion"] = 3
    question_list_group_2["question_2"]["numberQuestion"] = 4
    question_list_group_3["question_1"]["numberQuestion"] = 5
    question_list_group_3["question_2"]["numberQuestion"] = 6

    list_question_date_group_2 = parameters_quiz_group_two[
        "list_question_date_two"]
    list_question_date_group_3 = parameters_quiz_group_three[
        "list_question_date_three"]
    list_question_week_group_3 = parameters_quiz_group_three[
        "list_question_week_three"]
    list_weeks = parameters["weeks"]

    set_data(question_list_group_2, list_question_date_group_2)
    set_data(question_list_group_3, list_question_date_group_3)
    set_weeks(question_list_group_3, list_question_week_group_3, list_weeks)

    list_free_text = [
        {"category": 2, "text": text_category_two},
        {"category": 3, "text": text_category_three},
        {"category": 6, "text": text_category_six},
        {"category": 7, "text": text_category_seven},
        {"category": 8, "text": text_category_eight},
        {"category": 11, "text": text_category_eleven},
        {"category": 12, "text": text_category_twelve},
    ]

    model_respond = [question_list_group_1["question_1"],
                     question_list_group_1["question_2"],
                     question_list_group_2["question_1"],
                     question_list_group_2["question_2"],
                     question_list_group_3["question_1"],
                     question_list_group_3["question_2"]]
    data_respond = {
        "outputs": outputs,
        "parameters_dict": parameters_dict,
        "list_free_text": list_free_text,
        "model_respond": model_respond
    }
    respuesta = yield context.call_activity(
        "ActivitiesSortAnswer", data_respond)
    return respuesta


def build_text(parameters_dict: dict, tag: str) -> dict:

    if tag == "group_1":
        question_fare_rules = parameters[
            "question_fare_rules_change_manual_group_one"]
        structure_fare_rules = parameters["structure_fare_rules"]
        structure_questions = parameters[
            "structure_fare_rules_change_manual_group_one"]
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
            + "\n"
            + text_category_seven
            + "\n"
        )

        quiz_text_and_question = (
            gpt_paragraph_text
            + "\n" * 2
            + question_fare_rules
            + "\n" * 2
            + structure_fare_rules
            + "\n" * 2
            + structure_questions
            + "\n"
        )

        parameters_quiz = {
            "quiz_text_and_question": quiz_text_and_question,
            "number_questions": parameters[
                "number_question_change_manual_group_one"],
            "list_questions": parameters[
                "list_question_fare_rules_change_manual_group_one"
            ],
            "list_question_charge": parameters[
                "list_question_charge_change_manual_group_one"
            ],
            "task": "manual_group_one",
        }

    if tag == "group_2":
        question_fare_rules = parameters[
            "question_fare_rules_change_manual_group_two"]
        structure_fare_rules = parameters["structure_fare_rules"]
        structure_questions = parameters[
            "structure_fare_rules_change_manual_group_two"]
        text_category_eight = parameters_dict["text_category_eight"]
        text_category_eleven = parameters_dict["text_category_eleven"]
        parameters_dict["question_paragraph"] = parameters[
            "question_paragraph_change_manual_group_one"
        ]

        gpt_paragraph_text = (
            "STOPOVERS "
            + "\n"
            + text_category_eight
            + "\n"
            + "BLACKOUT DATES "
            + "\n"
            + text_category_eleven
            + "\n"
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
            "number_questions": parameters[
                "number_question_change_manual_group_two"],
            "list_questions": parameters[
                "list_question_fare_rules_change_manual_group_two"
            ],
            "list_question_charge": parameters[
                "list_question_charge_change_manual_group_two"
            ],
            "list_question_date_two": parameters[
                "list_question_date_change_manual_group_two"
            ],
            "task": "manual_group_two",
        }

    if tag == "group_3":
        question_fare_rules = parameters[
            "question_fare_rules_change_manual_group_three"
        ]
        structure_fare_rules = parameters["structure_fare_rules"]
        structure_questions = parameters[
            "structure_fare_rules_change_manual_group_three"
        ]
        text_category_two = parameters_dict["text_category_two"]
        text_category_three = parameters_dict["text_category_three"]
        parameters_dict["question_paragraph"] = parameters[
            "question_paragraph_change_manual_group_one"
        ]

        gpt_paragraph_text = (
            "DAY/TIMES "
            + "\n"
            + text_category_two
            + "\n"
            + "SEASONALITY "
            + "\n"
            + text_category_three
            + "\n"
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
            "number_questions": parameters[
                "number_question_change_manual_group_three"],
            "list_questions": parameters[
                "list_question_fare_rules_change_manual_group_three"
            ],
            "list_question_charge": parameters[
                "list_question_charge_change_manual_group_three"
            ],
            "list_question_date_three": parameters[
                "list_question_date_change_manual_group_three"
            ],
            "list_question_week_three": parameters[
                "list_question_week_change_manual_group_three"
            ],
            "task": "manual_group_three",
        }

    return parameters_quiz


def set_data(dict_question: dict, list_question_date: list):
    """
    This functios is used to extract the dates in the questions
    Args: list_question: list of questions
    list_question_date: list of questions with dates
    """
    for key, value in dict_question.items():
        if key in list_question_date:
            select_text = "quote" if len(
                value["quote"]) > len(value["answer"]) else "answer"
            list_format_dates = build_dates(value[select_text])
            value["value"] = list_format_dates


def set_weeks(dict_question: dict, list_question_week: list, list_weeks: list):
    """
    This function is used to extract the weeks in the questions
    Args: list_question: list of questions
    list_question_week: list of questions with weeks
    """
    response = []
    for key, value in dict_question.items():
        if key in list_question_week:
            text_split = value["answer"][0].split(" ")
            for text in text_split:
                if text in list_weeks:
                    response.append(text)
            value["value"] = response
