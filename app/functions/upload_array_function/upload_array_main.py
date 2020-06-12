import requests
import os
from json import dumps
from flask_restful import Resource
from models.voice_array_model import VoiceArrayModel
from helpers.helpers import UploadFileToDatabase, WorkingFolders
from src.sound_preprocessor_1 import SoundPreprocessor
from numpy import save


class VoiceArrayUploader(Resource):

    def post(self, merchant_id: int, user_id: int, text_id: int, local_filename: str):
        """
        create an ndarray out of .wav file sample and upload it to database
        :return: json message
        """
        # initialize voice array model from input data
        new_voice_array = VoiceArrayModel(merchant_id, user_id, text_id, local_filename)
        new_voice_array_exist = os.path.isfile(os.path.join(WorkingFolders.upload_folder, local_filename))
        if not new_voice_array_exist:
            return {'message': f'Filename: {local_filename} does not exists on back-end server!',
                    'status': 'error'}, 404

        # retrieve filepath/filename for storing data on server
        filename_to_upload = VoiceArrayModel.get_remote_destination(new_voice_array.merchant_id, new_voice_array.user_id, new_voice_array.text_id)

        if filename_to_upload is False:
            return {'message': 'Cannot establish connection to the database server!',
                    'status': 'error'}, 400

        # transform input wavefile
        input_sound = SoundPreprocessor(os.path.join(WorkingFolders.upload_folder, local_filename))
        # input_sound.convert_stereo_to_mono()
        input_sound.fourier_transform_audio()
        input_sound.minmax_array_numpy()

        # save .npy file
        save(os.path.join(WorkingFolders.arrays_folder, filename_to_upload), input_sound.scipy_audio)

        # upload to database as binary
        result = UploadFileToDatabase.post(os.path.join(WorkingFolders.arrays_folder, filename_to_upload))

        # delete local array
        os.remove(os.path.join(WorkingFolders.arrays_folder, filename_to_upload))
        os.remove(os.path.join(WorkingFolders.upload_folder, new_voice_array.local_filename))

        return {'message': result}

