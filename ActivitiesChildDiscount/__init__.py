# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Utilities.load_parameter import load_parameters
from Utilities.dto_respond import Respond
from Adapters import adapter_gpt


def main(parametersCancellation: dict) -> dict:

    """This is a function for extract child discount of the text
    Args:
        parametersCancellation (dict): This is a dictionary with text and task.
    Returns:
        dict: This is a dictionary with text and mean probability.
    """
    logging.warning("Executing ActivitiesChildDiscount")
    parameters = load_parameters()
    is_child = parametersCancellation["is_child"]
    text_category_nineteen = parametersCancellation["text_category_nineteen"]
    if is_child:
        question_fare_rules_nineteen = parameters["question_fare_rules_nineteen"]
        structure_fare_rules_nineteen = parameters["structure_fare_rules_nineteen"]
        quiz_text_and_question_five = (
            text_category_nineteen
            + question_fare_rules_nineteen
            + "\n" * 2
            + structure_fare_rules_nineteen
        )
        gpt_text_five = adapter_gpt.ask_openai(quiz_text_and_question_five, "list")
        list_quote = []
        list_answer = []
        gpt_text_five_text = gpt_text_five["Text"].split("\n")
        flag = False
        for text in gpt_text_five_text:
            text = text.replace("\n", "\\n")
            text = text.translate({ord(i): None for i in '",:/\\'})

            if "quote" in text.lower():
                flag = True

            if flag is True:
                list_quote.append(text.replace("Quote", "").lstrip())
            if flag is False:
                list_answer.append(text.replace("Answer", "").lstrip())

        list_quote = list(filter(None, list_quote))
        list_answer = list(filter(None, list_answer))

        respond = Respond(
            Question="5. List all the charges shown in the text",
            Answer=list_answer,
            Category=19,
            Quote=list_quote,
            FreeText=True,
            NumberQuestion=5,
            Boolean=False if len(list_answer) == 0 else True,
            MeanProbability=gpt_text_five["MeanProbability"],
            Value=None,
            Denomination=None,
        ).__dict__

        return respond
    else:
        respond = Respond(
            Question="5. List all the charges shown in the text",
            Answer=["passengerTypes is not child or infant"],
            Category=19,
            Quote="",
            FreeText=False,
            NumberQuestion=5,
            Boolean=False,
            MeanProbability=0,
            Value=None,
            Denomination=None,
        ).__dict__
        return respond
