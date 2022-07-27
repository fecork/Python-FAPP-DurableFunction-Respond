import logging
import os
import sys

import azure.functions as func

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from shared import pipeline

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    parameter_rules = get_parameter(req,"rules")
    parameter_information = get_parameter(req,"information")

    if parameter_rules:

        gpt_response = pipeline.execute(parameter_rules,parameter_information)
        logging.info(gpt_response)

        return func.HttpResponse(f"{gpt_response}")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a parameter_string in the query string or in the request body for a gpt response.",
            status_code=200,
        )

def get_parameter(req, parameter):

    parameter_string = req.params.get(parameter)
    if not parameter_string:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            parameter_string = req_body.get(parameter)

    return parameter_string
