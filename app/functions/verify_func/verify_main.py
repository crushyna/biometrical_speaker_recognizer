from io import BytesIO
import os
from flask_restful import Resource
from src.image_preprocessor_1 import ImagePreprocessor
from src.sound_preprocessor_1 import SoundPreprocessor
from models.user_model import UserModel
from helpers.helpers import WorkingFolders, DownloadFileFromDatabase


class VoiceVerification(Resource):
    """
    Entry point for actual magical function of this application.
    """

    def get(self, merchant_id: int, user_email: str, text_id: int, filename: str):
        """
        First, create user model.
        Then, check if filename provided by front-end DOES exists on back-end (this) server.
        Then, download voice image file from database to back-end server.
        Finally, execute verify_voice() function and return it's result.
        :param merchant_id: int
        :param user_email: str
        :param text_id: int
        :param filename: str
        :return: json message
        """
        # create User model
        print("Starting voice verification function...")
        user_data, status_code = UserModel.retrieve_user_data_3(merchant_id, user_email, text_id)
        # if status_code in (500, 404):
        if status_code != 200:
            return user_data, status_code

        ongoing_user = UserModel(**user_data)
        print("Ongoing user model created!")

        # check, if wavefile uploaded from front-end exists
        print("Searching for wavefile...")
        local_file_exist = os.path.isfile(os.path.join(WorkingFolders.upload_folder, filename))
        if not local_file_exist:
            return {'message': f'File: {filename} has not been found on back-end server!',
                    'status': 'error'}, 400

        # download voice image per user, per text
        print("Downloading voice image...")
        file_from_server_path = DownloadFileFromDatabase.get(ongoing_user.image_file, WorkingFolders.images_folder)
        if not file_from_server_path:
            return {'message': f'Error when downloading file from server: {ongoing_user.image_file}',
                    'status': 'error'}, 400

        # check, if downloaded voice image exist
        remote_file_exist = os.path.isfile(os.path.join(WorkingFolders.images_folder, ongoing_user.image_file))
        if not remote_file_exist:
            return {'message': f'Downloaded file not found! Searched filename: {ongoing_user.image_file}',
                    'status': 'error'}, 400

        # run verification function
        print("Veryfing voice...")
        verification_result = VoiceVerification.verify_voice(user_email,
                                                             os.path.join(WorkingFolders.upload_folder, filename),
                                                             file_from_server_path)

        # clear space
        os.remove(file_from_server_path)

        return {'verification_result': verification_result}, 200


    @staticmethod
    def verify_voice(user_email: str, local_wavefile: str, local_voice_image: str):

        # process input sound
        input_sound = SoundPreprocessor(local_wavefile)
        # input_sound.convert_stereo_to_mono()
        input_sound.fourier_transform_audio()
        input_sound.minmax_array_numpy()

        # generate image from processed audio and put it into buffer
        input_image_buffer: BytesIO
        _, input_image_buffer = ImagePreprocessor.generate_audio_image(input_sound.scipy_audio)

        # compare images
        image_preprocessor = ImagePreprocessor(input_image_buffer, local_voice_image)

        result_dhash = image_preprocessor.compare_dhash()
        result_whash = image_preprocessor.compare_whash()

        print(f"DHASH Difference: {result_dhash}")
        print(f"WHASH Difference: {result_whash}")

        # close BytesIO buffers
        input_image_buffer.close()

        """
        return {'dhash': str(result_dhash),
                'whash': str(result_whash)}
        """

        if result_dhash > 600 or result_whash > 600:
            return {'message': 'Values over 600!',
                    'dhash': str(result_dhash),
                    'whash': str(result_whash),
                    'status': 'error'}, 403
        elif result_dhash > result_whash:
            return {'message': 'DHASH bigger then WHASH!!',
                    'dhash': str(result_dhash),
                    'whash': str(result_whash),
                    'status': 'error'}, 403
        elif result_whash / result_dhash < 1.5:
            return {'message': 'Proportion lower than 1.5!!',
                    'dhash': str(result_dhash),
                    'whash': str(result_whash),
                    'status': 'error'}, 403
        else:
            if result_dhash < 250:
                if result_dhash <= 220:
                    return {'message': f'Minimal DHASH OK: {result_dhash}',
                            'dhash': str(result_dhash),
                            'whash': str(result_whash),
                            'status': 'success'}, 200
                elif result_dhash + result_whash < 650:
                    return {'message': f'Sum OK: {result_dhash + result_whash}',
                            'dhash': str(result_dhash),
                            'whash': str(result_whash),
                            'status': 'success'}, 200
                else:
                    return {'message': f'Sum too big: {result_dhash + result_whash}',
                            'dhash': str(result_dhash),
                            'whash': str(result_whash),
                            'status': 'error'}, 403
            else:
                return {'message': f'DHASH too big: {result_dhash}',
                        'dhash': str(result_dhash),
                        'whash': str(result_whash),
                        'status': 'error'}, 403

        # TODO: upload result if OK
        # if result (some operation) then:
        # upload result = upload_voice_array(user_id, sound_sample)
