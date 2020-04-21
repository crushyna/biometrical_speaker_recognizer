from src.controllers.azure_sql_controller import SQLController
from src.sound_preprocessor_1 import SoundPreprocessor
from flask_restful import Resource


class VoiceImageGenerator(Resource):

    def __init__(self, user_id: int, text_id: int):
        self.name = str(user_id)
        self.user_id = user_id
        self.text_id = text_id
        self.generate_image_sql_database = SQLController()

    def generate_binary_voice_image(self):
        """
        generates binary image from average values of voice arrays (per specific text) and upload it up to database
        returns 1 if it's done correctly
        :return: bool
        """

        # first: check, if user even exists
        user_login, voice_id = self.generate_image_sql_database.get_user_login_and_voice_id(self.user_id)

        # create ndarray from selected arrays
        arrays_list = self.generate_image_sql_database.download_user_voice_arrays(self.user_id, self.text_id)
        image_ndarray = SoundPreprocessor.create_voice_image_mean_array(arrays_list)

        # update Voice Image Link table first, get new Voice Image ID in return
        voice_image_id = self.generate_image_sql_database.update_voice_image_link(voice_id, self.text_id)

        # upload voice image
        result1 = self.generate_image_sql_database.upload_voice_image(int(voice_image_id), image_ndarray)

        return result1
