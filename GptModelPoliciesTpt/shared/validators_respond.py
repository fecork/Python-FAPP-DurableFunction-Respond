import re
import logging

list_questions = [
    "The text says that the CANCELLATIONS is?",
    "According to the rules at which time you can cancel",
    "How much is the CHARGE FOR CANCEL?",
    "What is the departure date?",
    "According to the above, is the ticket refundable?"
]

def validate_boolean(text):
    text = str(text).lower()
    if "true" in text:
        return True
    if "false" in text:
        return False
    return None


def validate_charge_number(dict_questions):

    text = dict_questions["question_3"]["answer"]
    number = [float(s) for s in re.findall(r'-?\d+\.?\d*', text)]
    denomination = ''.join([i for i in text if not i.isdigit()])
    dict_questions["question_3"]["value"] = number[0]
    dict_questions["question_3"]["denomination"] = denomination[:3]
    return dict_questions


def validate_structure_json(dict_questions):
    number_questions = 5
    list_numbers = range(number_questions)

    for number in list_numbers:
        number = number + 1
        if "question_" + str(number) not in dict_questions:
            dict_questions["question_" + str(number)] = {"answer": "",
                                                         "quote": "",
                                                         "boolean": "",
                                                         "question": list_questions[int(number)],
                                                         }
    return dict_questions


def validate_refund(dict_questions):
    charge = dict_questions["question_3"]["value"]
    time = dict_questions["question_2"]["answer"]

    ischarge = False
    istime = False

    logging.info('99999')
    logging.info(ischarge)
    logging.info(istime)
    logging.info('99999')


    if type(charge) is float or type(charge) is int:
        ischarge= True
    if not "None" in time:
        ischarge = True

    if ischarge and istime:
        dict_questions["question_5"]["answer"] = 'refundable'
        dict_questions["question_5"]["boolean"] = True
    else:
        dict_questions["question_5"]["answer"] = 'nonrefundable'
        dict_questions["question_5"]["boolean"] = False
    return dict_questions
