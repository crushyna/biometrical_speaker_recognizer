from io import BytesIO
import os
from flask_restful import Resource, reqparse
from src.image_preprocessor_1 import ImagePreprocessor
from src.sound_preprocessor_1 import SoundPreprocessor
from models.user_model import UserModel
from helpers.helpers import WorkingFolders, DownloadFileFromDatabase


class VoiceVerification(Resource):
    """
    Entry point for actual function of this application.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="Missing user_id in request!"
                        )
    parser.add_argument('text_id',
                        type=int,
                        required=True,
                        help="Missing text_id in request!!"
                        )
    parser.add_argument('filename',
                        type=str,
                        required=True,
                        help="Missing filename in request!"
                        )

    def get(self, user_email: str, text_id: int, filename: str):
        """
        First, create user model.
        Then, check if filename provided by front-end DOES exists on back-end server.
        Then, download voice image file from database to back-end server.
        Finally, execute verify_voice() function and return it's result.
        :param user_email: str
        :param text_id: int
        :param filename: str
        :return: json message
        """
        # create User model
        user_data = UserModel.retrieve_user_data_3(user_email, text_id)
        ongoing_user = UserModel(**user_data)

        # check, if wavefile uploaded from front-end exists
        local_file_exist = os.path.isfile(os.path.join(WorkingFolders.upload_folder, filename))
        if not local_file_exist:
            return {'message': f'File: {filename} has not been found on back-end server!',
                    'status': 'error'}

        # download voice image per user, per text
        file_from_server_path = DownloadFileFromDatabase.get(ongoing_user.image_file, WorkingFolders.images_folder)
        if file_from_server_path['status'] == 'error':
            return {'message': f'Remote file not found! Searched filename: {ongoing_user.image_file}',
                    'status': 'error'}, 400

        # check, if downloaded file exist
        remote_file_exist = os.path.isfile(os.path.join(WorkingFolders.images_folder, ongoing_user.image_file))

        # run verification function
        verification_result = VoiceVerification.verify_voice(user_email,
                                                             os.path.join(WorkingFolders.upload_folder, filename),
                                                             file_from_server_path)

        # return results
        return {'ongoing_user': ongoing_user.return_all_attributes(),
                'local_filename': filename,
                'local_file_exists': local_file_exist,
                'remote_image_filename': ongoing_user.image_file,
                'remote_image_filename_exists': remote_file_exist,
                'file_from_server_path': file_from_server_path['message'],
                'verification_result': verification_result
                }, 200

        # os.remove(file_from_server_path['message'])

    @staticmethod
    def verify_voice(user_email, local_wavefile, local_voice_image):

        # process input sound
        input_sound = SoundPreprocessor(local_wavefile)
        input_sound.convert_stereo_to_mono()
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

    def _old_verify_voice(self):
        """
        entry point for module, that is simple voice hash comparison
        :return: bool
        """

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
