import os
from numpy import load
from helpers.helpers import DownloadFileFromDatabase, WorkingFolders, UploadFileToDatabase
from src.image_preprocessor_1 import ImagePreprocessor
from src.sound_preprocessor_1 import SoundPreprocessor
from models.voice_image_model import VoiceImageModel
from flask_restful import Resource


class VoiceImageGenerator(Resource):

    def post(self, merchant_id: int, user_id: int, text_id: int):
        '''
        comment to add here
        '''

        # get list of .npy files per user / text
        response_list = VoiceImageModel.get_list_of_numpy_arrays(merchant_id, user_id, text_id)

        if not response_list:
            return {
                       'message': 'Connection error! Cannot retrieve list of numpy arrays from database!',
                       'status': 'error'
                   }, 500

        # get name of image file to upload
        image_filename = VoiceImageModel.get_remote_destination(merchant_id, user_id, text_id)

        if not image_filename:
            return {
                       'message': 'Connection error! Cannot retrieve image destination from database!',
                       'status': 'error'
                   }, 500

        # download all voice arrays per user per text, and create separate list with numpy values
        local_numpy_files_list = []
        local_arrays_list = []

        for each_numpy_file in response_list:
            next_numpyfile = DownloadFileFromDatabase.get(filename=each_numpy_file,
                                                          destination=WorkingFolders.arrays_folder)
            if not next_numpyfile:
                return {'message': f'Cannot retrieve {each_numpy_file} from database!',
                        'status': 'error'}, 400

            local_numpy_files_list.append(next_numpyfile)
            local_arrays_list.append(load(next_numpyfile))

        # compile all local numpy files into one image
        local_image_file = VoiceImageGenerator.generate_binary_voice_image(arrays_list=local_arrays_list,
                                                                           local_filename=os.path.join(
                                                                               WorkingFolders.images_folder,
                                                                               image_filename))

        if not os.path.isfile(local_image_file):
            return {
                       'message': 'Error when creating binary voice image!!',
                       'status': 'error'
                   }, 500

        # upload new image file to database
        final_result = UploadFileToDatabase.post(local_image_file)

        # clean up used data
        os.remove(local_image_file)
        for each_file in local_numpy_files_list: os.remove(each_file)

        return final_result

    @staticmethod
    def generate_binary_voice_image(arrays_list: list, local_filename: str):
        """
        generates binary image from average values of voice arrays (per specific text) and upload it up to database
        :return: bool
        """

        # create ndarray from selected arrays
        image_ndarray = SoundPreprocessor.create_voice_image_mean_array(arrays_list)

        # generate image out of compiled ndarray file
        _, stored_image_buffer = ImagePreprocessor.generate_audio_image(image_ndarray)

        with open(local_filename, "wb") as f:
            f.write(stored_image_buffer.getbuffer())

        return local_filename
