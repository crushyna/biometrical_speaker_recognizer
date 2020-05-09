from json import dumps
from json import JSONDecodeError
import requests


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
        try:
            response = requests.request("GET", url).json()
        except JSONDecodeError:
            return {'message': 'User data not found!',
                    'status': 'error'}
        user_id = response['data']['userId']
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
                return False

        return new_user_data_dict

    @staticmethod
    def add_new_user(user_email: str, merchant_id: int, password: str):
        url = "https://dbapi.pl/user/add"

        payload = {
            "email": user_email,
            "merchantId": merchant_id,
            "password": password
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=dumps(payload))

        return response

    @staticmethod
    def retrieve_logging_user_data(merchant_id: int, user_email: str, password: str):
        url1 = f"https://dbapi.pl/texts/byEmail/{merchant_id}/{user_email}"
        try:
            response1 = requests.request("GET", url1).json()
        except JSONDecodeError as error:
            return error

        user_id = response1['data']['userId']

        url2 = f"https://dbapi.pl/user/byId/{merchant_id}/{user_id}"
        try:
            response2 = requests.request("GET", url2).json()
        except JSONDecodeError as error:
            return error

        user_password = response2['data']['password']

        if user_password == password:
            return True
        else:
            return False
