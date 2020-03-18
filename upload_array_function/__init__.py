import logging
import azure.functions as func
import pyodbc
from . import upload_array_main


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.params.get('user_id')
    if not user_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            user_id = req_body.get('user_id')

    if user_id:
        print(f"Starting function for user ID: {user_id}!")
        try:
            # test voice sample only for now!
            result1 = upload_array_main.upload_voice_array(int(user_id), 'src/test_sounds/clint_eastwood_2.wav')
            return func.HttpResponse(f'Result1: {result1}', status_code=200)
        except IndexError:
            return func.HttpResponse(f'User ID: {user_id} not found!', status_code=204)
        except ValueError:
            return func.HttpResponse(f'Inproper input data!', status_code=400)

    else:
        return func.HttpResponse(
            "Please pass a user ID on the query string or in the request body",
            status_code=400
        )
