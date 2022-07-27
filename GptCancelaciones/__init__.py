import logging
import os
import sys

import azure.functions as func

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from shared import pipeline

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Recibe el objeto Json

    Args:

    `{
        "string":"CANCELLATIONS ANY"
    }`

    Returns:

    las respuestas del modelo **GPT**

    `{
        "question_1": {
                "number_question": "1",
                "answer": "B",
                "quote": "TICKET IS NONREFUNDABLE"
        },
    }`
    """
    logging.info("Python HTTP trigger function processed a request.")

    parameter_string = req.params.get("string")
    if not parameter_string:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            parameter_string = req_body.get("string")

    if parameter_string:

        gpt_response = pipeline.execute(parameter_string)
        logging.info(gpt_response)

        return func.HttpResponse(f"{gpt_response}")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a parameter_string in the query string or in the request body for a gpt response.",
            status_code=200,
        )
