from Utilities import dto_respond


def edit_response(
    question_i=None,
    answer_i=None,
    category_i=None,
    quote_i=None,
    freeText_i=None,
    numberQuestion_i=None,
    boolean_i=None,
    meanProbability_i=None,
    value_i=None,
    denomination_i=None,
) -> dict:
    """
    This function edit the response
    Args:
        inputs
    Returns:
        dict: This is a dictionary with text and mean probability.
    """

    respond = dto_respond.Respond(
        question="",
        answer="",
        category=0,
        quote="",
        freeText=False,
        numberQuestion=0,
        boolean=False,
        meanProbability=0,
        value=None,
        denomination=None,
    ).__dict__

    if question_i is not None:
        respond["question"] = question_i
    if answer_i is not None:
        respond["answer"] = answer_i
    if category_i is not None:
        respond["category"] = category_i
    if quote_i is not None:
        respond["quote"] = quote_i
    if freeText_i is not None:
        respond["freeText"] = freeText_i
    if numberQuestion_i is not None:
        respond["numberQuestion"] = numberQuestion_i
    if boolean_i is not None:
        respond["boolean"] = boolean_i
    if meanProbability_i is not None:
        respond["meanProbability"] = meanProbability_i
    if value_i is not None:
        respond["value"] = value_i
    if denomination_i is not None:
        respond["denomination"] = denomination_i

    return respond
