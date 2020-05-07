from json import dumps

import requests


class VoiceImageModel:

    def __init__(self, merchant_id: int, user_id: int, user_email: str, text_id: int, image_id: int, image_file: str):
        self.merchant_id = merchant_id
        self.user_id = user_id
        self.user_email = user_email
        self.text_id = text_id
        self.image_id = image_id
        self.image_file = image_file

    @staticmethod
    def retrieve_user_image_data(merchant_id, user_email, text_id):
        from json import JSONDecodeError
        new_image_data_dict = {}
        url = f"https://dbapi.pl/texts/byEmail/{merchant_id}/{user_email}"
        response = requests.request("GET", url)

        if response.status_code not in (200, 201):
            return False
        else:
            response = requests.request("GET", url).json()

        user_id = response['data']['userId']

        for each_text_data in response['data']['texts']:
            if each_text_data['textId'] == text_id:
                new_image_data_dict = {'user_id': user_id,
                                       'user_email': user_email,
                                       'text_id': each_text_data['textId'],
                                       'image_id': each_text_data['imageId'],
                                       'image_file': each_text_data['imageFile'],
                                       'merchant_id': merchant_id,
                                       }
                return new_image_data_dict
            else:
                return False

    @staticmethod
    def get_list_of_numpy_arrays(merchant_id, user_id, text_id):
        url = f"https://dbapi.pl/samples/byUserIdAndTextId/{merchant_id}/{user_id}/{text_id}"
        numpy_arrays_list = []
        response = requests.request("GET", url)
        data = response.json()
        if response.status_code in (200, 201):
            for each_sample in data['data']['samples']:
                var = each_sample['sampleFile']
                numpy_arrays_list.append(var)

            return numpy_arrays_list
        else:
            return False

    @staticmethod
    def get_remote_destination(merchant_id, user_id, text_id):

        url = "https://dbapi.pl/image/add"
        payload = {
            "merchantId": merchant_id,
            "userId": user_id,
            "textId": text_id
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=dumps(payload))
        if response.status_code in (200, 201):
            remote_filename = response.json()['data']['imageFile']
            return remote_filename
        else:
            return False
