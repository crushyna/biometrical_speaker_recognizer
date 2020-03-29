import logging
import azure.functions as func
from .upload_array_main import VoiceArrayUploader


def main(req: func.HttpRequest):
    logging.info('Python HTTP trigger function processed a request.')
    user_id = req.route_params.get('user_id')
    sample_name = req.route_params.get('sample_name')
    text_id = req.route_params.get('text_id')
    message = f"User ID: {user_id}, sample name: {sample_name}, text ID: {text_id}"
    logging.info(message)

    if type(user_id) == str:
        print(f"Starting function for {message}")
        try:
            function_client = VoiceArrayUploader(int(user_id), sample_name, int(text_id))
            result1 = function_client.upload_voice_array()
            return func.HttpResponse(f'Result: {result1}', status_code=200)
        except Exception as ex:
            return func.HttpResponse(str(ex), status_code=400)

    else:
        return func.HttpResponse(
            "Please pass a user ID on the query string or in the request body",
            status_code=400
        )
