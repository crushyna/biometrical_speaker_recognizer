import os
from dataclasses import dataclass
import requests
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

UPLOAD_FOLDER = 'code/temp/voicefiles'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ARRAYS_FOLDER = 'code/temp/arrays'
if not os.path.exists(ARRAYS_FOLDER):
    os.makedirs(ARRAYS_FOLDER)

IMAGES_FOLDER = 'code/temp/voice_images'
if not os.path.exists(IMAGES_FOLDER):
    os.makedirs(IMAGES_FOLDER)


@dataclass
class WorkingFolders:
    upload_folder = UPLOAD_FOLDER
    arrays_folder = ARRAYS_FOLDER
    images_folder = IMAGES_FOLDER


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

        return {'message': user_data_dict['text_phrase']}, 200


class VoiceFileUpload(Resource):
    """
    endpoint for uploading new wavefile from front-end
    """

    @staticmethod
    def post(filename):
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
                   'message': 'Something when wrong',
                   'status': 'error'
               }, 400


class DownloadFileFromDatabase:

    @staticmethod
    def get(filename, destination):
        """
        download specific file from database
        :param destination: string
        :param filename: string
        :return: location + filename
        """

        url = f"https://dbapi.pl/file/download/{filename}"
        response = requests.get(url)

        if response.status_code == 200:
            with open(os.path.join(destination, filename), 'wb') as f:
                f.write(response.content)

            return {
                'message': os.path.join(destination, filename),
                'status': 'success'
            }
        else:
            return {
                'message': 'Something when wrong or file does NOT exist on remote server!',
                'status': 'error'
            }


class UploadFileToDatabase:

    @staticmethod
    def post(filename):
        """
        just read class name
        :param filename:
        :return: json response
        """
        url = "https://dbapi.pl/file/upload"
        files = [
            ('file', open(filename, 'rb'))
        ]
        response = requests.request("POST", url, files=files)
        if response.status_code == 201:
            return response.json()
        else:
            return {
                       'message': 'Something when wrong or file does NOT exist on remote server!',
                       'status': 'error'
                   }, 400
