import os
from json import dumps

import requests
from numpy import load
from numpy.core.multiarray import ndarray

from helpers.helpers import DownloadFileFromDatabase, WorkingFolders
from src.image_preprocessor_1 import ImagePreprocessor
from src.sound_preprocessor_1 import SoundPreprocessor
from models.voice_image_model import VoiceImageModel
from flask_restful import Resource


class VoiceImageGenerator(Resource):

    def post(self, merchant_id, user_email, text_id):
        new_image_data: dict = VoiceImageModel.retrieve_user_image_data(merchant_id, user_email, text_id)

        if not isinstance(new_image_data, dict):
            return {'message': 'Database returned no sample data!',
                    'status': 'error'}, 500

        ongoing_image = VoiceImageModel(**new_image_data)

        # return ongoing_image.__dict__

        # get list of .npy files per user / text
        response_list: list = VoiceImageGenerator.get_list_of_numpy_arrays(ongoing_image.merchant_id, ongoing_image.user_id,
                                                                     ongoing_image.text_id)

        if not response_list:
            return {
                       'message': 'Cannot establish connection to the server!',
                       'status': 'error'
                   }, 400

        # return response_list

        # download all voice arrays per user per text
        local_numpys_list = []

        for each_numpy_file in response_list:
            next_numpyfile = DownloadFileFromDatabase.get(filename=each_numpy_file, destination=WorkingFolders.arrays_folder)
            local_numpys_list.append(load(next_numpyfile))

        return local_numpys_list

        # compile all local numpy files into one image
        local_image_file = VoiceImageGenerator.generate_binary_voice_image(arrays_list=local_numpys_list,
                                                                           local_filename=os.path.join(
                                                                               WorkingFolders.images_folder,
                                                                               ongoing_image.image_file))
        return local_image_file

    @staticmethod
    def generate_binary_voice_image(arrays_list, local_filename):
        """
        generates binary image from average values of voice arrays (per specific text) and upload it up to database
        :return: bool
        """

        # create ndarray from selected arrays
        image_ndarray = SoundPreprocessor.create_voice_image_mean_array(arrays_list)

        # return image_ndarray

        # generate image out of compiled ndarray file
        _, stored_image_buffer = ImagePreprocessor.generate_audio_image(image_ndarray)

        with open(local_filename, "wb") as f:
            f.write(stored_image_buffer.getbuffer())

        return local_filename

    @staticmethod
    def get_list_of_numpy_arrays(merchant_id, user_id, text_id):
        url = f"https://dbapi.pl/samples/byUserIdAndTextId/{merchant_id}/{user_id}/{text_id}"
        numpy_arrays_list = []
        response = requests.request("GET", url)
        data = response.json()
        if response.status_code == 200 or 201:
            for each_sample in data['data']['samples']:
                var = each_sample['sampleFile']
                numpy_arrays_list.append(var)

            return numpy_arrays_list
        else:
            return False

    @staticmethod
    def get_remote_destination(merchant_id, user_id, text_id):

        url = "https://dbapi.pl/image/add"
        payload = {
            "merchantId": merchant_id,
            "userId": user_id,
            "textId": text_id
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=dumps(payload))
        if response.status_code == 200 or 201:
            remote_filename = response.json()['data']['fileAddress']
            return {'message': remote_filename,
                    'status': 'success'}
        else:
            return {
                       'message': 'Cannot establish connection to the server!',
                       'status': 'error'
                   }, 400
