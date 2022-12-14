import logging


def overall_average(respuesta: list) -> float:
    
    """
    This function is for calculate the overall average of the respond of the GPT.
    Args:
        respuesta (dict): This is a dictionary with the respond of the GPT.
    Returns:
        float: This is a float with the overall average of the respond of the GPT.
    """
    
    logging.info("Executing overall_average")
    list_true_answers = []
    try:
        for value in respuesta:
            if value["meanProbability"] != 0:
                list_true_answers.append(value["meanProbability"])
        average = sum(list_true_answers) / len(list_true_answers)

        return average
    except Exception as e:
        return 0
