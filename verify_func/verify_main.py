from io import BytesIO
import requests
from flask import jsonify
from flask.json import loads
from flask_restful import Resource, reqparse
# from src.controllers.azure_sql_controller import SQLController
# from src.controllers.azure_blob_controller import AzureBlobController
from src.image_preprocessor_1 import ImagePreprocessor
from src.sound_preprocessor_1 import SoundPreprocessor
# from code.models.user_model import InitialUserModel


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
        text_phrase_dict = {}
        url = f"https://dbapi.pl/texts/byEmail/100000/{user_email}"
        try:
            response = requests.request("GET", url)
            for each_item in response.json():
                text_id_list.append(each_item['textId'])
                next_dict = {each_item['textId']: each_item['phrase']}
                text_phrase_dict.update(next_dict)
        except:
            return {'message': 'Cannot establish database connection or user does not exist!'}, 404

        selected_text_id = random.choice(text_id_list)

        return {'text_phrase': text_phrase_dict[selected_text_id]}, 200


class VoiceVerification(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, user_email, us_image_file, us_text_id):

        initial_user_data = f"https://dbapi.pl/texts/byEmail/100000/{user_email}"

        # make connections
        # self.verify_main_sql_database = SQLController()
        # self.verify_main_blob_service = AzureBlobController(self.azure_blob_connection_string, self.blob_container)

    def verify_voice(self):
        """
        entry point for module, that is simple voice hash comparison
        :return: bool
        """

        # check if requested data exists
        user_id, voice_id = self.verify_main_sql_database.get_user_id_and_voice_id(self.user_login)
        voices_list = self.verify_main_blob_service.ls_files(self.blob_folder)
        if self.sound_sample_filename not in voices_list:
            raise FileNotFoundError('File not found in blob container!')

        # TODO: needs recognition Voice Image per Text
        # get database-stored image into buffer
        voice_image_id = self.verify_main_sql_database.get_image_voice_id(voice_id, self.text_id)
        voice_image_bytes = self.verify_main_sql_database.download_voice_image(voice_image_id)
        stored_image_buffer: BytesIO
        _, stored_image_buffer = ImagePreprocessor.generate_audio_image(voice_image_bytes)

        # get input file from blob
        input_blob_buffer: BytesIO
        _, input_blob_buffer = self.verify_main_blob_service.download_file_to_bytesbuffer(
            self.blob_folder + self.sound_sample_filename)

        # process input sound
        input_sound = SoundPreprocessor(self.user_login, input_blob_buffer)
        input_sound.convert_stereo_to_mono()
        input_sound.fourier_transform_audio()
        input_sound.minmax_array_numpy()

        # generate image from processed audio and put it into buffer
        input_image_buffer: BytesIO
        _, input_image_buffer = ImagePreprocessor.generate_audio_image(input_sound.scipy_audio)

        # compare images
        image_preprocessor = ImagePreprocessor(input_image_buffer, stored_image_buffer)

        result_dhash = image_preprocessor.compare_dhash()
        result_whash = image_preprocessor.compare_whash()

        print(f"DHASH Difference: {result_dhash}")
        print(f"WHASH Difference: {result_whash}")

        # close BytesIO buffers
        stored_image_buffer.close()
        input_image_buffer.close()
        input_blob_buffer.close()

        if result_dhash > 1000 or result_whash > 1000:
            return False
        else:
            if result_dhash / result_whash > 0.85:
                if result_dhash + result_whash <= 1500:
                    return True
                else:
                    return False
            else:
                return False

        # TODO: upload result if OK
        # if result (some operation) then:
        # upload result = upload_voice_array(user_id, sound_sample)
