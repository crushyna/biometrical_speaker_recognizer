import requests


class VoiceImageModel:

    def __init__(self, user_id: int, user_email: str, text_id: int, image_id: int, image_file: str):
        self.user_id = user_id
        self.user_email = user_email
        self.text_id = text_id
        self.image_id = image_id
        self.image_file = image_file

    @staticmethod
    def retrieve_user_image_data(user_email, text_id):
        from json import JSONDecodeError
        new_image_data_dict: dict
        url = f"https://dbapi.pl/texts/byEmail/100000/{user_email}"
        try:
            response = requests.request("GET", url).json()
        except JSONDecodeError:
            return {'message': 'Image data not found!',
                    'status': 'error'}
        user_id = response['data']['userId']
        for each_text_data in response['data']['texts']:
            if each_text_data['textId'] == text_id:
                new_image_data_dict = {'user_id': user_id,
                                      'user_email': user_email,
                                      'text_id': each_text_data['textId'],
                                      'image_id': each_text_data['imageId'],
                                      'image_file': each_text_data['imageFile'],
                                      }

        return new_image_data_dict
