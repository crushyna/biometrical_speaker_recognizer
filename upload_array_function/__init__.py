import logging
import azure.functions as func
import pyodbc
from azure.core.exceptions import ResourceNotFoundError

from . import upload_array_main


def main(req: func.HttpRequest):
    logging.info('Python HTTP trigger function processed a request.')
    user_id = req.route_params.get('user_id')
    sample_name = req.route_params.get('sample_name')
    message = f"User ID: {user_id}, Sample name: {sample_name}"
    logging.info(message)

    if type(user_id) == str:
        print(f"Starting function for {message}")
        try:
            result1 = upload_array_main.upload_voice_array(int(user_id), sample_name)
            return func.HttpResponse(f'Result: {result1}', status_code=200)
        except Exception as ex:
            return func.HttpResponse(str(ex), status_code=400)

    else:
        return func.HttpResponse(
            "Please pass a user ID on the query string or in the request body",
            status_code=400
        )
