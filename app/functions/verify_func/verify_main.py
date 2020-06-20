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
        user_data = UserModel.retrieve_user_data_3(merchant_id, user_email, text_id)
        if 'status' or 'error' in user_data:
            return user_data

        ongoing_user = UserModel(**user_data)

        # check, if wavefile uploaded from front-end exists
        local_file_exist = os.path.isfile(os.path.join(WorkingFolders.upload_folder, filename))
        if not local_file_exist:
            return {'message': f'File: {filename} has not been found on back-end server!',
                    'status': 'error'}, 400

        # download voice image per user, per text
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
        verification_result = VoiceVerification.verify_voice(user_email,
                                                             os.path.join(WorkingFolders.upload_folder, filename),
                                                             file_from_server_path)

        # clear space
        os.remove(file_from_server_path)

        return {'verification_result': verification_result}, 200

        """        
        return {'ongoing_user': ongoing_user.return_all_attributes(),
                'local_filename': filename,
                'local_file_exists': local_file_exist,
                'remote_image_filename': ongoing_user.image_file,
                'remote_image_filename_exists': remote_file_exist,
                'file_from_server_path': file_from_server_path,
                'verification_result': verification_result
                }, 200
        
        """

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

        if result_dhash > 1000 or result_whash > 1000:
            return {'message': 'Values over 1000!',
                    'status': 'error'}
        else:
            print(result_dhash)
            print(result_whash)
            if result_dhash / result_whash > 0.85:
                if result_dhash + result_whash <= 1500:
                    return {'message': f'Sum: {result_dhash + result_whash}',
                            'status': 'success'}
                else:
                    return {'message': f'Sum: {result_dhash + result_whash}',
                            'status': 'error'}
            else:
                return {'message': f'Division: {result_dhash / result_whash}',
                        'status': 'error'}

        '''
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
        '''

        # TODO: upload result if OK
        # if result (some operation) then:
        # upload result = upload_voice_array(user_id, sound_sample)
