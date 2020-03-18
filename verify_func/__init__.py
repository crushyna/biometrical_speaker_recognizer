import logging
import azure.functions as func
from . import verify_main


def main(req: func.HttpRequest):
    logging.info('Python HTTP trigger function processed a request.')

    login = req.params.get('login')
    if not login:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            login = req_body.get('name')

    if login:
        print(f"Starting function for login: {login}!")
        try:
            # test voice sample only for now!
            result1, result2 = verify_main.verify_voice(login, 'src/test_sounds/clint_eastwood_1.wav')
            return func.HttpResponse(f'Result1: {result1}, result2: {result2}', status_code=200)
        except IndexError:
            return func.HttpResponse(f'User {login} not found!', status_code=204)

    else:
        return func.HttpResponse("Please pass a user login on the query string or in the request body", status_code=400)
