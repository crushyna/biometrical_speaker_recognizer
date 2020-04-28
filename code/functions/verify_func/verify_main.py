from io import BytesIO
import os
import requests
from werkzeug.datastructures import FileStorage
from flask_restful import Resource, reqparse
from src.image_preprocessor_1 import ImagePreprocessor
from src.sound_preprocessor_1 import SoundPreprocessor
from models.user_model import UserModel
from helpers.helpers import DownloadFileFromDatabase

UPLOAD_FOLDER = 'code/functions/verify_func/temp_voicefiles'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


class VoiceFileUpload(Resource):
    """
    endpoint for uploading new wavefile from front-end
    """
    def post(self, filename):
        """
        Upload a new voicefile from front-end.
        :return: json message
        """
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=FileStorage, location='files', help='File was not provided!')
        data = parse.parse_args()
        if data['file'] == "":
            return {
                       'message': 'No file found',
                       'status': 'error'
                   }, 400
        wave_file = data['file']

        if wave_file:
            wave_file.save(os.path.join(UPLOAD_FOLDER, filename))
            return {
                       'message': 'File uploaded',
                       'status': 'success'
                   }, 200
        return {
                   'message': 'Something when wrong',
                   'status': 'error'
               }, 400


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

    def get(self, user_email, text_id, filename):
        user_data = UserModel.retrieve_user_data_3(user_email, text_id, filename)
        ongoing_user = UserModel(**user_data)

        # check, if file uploaded from front-end exists
        local_file_exist = os.path.isfile(os.path.join(UPLOAD_FOLDER, filename))

        # download voice image per user, per text
        file_from_server_path = DownloadFileFromDatabase.get(ongoing_user.image_file)
        if file_from_server_path[0]['status'] == 'error':
            return {'message': 'Remote file not found!',
                    'status': 'error'}, 400

        remote_file_exist = os.path.isfile(os.path.join(UPLOAD_FOLDER, ongoing_user.image_file))
        # file_from_server_exists = os.path.isfile(file_from_server_path)

        return {'ongoing_user': ongoing_user.return_all_attributes(),
                'local_filename': filename,
                'local_file_exists': local_file_exist,
                'remote_image_filename': ongoing_user.image_file,
                # 'file_from_server_exists': file_from_server_exists,
                'remote_image_filename_exists': remote_file_exist,
                'file_from_server_path_exists': file_from_server_path
                }, 200

    def verify_voice(self):
        # get database-stored image into buffer
        pass

    def _old_verify_voice(self):
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
