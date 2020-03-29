import logging
import azure.functions as func
from .generate_image_main import VoiceImageGenerator


def main(req: func.HttpRequest):
    logging.info('Python HTTP trigger function processed a request.')
    user_id = req.route_params.get('user_id')
    text_id = req.route_params.get('text_id')
    message = f"User ID: {user_id}, text ID: {text_id}"
    logging.info(message)

    if type(user_id) == str:
        print(f"Starting function for user ID: {user_id}, text ID: {text_id}!")
        try:
            function_client = VoiceImageGenerator(int(user_id), int(text_id))
            result1 = function_client.generate_binary_voice_image()
            return func.HttpResponse(f'Result1: {result1}', status_code=200)
        except Exception as ex:
            return func.HttpResponse(str(ex), status_code=400)

    else:
        return func.HttpResponse(
             "Please pass a user ID on the query string or in the request body",
             status_code=400
        )
