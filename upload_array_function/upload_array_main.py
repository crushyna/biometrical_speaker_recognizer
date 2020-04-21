from io import BytesIO
from flask_restful import Resource
from src.controllers.azure_sql_controller import SQLController
from src.sound_preprocessor_1 import SoundPreprocessor
from src.controllers.azure_blob_controller import AzureBlobController


class VoiceArrayUploader(Resource):

    def __init__(self, user_id: int, sound_sample_filename: str, text_id: int):
        self.name = f'{user_id}+{sound_sample_filename}'
        self.user_id = user_id
        self.text_id = text_id
        self.sound_sample_filename = sound_sample_filename
        self.azure_blob_connection_string = """DefaultEndpointsProtocol=https;AccountName=storageaccountvbioma487;AccountKey=kQjOecdi/KtMStu4iQkxmsAbe4HupAiByUqoumRVmCn+IfcYqNuEhPJGdbpBzta5rPqk8A0JxGrMxzwUJKAJDw==;EndpointSuffix=core.windows.net"""
        self.blob_container = "default"
        self.blob_folder = "voices/"

        # make connections
        self.upload_array_sql_database = SQLController()
        self.upload_array_blob_service = AzureBlobController(self.azure_blob_connection_string, self.blob_container)

    def upload_voice_array(self):
        """
        create an ndarray out of .wav file sample and upload it to database
        :return: bool
        """

        # first: check, if user even exists
        login, _ = self.upload_array_sql_database.get_user_login_and_voice_id(self.user_id)
        voices_list = self.upload_array_blob_service.ls_files(self.blob_folder)
        if self.sound_sample_filename not in voices_list:
            raise FileNotFoundError('File not found in blob container!')

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