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
    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new(
        req.route_params["functionName"], None, None
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
