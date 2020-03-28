from io import BytesIO
from ..src.controllers.azure_sql_controller import SQLController
from ..src.sound_preprocessor_1 import SoundPreprocessor
from ..src.controllers.azure_blob_controller import AzureBlobController


def upload_voice_array(user_id: int, sound_sample_filename: str):
    """
    create an ndarray out of .wav file sample and upload it to database
    :param sound_sample_filename: str
    :param user_id: int
    :return: bool
    """
    connection_string = """DefaultEndpointsProtocol=https;AccountName=storageaccountvbioma487;AccountKey=kQjOecdi/KtMStu4iQkxmsAbe4HupAiByUqoumRVmCn+IfcYqNuEhPJGdbpBzta5rPqk8A0JxGrMxzwUJKAJDw==;EndpointSuffix=core.windows.net"""
    blob_container = "default"
    blob_folder = "voices/"
    # local_download_folder = "src/temp_voices/"

    # make connections
    upload_array_sql_database = SQLController()
    upload_array_blob_service = AzureBlobController(connection_string, blob_container)

    # first: check, if user even exists
    login, __ = upload_array_sql_database.get_user_login_and_voice_image_id(user_id)
    voices_list = upload_array_blob_service.ls_files(blob_folder)
    if sound_sample_filename not in voices_list:
        raise FileNotFoundError('File not found in blob container!')

    # get new file from blob
    input_blob_buffer: BytesIO
    _, input_blob_buffer = upload_array_blob_service.download_file_to_bytesbuffer(blob_folder + sound_sample_filename)

    input_sound = SoundPreprocessor(login, input_blob_buffer)
    input_sound.convert_stereo_to_mono()
    input_sound.fourier_transform_audio()
    input_sound.minmax_array_numpy()
    result = upload_array_sql_database.upload_voice_array(user_id, input_sound.scipy_audio)

    input_blob_buffer.close()

    return result
