import logging
import azure.functions as func
import pyodbc
from . import generate_image_main


def main(req: func.HttpRequest):
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
            result1 = generate_image_main.generate_binary_voice_image(int(user_id))
            return func.HttpResponse(f'Result1: {result1}', status_code=200)
        except IndexError:
            return func.HttpResponse('Error! User does not exist in database!', status_code=404)
        except LookupError:
            raise func.HttpResponse("Voice image for this user already exists!", status_code=404)
        except ValueError:
            return func.HttpResponse(f'Inproper input data!', status_code=400)

    else:
        return func.HttpResponse(
             "Please pass a user ID on the query string or in the request body",
             status_code=400
        )
