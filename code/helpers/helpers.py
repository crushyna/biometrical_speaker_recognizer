import requests
from flask_restful import Resource
from models.user_model import UserModel


class VoiceVerificationTest(Resource):

    def get(self):
        return {'message': "GET function called. Working correctly."}

    def put(self):
        return {'message': "PUT function called. Working correctly."}

    def post(self):
        return {'message': "POST function called. Working correctly."}


class GetTextPhrase(Resource):

    def get(self, user_email):
        import random
        text_id_list = []
        user_data_dict = {}
        url = f"https://dbapi.pl/texts/byEmail/100000/{user_email}"
        try:
            response = requests.request("GET", url)
            for each_item in response.json():
                text_id_list.append(each_item['textId'])
                next_full_dict = {each_item['textId']: {
                    'image_file': each_item['imageFile'],
                    'image_id': each_item['imageId'],
                    'text_phrase': each_item['phrase'],
                    'text_id': each_item['textId'],
                    'user_id': each_item['userId']
                }}
                user_data_dict.update(next_full_dict)
        except:
            return {'message': 'Cannot establish database connection or user does not exist!'}, 404

        selected_text_id = random.choice(text_id_list)

        new_user = UserModel(**user_data_dict[selected_text_id])
        UserModel.create_table_for_users()
        new_user.save_user_to_database()

        # return {'text_phrase': user_data_dict[selected_text_id]['text_phrase']}, 200
        # return {'ongoing user': f'{new_user.return_all_attributes()}'}
        return user_data_dict[selected_text_id]