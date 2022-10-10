def validate_error(respond: object) -> str:
    if "gpt_paragraph_text" in respond.output:
        cause = "It was dont found information about Cancellation or Change in the freeText."
    if "maximum context length" in respond.output:
        cause = "The length of the text is too long for the GPT-3 model."
    if "APIConnectionError" in respond.output:
        cause = "There is not more credits for the GPT-3 model."
    else:
        cause = "unknown"
    return cause
