# This function an HTTP starter function for Durable Functions.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable activity function (default name is "Hello")
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json
import azure.functions as func
import azure.durable_functions as df


async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:

    logging.info("Python HTTP trigger function processed a request.")
    parameter_task = get_parameter(req, "task")
    parameter_information = get_parameter(req, "information")
    parameter_penalty_text = get_parameter(req, "penaltyText")
    dict_parameters = {
        "task": parameter_task,
        "information": parameter_information,
        "penaltyText": parameter_penalty_text,
    }
    logging.warning("starter: " + starter)

    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new(
        req.route_params["functionName"], None, dict_parameters
    )

    logging.info(f"Started orchestration with ID = '{instance_id}'.")

    respond = await client.get_status(instance_id)

    while respond.runtime_status.value != "Completed":
        respond = await client.get_status(instance_id)
        logging.warning(f"Orchestration status: {respond.runtime_status.value}")
        if respond.runtime_status.value == "Failed":
            return func.HttpResponse(
                f"Orchestration failed: {respond.custom_status}"
            )

    return func.HttpResponse(
        json.dumps(respond.output),
        mimetype="application/json",
        status_code=200,
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
            pass
        else:
            parameter_string = req_body.get(parameter)
    return parameter_string