import logging
import azure.functions as func
from .verify_main import VoiceVerification


def main(req: func.HttpRequest):
    logging.info('Python HTTP trigger function processed a request.')
    login = req.route_params.get('login')
    sample_name = req.route_params.get('sample_name')
    text_id = req.route_params.get('text_id')
    message = f"Login: {login}, Sample name: {sample_name}"
    logging.info(message)

    if type(login) == str:
        print(f"Starting function for {message}")
        try:
            function_client = VoiceVerification(login, sample_name, int(text_id))
            result1 = function_client.verify_voice()
            if result1:
                return func.HttpResponse(status_code=200)
            else:
                return func.HttpResponse(status_code=403)
        except Exception as ex:
            logging.info(ex)
            return func.HttpResponse(str(ex), status_code=400)
    else:
        return func.HttpResponse("Please pass a user login on the query string or in the request body", status_code=400)
