import requests
from flask_restful import Resource

import Config


class GetSamplesInfoByUserId(Resource):

    def get(self, merchant_id: int, user_id: int):
        from json import JSONDecodeError
        url = f"https://dbapi.pl/samples/info/byUserId/{merchant_id}/{user_id}"
        basic_auth = Config.BasicAuth()
        try:
            response = requests.request("GET", url, auth=(basic_auth.login, basic_auth.password))
        except JSONDecodeError:
            return {'message': 'Database error!',
                    'status': 'error'}, 403

        return response.json()


class GetTextsRandom(Resource):

    def get(self, number_of_missing_texts: int):
        from json import JSONDecodeError
        url = f"https://dbapi.pl/texts/random/{number_of_missing_texts}"
        basic_auth = Config.BasicAuth()
        try:
            response = requests.request("GET", url, auth=(basic_auth.login, basic_auth.password))
        except JSONDecodeError:
            return {'message': 'Database error!',
                    'status': 'error'}, 403

        return response.json()


class GetTextsInfoByUserId(Resource):

    def get(self, merchant_id: int, user_id: int):
        from json import JSONDecodeError
        url = f"https://dbapi.pl/texts/info/byUserId/{merchant_id}/{user_id}"
        basic_auth = Config.BasicAuth()
        try:
            response = requests.request("GET", url, auth=(basic_auth.login, basic_auth.password))
        except JSONDecodeError:
            return {'message': 'Database error!',
                    'status': 'error'}, 403

        return response.json()
