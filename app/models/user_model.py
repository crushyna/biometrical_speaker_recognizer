import base64
from json import dumps
from json import JSONDecodeError
import requests
import Config


class UserModel:

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def return_all_attributes(self):
        return self.__dict__

    @staticmethod
    def retrieve_user_data_3(merchant_id: int, user_email: str, text_id: int):
        new_user_data_dict: dict
        url = f"https://dbapi.pl/texts/byEmail/{merchant_id}/{user_email}"
        basic_auth = Config.BasicAuth()

        response = requests.request("GET", url, auth=(basic_auth.login, basic_auth.password))

        if response.status_code == 500:
            return {'message': 'Database server error!',
                    'status': 'error'}, 500

        elif response.status_code == 404:
            return response.json(), 404

        response = response.json()
        user_id = response['data']['userId']
        new_user_data_dict = {}
        for each_text_data in response['data']['texts']:
            if each_text_data['textId'] == text_id:
                new_user_data_dict = {'user_id': user_id,
                                      'merchant_id': merchant_id,
                                      'image_file': each_text_data['imageFile'],
                                      'image_id': each_text_data['imageId'],
                                      'text_id': each_text_data['textId'],
                                      'text_phrase': each_text_data['phrase'],
                                      }
            else:
                continue

        return new_user_data_dict, 200

    @staticmethod
    def add_new_user(user_email: str, merchant_id: int, password: str):
        url = "https://dbapi.pl/user/add"
        basic_auth = Config.BasicAuth()

        payload = {
            "email": user_email,
            "merchantId": merchant_id,
            "password": password
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=dumps(payload), auth=(basic_auth.login, basic_auth.password))

        return response

    @staticmethod
    def retrieve_logging_user_data(merchant_id: int, user_email: str, password: str):
        url1 = f"https://dbapi.pl/texts/byEmail/{merchant_id}/{user_email}"
        basic_auth = Config.BasicAuth()
        response1 = requests.request("GET", url1, auth=(basic_auth.login, basic_auth.password))
        if response1.status_code not in (200, 201):
            return {'message': 'Database error while executing url: https://dbapi.pl/texts/byEmail/',
                    'status': 'error'}

        user_id = response1.json()['data']['userId']

        url2 = f"https://dbapi.pl/user/byId/{merchant_id}/{user_id}"
        response2 = requests.request("GET", url2, auth=(basic_auth.login, basic_auth.password))
        if response2.status_code not in (200, 201):
            return {'message': 'Database error while executing url: https://dbapi.pl/user/byId/',
                    'status': 'error'}

        user_password = response2.json()['data']['password']

        if user_password == password:
            return {'message': 'authorized',
                    'status': 'success'}
        else:
            return {'message': 'unauthorized',
                    'status': 'success'}
