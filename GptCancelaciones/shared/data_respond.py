import logging
import spacy
import json
import pandas as pd
import re

nlp = spacy.load("en_core_web_sm")
list_questions = [
    "The text says that the CANCELLATIONS is?",
    "According to the rules at which time you can cancel",
    "How much is the CHARGE FOR CANCEL?",
    "What is the departure date?",
    "According to the above, is the ticket refundable?"
]


def paragraph_segmentation(text):
    sentence = []
    doc = nlp(text)
    document = nlp(text)

    for sent in doc.sents:
        sentence.append(sent.text)

    start = 0
    for token in document:

        if token.is_space and token.text.count("\n") > 1:
            yield document[start: token.i]
            start = token.i
    yield document[start:]


def iterate_paragraphs(dataset):

    dict_responses = {}
    id_file = []

    for partition_id, partition_load_func in dataset.items():
        text = partition_load_func()
        text = text.replace("{", "")
        text = text.replace("}", "")
        paragraph_detected = paragraph_segmentation(text)

        list_probe = split_paragraph(paragraph_detected)
        dict_questions = text_to_json(list_probe)
        dict_responses[partition_id] = dict_questions
        id_file.append(partition_id)

    res = pd.DataFrame(dict_responses)
    return res


def individual_paragraphs(text) -> pd.DataFrame:

    paragraph_detected = paragraph_segmentation(text)

    list_probe = split_paragraph(paragraph_detected)
    logging.warning(list_probe)
    dict_questions = text_to_json(list_probe)
    return json.dumps(dict_questions)


def extrac_answer_and_quote(text):
    text.replace("\n", "")
    return text


def split_paragraph(paragraph_detected):
    list_format_text = []
    for paragraph in paragraph_detected:
        content = paragraph.text
        if "number_question" in content:
            list_format_text.append(content)

    return list_format_text


def text_to_json(list_probe):
    dict_questions = {}
    list_questions = [
        "The text says that the CANCELLATIONS is?",
        "According to the rules at which time you can cancel",
        "How much is the CHARGE FOR CANCEL?",
        "What is the departure date?",
        "According to the above, is the ticket refundable?"
    ]

    for paragraphs in list_probe:
        text = paragraphs.split("\n")
        dict_response = {"answer": "",
                         "quote": "",
                         "boolean": ""
                         }

        for line in text:

            value = clear_value_json(line, "answer")
            if value is not None:
                dict_response["answer"] = value

            value = clear_value_json(line, "number_question")
            if value is not None:
                key_number = value
                dict_response["question"] = list_questions[int(value)-1]

            value = clear_value_json(line, "quote")
            if value is not None:
                dict_response["quote"] = value

            value = clear_value_json(line, "boolean")
            if value is not None:
                value = validate_boolean(value)
                dict_response["boolean"] = value

        dict_questions["question_" + str(key_number)] = dict_response

    dict_questions = validate_charge_number(dict_questions)
    validate_structure_json(dict_questions)
    return dict_questions


def clear_value_json(line, key):
    key_json = key.translate({ord(i): None for i in ":"})

    if "quote" in line:
        line = line.replace("\n", " ")

    if key_json in line:
        res = line.replace(key, "")
        res = res.translate({ord(i): None for i in '",:'})
        res = res.strip()
        return res


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
    dict_questions["question_3"]["denomination"] = denomination
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
