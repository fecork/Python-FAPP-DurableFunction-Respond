# This function an HTTP starter function for Durable Functions.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable activity function (default name is "Hello")
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt


from Utilities.load_parameter import load_parameters
from Utilities.error_respond import validate_error
from Adapters.adapter_auth import get_jwk

import json
import azure.functions as func
import azure.durable_functions as df
import os
import sys
import logging


from authlib.jose import jwt

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)


parameters = load_parameters()


async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:

    try:

        logging.info("Python HTTP trigger function processed a request.")

        correct_req = validate_req(req)
        jwt = req.headers.get("Authorization")
        is_token = validate_token(jwt)
        # is_token = True
        if is_token == False:
            return func.HttpResponse(
                status_code=401, mimetype="application/json"
            )

        if correct_req:
            parameter_task = get_parameter(req, "task")
            parameter_information = get_parameter(req, "information")
            parameter_penalty_text = get_parameter(req, "penaltyText")
            dict_parameters = {
                "task": parameter_task,
                "information": parameter_information,
                "penaltyText": parameter_penalty_text,
            }
            fare_basis = str(parameter_penalty_text[0]["fareBasis"])
            logging.warning("Starter")
            logging.warning(fare_basis)
            client = df.DurableOrchestrationClient(starter)

            instance_id = await client.start_new(
                "Orchestator", None, dict_parameters
            )

            logging.info(f"Started orchestration with ID = '{instance_id}'.")

            respond = await client.get_status(instance_id)

            while respond.runtime_status.value != "Completed":
                respond = await client.get_status(instance_id)
                if respond.runtime_status.value == "Failed":
                    cause = validate_error(respond)

                    return func.HttpResponse(
                        json.dumps({"cause": cause, "error": respond.output}),
                        mimetype="application/json",
                        status_code=500,
                    )
            logging.warning(
                f"Orchestration status: {respond.runtime_status.value}"
            )
            logging.warning("fareBasis: " + str(fare_basis))
            return func.HttpResponse(
                json.dumps(respond.output),
                mimetype="application/json",
                status_code=200,
            )
        else:
            return func.HttpResponse(
                json.dumps(
                    {
                        "cause": (
                            "There is a Error in the Json, review that task"
                            " should be CANCELLATION or CHANGE, or penaltyText"
                            " and information is not empty"
                        ),
                        "error": "Bad Request",
                    }
                ),
                mimetype="application/json",
                status_code=500,
            )
    except Exception as e:
        logging.error(e)
        return func.HttpResponse(
            json.dumps({"cause": str(e), "error": "Internal Server Error"}),
            mimetype="application/json",
            status_code=500,
        )


def get_parameter(req: object, parameter: str) -> str:
    """
    get the parameter from the request
    Args:
        req: request, parameter: parameter to get
    Returns:
        parameter string
    """
    parameter_string = req.params.get(parameter)
    if not parameter_string:
        try:
            req_body = req.get_json()
        except ValueError:
            raise ValueError("Request body must be valid JSON")
        else:
            parameter_string = req_body.get(parameter)
    return parameter_string


def validate_req(req) -> bool:
    """
    this function validate the information of the request
    Args:
        req: request
    Returns:
        dict with the parameters
    """
    parameter_task = get_parameter(req, "task")
    correct_task = validate_task(parameter_task)
    logging.info("======================================")
    logging.warning("correct_task: " + str(correct_task))
    parameter_information = get_parameter(req, "information")
    parameter_penalty_text = get_parameter(req, "penaltyText")
    fare_basis = str(parameter_penalty_text[0]["fareBasis"])
    correct_penalty = validate_text(parameter_penalty_text)
    logging.warning("correct_penalty: " + str(correct_penalty))
    correct_information = validate_text(parameter_information)
    logging.warning("correct_information: " + str(correct_information))
    logging.warning("fareBasis: " + fare_basis)
    logging.info("======================================")
    if correct_task and correct_penalty and correct_information:
        return True
    else:
        return False


def validate_task(parameter_task: str):
    if parameter_task not in ["CANCELLATION", "CHANGE", "MANUALCHANGE", "FUELSURCHARGE"]:
        return False
    else:
        return True


def validate_text(parameter_text: str):
    if parameter_text is None:
        return False
    elif parameter_text == "":
        return False
    else:
        return True


def validate_token(token: str) -> bool:
    """
    this function validate the token
    Args:
        token: token
    Returns:
        bool
    """
    if token is None:
        return False
    try:
        logging.warning("validate_token")
        jwk = get_jwk()
        token = token.replace("Bearer ", "")
        claims = jwt.decode(token, jwk)
        claims.validate()
        logging.info("token validated")
        return True
    except Exception as e:
        logging.error(e)
        return False
