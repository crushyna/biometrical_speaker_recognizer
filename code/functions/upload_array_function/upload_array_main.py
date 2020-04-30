from io import BytesIO
import requests
import os
from json import dumps
from flask_restful import Resource
from models.voice_array_model import VoiceArrayModel
from helpers.helpers import UploadFileToDatabase
from src.sound_preprocessor_1 import SoundPreprocessor
from numpy import save

UPLOAD_FOLDER = 'code/temp/voicefiles'
ARRAYS_FOLDER = 'code/temp/arrays'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


class VoiceArrayUploader(Resource):

    def post(self, merchant_id, user_id, text_id, filename):
        """
        create an ndarray out of .wav file sample and upload it to database
        :return: json message
        """
        # initialize voice array model from input data
        new_voice_array = VoiceArrayModel(merchant_id, user_id, text_id, filename)

        # retrieve filepath/filename for storing data on server
        remote_dest = VoiceArrayUploader.get_remote_destination(new_voice_array.merchant_id, new_voice_array.user_id, new_voice_array.text_id)
        filename_to_upload = remote_dest['message']

        # transform input wavefile
        input_sound = SoundPreprocessor(os.path.join(UPLOAD_FOLDER, filename))
        input_sound.convert_stereo_to_mono()
        input_sound.fourier_transform_audio()
        input_sound.minmax_array_numpy()

        save(os.path.join(ARRAYS_FOLDER, filename_to_upload), input_sound.scipy_audio)

        # upload to database as binary
        result = UploadFileToDatabase.post(os.path.join(ARRAYS_FOLDER, filename_to_upload))

        # delete local array
        os.remove(os.path.join(ARRAYS_FOLDER, filename_to_upload))

        return {'message': result.json()}

    @staticmethod
    def get_remote_destination(merchant_id, user_id, text_id):  # "merchantId: 100000, "userId": 100001, "textId": 100001

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
        if response.status_code == 200:
            remote_filename = response.json()['data']['fileAddress']
            return {'message': remote_filename,
                    'status': 'success'}
        else:
            return {
                       'message': 'Cannot establish connection to the server!',
                       'status': 'error'
                   }, 400
