from io import BytesIO
import requests
from flask_restful import Resource
from models.voice_array_model import VoiceArrayModel
from src.sound_preprocessor_1 import SoundPreprocessor


class VoiceArrayUploader(Resource):

    def post(self, merchant_id, user_id, text_id, filename):    # "merchantId: 100000, "userId": 100001, "textId": 100001
        # initialize model from input data
        new_voice_array = VoiceArrayModel(merchant_id, user_id, text_id, filename)

        # retrieve filepath/filename for storing data on server
        url = "https://dbapi.pl/sample/add"
        payload = {
            "merchantId": new_voice_array.merchant_id,
            "userId": new_voice_array.user_id,
            "textId": new_voice_array.text_id
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        remote_filename = response.text.encode('utf8')

        return {'message': remote_filename,
                'status': 'success'}

    def upload_voice_array(self, remote_filename):
        """
        create an ndarray out of .wav file sample and upload it to database
        :return: json message
        """

        # first: check, if user even exists

        # get new file from blob
        input_blob_buffer: BytesIO
        _, input_blob_buffer = self.upload_array_blob_service.download_file_to_bytesbuffer(
            self.blob_folder + self.sound_sample_filename)

        input_sound = SoundPreprocessor(login, input_blob_buffer)
        input_sound.convert_stereo_to_mono()
        input_sound.fourier_transform_audio()
        input_sound.minmax_array_numpy()

        # upload to database as binary
        result = self.upload_array_sql_database.upload_voice_array(self.user_id, input_sound.scipy_audio, self.text_id)

        input_blob_buffer.close()

        return result
