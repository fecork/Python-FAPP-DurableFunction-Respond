import logging
import spacy
import json
import pandas as pd

nlp = spacy.load("en_core_web_sm")


def paragraph_segmentation(text):
    sentence = []
    doc = nlp(text)
    document = nlp(text)

    for sent in doc.sents:
        sentence.append(sent.text)

    start = 0
    for token in document:

        if token.is_space and token.text.count("\n") > 1:
            yield document[start : token.i]
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
    dict_questions = text_to_json(list_probe)
    # dataframe = pd.DataFrame(dict_questions)
    # result = dataframe.to_json(orient="split")
    # logging.info(dict_questions)
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

    for paragraphs in list_probe:
        text = paragraphs.split("\n")
        dict_response = {}

        for line in text:

            value = clear_value_json(line, "answer")
            if value is not None:
                dict_response["answer"] = value

            value = clear_value_json(line, "number_question")
            if value is not None:
                dict_response["number_question"] = value

            value = clear_value_json(line, "quote")
            if value is not None:
                dict_response["quote"] = value
        key_number = dict_response["number_question"].strip()
        dict_questions["question_" + key_number] = dict_response

    return dict_questions


def clear_value_json(line, key):
    key_json = key.translate({ord(i): None for i in ":"})

    if "quote" in line:
        line = line.replace("\n", " ")

    if key_json in line:
        res = line.replace(key, "")
        res = res.translate({ord(i): None for i in '".,:'})
        res = res.strip()
        return res
