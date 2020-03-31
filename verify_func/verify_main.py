from io import BytesIO
from ..src.controllers.azure_sql_controller import SQLController
from ..src.controllers.azure_blob_controller import AzureBlobController
from ..src.image_preprocessor_1 import ImagePreprocessor
from ..src.sound_preprocessor_1 import SoundPreprocessor


class VoiceVerification:

    def __init__(self, user_login: str, sound_sample_filename: str, text_id: int):
        self.name = user_login
        self.user_login = user_login
        self.sound_sample_filename = sound_sample_filename
        self.text_id = text_id
        self.azure_blob_connection_string = """DefaultEndpointsProtocol=https;AccountName=storageaccountvbioma487;AccountKey=kQjOecdi/KtMStu4iQkxmsAbe4HupAiByUqoumRVmCn+IfcYqNuEhPJGdbpBzta5rPqk8A0JxGrMxzwUJKAJDw==;EndpointSuffix=core.windows.net"""
        self.blob_container = "default"
        self.blob_folder = "voices/"

        # make connections
        self.verify_main_sql_database = SQLController()
        self.verify_main_blob_service = AzureBlobController(self.azure_blob_connection_string, self.blob_container)

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