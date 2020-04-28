import requests
from flask_restful import Resource
from models.user_model import UserModel


class VoiceVerificationTest(Resource):

    def get(self):
        return {'message': "GET function called. Working correctly."}, 200

    def put(self):
        return {'message': "PUT function called. Working correctly."}, 200

    def post(self):
        return {'message': "POST function called. Working correctly."}, 200


class GetTextPhrase(Resource):

    def get(self, user_email):
        import random
        from json import JSONDecodeError
        url = f"https://dbapi.pl/texts/byEmail/100000/{user_email}"
        try:
            response = requests.request("GET", url).json()
        except JSONDecodeError:
            return {'message': 'User email not found!',
                    'status': 'error'}
        number_of_text: int = len(response['data']['texts'])
        text_choice = random.choice(range(number_of_text))
        user_id = response['data']['userId']
        user_data_dict = {'user_id': user_id,
                          'image_file': response['data']['texts'][text_choice]['imageFile'],
                          'image_id': response['data']['texts'][text_choice]['imageId'],
                          'text_id': response['data']['texts'][text_choice]['textId'],
                          'text_phrase': response['data']['texts'][text_choice]['phrase'],
                          }

        # new_user = UserModel(**user_data_dict)
        # UserModel.create_table_for_users()
        # new_user.save_user_to_database()

        # return {'text_phrase': user_data_dict[selected_text_id]['text_phrase']}, 200
        # return {'ongoing user': f'{new_user.return_all_attributes()}'}
        return {'message': user_data_dict['text_phrase']}, 200
