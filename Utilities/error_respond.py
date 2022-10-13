import logging


def validate_error(respond: object) -> str:

    logging.error(f"Orchestration failed:")
    logging.warning(f"Orchestration status: {respond.output}")
    if "gpt_paragraph_text" in respond.output:
        cause = "It was dont found information about Cancellation or Change in the freeText."
    if "maximum context length" in respond.output:
        cause = "The length of the text is too long for the GPT-3 model."
    if "APIConnectionError" in respond.output:
        cause = "There is not more credits for the GPT-3 model."
    if "ActivitiesSortAnswer" in respond.output:
        cause = "GPT dont answer the question, check the tokens."
    if "Functions.ActivitieExtractParagraphIndex" in respond.output:
        cause = "The FreeText is empty."
    if "KeyError" in respond.output:
        cause = "The key is not in the dictionary. The JSON input is not correct."

    else:
        cause = "unknown"
    return cause
