import requests
from flask.json import dumps


class VoiceArrayModel:

    def __init__(self, merchant_id: int, user_id: int, text_id: int, local_filename: str):
        self.merchant_id = merchant_id
        self.user_id = user_id
        self.text_id = text_id
        self.local_filename = local_filename

    @staticmethod
    def get_remote_destination(merchant_id: int, user_id: int,
                               text_id: int):  # "merchantId: 100000, "userId": 100001, "textId": 100001

        url = "https://dbapi.pl/sample/add"
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
            remote_filename = response.json()['data']['sampleFile']
            return remote_filename
        else:
            return False
