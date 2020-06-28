import os
from dataclasses import dataclass
import requests
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
import Config

UPLOAD_FOLDER = 'temp/wavefiles'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ARRAYS_FOLDER = 'temp/arrays'
if not os.path.exists(ARRAYS_FOLDER):
    os.makedirs(ARRAYS_FOLDER)

IMAGES_FOLDER = 'temp/voice_images'
if not os.path.exists(IMAGES_FOLDER):
    os.makedirs(IMAGES_FOLDER)


@dataclass
class WorkingFolders:
    upload_folder = UPLOAD_FOLDER
    arrays_folder = ARRAYS_FOLDER
    images_folder = IMAGES_FOLDER


class ConnectionTest(Resource):
    """
    simple connection test resource
    returns simple JSON message
    """
    def get(self):
        return {'message': "GET function called. Working correctly."}, 200

    def put(self):
        return {'message': "PUT function called. Working correctly."}, 200

    def post(self):
        return {'message': "POST function called. Working correctly."}, 200


class CheckIfUserExists(Resource):
    """
    checks if user exists in database.
    Returns 200 if exists, 404 if not.
    Keep in mind, that status code 404 actually might be the one you need (for example: when adding new user).
    """
    def get(self, merchant_id: int, user_email: str):
        from json import JSONDecodeError
        url = f"https://dbapi.pl/user/check/exist/{merchant_id}/{user_email}"
        basic_auth = Config.BasicAuth()
        try:
            response = requests.request("GET", url, auth=(basic_auth.login, basic_auth.password))
        except JSONDecodeError:
            return {'message': 'Database error!',
                    'status': 'error'}, 403

        if response.status_code in (200, 201):
            return {'message': 'User exist!',
                    'status': 'success'}, 200
        elif response.status_code == 404:
            return {'message': 'User does not exists!',
                    'status': 'error'}, 404
        else:
            return {'message': 'Database error! @function: CheckIfUserExists',
                    'status': 'error'}, 500


class GetTextPhrase(Resource):

    def get(self, user_email: str, merchant_id: int):
        import random
        url = f"https://dbapi.pl/texts/byEmail/{merchant_id}/{user_email}"
        basic_auth = Config.BasicAuth()
        response = requests.request("GET", url, auth=(basic_auth.login, basic_auth.password))

        if response.status_code == 500:
            return {'message': 'Database server error!',
                    'status': 'error'}, 500

        elif response.status_code == 404:
            return response.json()

        try:
            response = response.json()
            number_of_text: int = len(response['data']['texts'])
            text_choice = random.choice(range(number_of_text))
            user_id = response['data']['userId']
            user_data_dict = {'user_id': user_id,
                              'image_file': response['data']['texts'][text_choice]['imageFile'],
                              'image_id': response['data']['texts'][text_choice]['imageId'],
                              'text_id': response['data']['texts'][text_choice]['textId'],
                              'text_phrase': response['data']['texts'][text_choice]['phrase'],
                              }
        except Exception:
            return {'message': 'Insufficient data for completing user model!',
                    'status': 'error'}, 500

        return {'message': {
            'data':
                {'textphrase': response['data']['texts'][text_choice]['phrase'],
                 'text_id': response['data']['texts'][text_choice]['textId'],
                 'user_id': response['data']['userId']
                 },
        },
                   'status': 'success'}, 200


class WaveFileUpload(Resource):
    """
    endpoint for uploading new wavefile from front-end to back-end (this) server
    """
    @staticmethod
    def post(filename: str):
        """
        Retrieve a new voicefile from the front-end.
        :return: json message
        """
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=FileStorage, location='files', help='File was not provided!')
        data = parse.parse_args()
        if data['file'] == "":
            return {
                       'message': 'No file found',
                       'status': 'error'
                   }, 400
        wave_file = data['file']

        if wave_file:
            wave_file.save(os.path.join(WorkingFolders.upload_folder, filename))
            return {
                       'message': 'File uploaded',
                       'status': 'success'
                   }, 200
        return {
                   'message': 'Something when wrong or file does not exist!',
                   'status': 'error'
               }, 400


class DownloadFileFromDatabase:

    @staticmethod
    def get(filename: str, destination: str):
        """
        download specific file from database
        :param destination: string
        :param filename: string
        :return: location + filename
        """

        url = f"https://dbapi.pl/file/download/{filename}"
        basic_auth = Config.BasicAuth()
        response = requests.get(url, auth=(basic_auth.login, basic_auth.password))

        if response.status_code == 200 or 201:
            with open(os.path.join(destination, filename), 'wb') as f:
                f.write(response.content)

            return os.path.join(destination, filename)
        else:
            return False


class UploadFileToDatabase:

    @staticmethod
    def post(filename: str):
        """
        just read class name
        :param filename: string
        :return: json response
        """
        url = "https://dbapi.pl/file/upload"
        basic_auth = Config.BasicAuth()
        files = [
            ('file', open(filename, 'rb'))
        ]
        response = requests.request("PUT", url, files=files, auth=(basic_auth.login, basic_auth.password))
        # status = response.status_code
        if response.status_code in (200, 201):
            return response.json()
        else:
            # return {
            #            'message': 'Something when wrong or file does NOT exist on remote server!',
            #            'status': 'error'
            #        }, 400

            if str(response.status_code).startswith('5'):
                return {
                           'message': 'Database server error!',
                           'status': 'error'
                       }, 502
            elif str(response.status_code).startswith('4'):
                return {
                           'message': 'Backend server error!',
                           'status': 'error'
                       }, 500
