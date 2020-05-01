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
    def retrieve_user_data_3(user_email, text_id):
        from json import JSONDecodeError
        new_user_data_dict: dict
        url = f"https://dbapi.pl/texts/byEmail/100000/{user_email}"
        try:
            response = requests.request("GET", url).json()
        except JSONDecodeError:
            return {'message': 'User data not found!',
                    'status': 'error'}
        user_id = response['data']['userId']
        for each_text_data in response['data']['texts']:
            if each_text_data['textId'] == text_id:
                new_user_data_dict = {'user_id': user_id,
                                      'image_file': each_text_data['imageFile'],
                                      'image_id': each_text_data['imageId'],
                                      'text_id': each_text_data['textId'],
                                      'text_phrase': each_text_data['phrase'],
                                      }

        return new_user_data_dict
