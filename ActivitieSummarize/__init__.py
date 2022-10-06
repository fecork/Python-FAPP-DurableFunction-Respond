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

# from Utilities.load_parameter import load_parameters
from Utilities.clear_respond import format_text
from transformers import pipeline

# parameters = load_parameters()


def main(article: str) -> str:
    """
    summarize the text when the text is too long. max length is 1800 characters
    Args: article: String with the text.
    returns: summary of the text
    """

    if len(article) > 1800:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        article = format_text(article)
        # split text in 1800 characters
        len_char = 1800
        list_text = [
            article[i : i + len_char] for i in range(0, len(article), len_char)
        ]
        list_result = []
        print(len(list_text))
        for text in list_text[: int(len(list_text) / 2)]:
            summary = summarizer(text, max_length=100, min_length=50)
            list_result.append(summary[0]["summary_text"])

        # join all summaries
        result = "".join(list_result)
        print(result)
        print(len(result))
    else:
        result = article
    return result
