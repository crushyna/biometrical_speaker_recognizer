from ..src.controllers.azure_sql_controller import SQLController
from ..src.controllers.azure_blob_controller import AzureBlobController
from ..src.image_preprocessor_1 import ImagePreprocessor
from ..src.sound_preprocessor_1 import SoundPreprocessor


def verify_voice(user_login: str, sound_sample_filename: str):
    """
    entry point for module, that is simple voice hash comparison
    :return: bool
    """
    connection_string = """DefaultEndpointsProtocol=https;AccountName=storageaccountvbioma487;AccountKey=kQjOecdi/KtMStu4iQkxmsAbe4HupAiByUqoumRVmCn+IfcYqNuEhPJGdbpBzta5rPqk8A0JxGrMxzwUJKAJDw==;EndpointSuffix=core.windows.net"""
    blob_container = "default"
    blob_folder = "voices/"
    local_download_folder = "src/temp_voices/"

    # make connections
    verify_main_sql_database = SQLController()
    verify_main_blob_service = AzureBlobController(connection_string, blob_container)

    # check if requested data exists
    user_id, voice_image_id = verify_main_sql_database.get_user_id_and_voice_image_id(user_login)
    voices_list = verify_main_blob_service.ls_files(blob_folder)
    if sound_sample_filename not in voices_list:
        raise FileNotFoundError('File not found in blob container!')

    # get stored image into buffer
    voice_image_bytes = verify_main_sql_database.download_voice_image(voice_image_id)
    _, stored_image_buffer = ImagePreprocessor.generate_audio_image(voice_image_bytes, "stored_image")

    # get input file from blob
    verify_main_blob_service.download(blob_folder + sound_sample_filename, local_download_folder)
    downloaded_file = f"{local_download_folder}{sound_sample_filename}"

    # process input image
    input_sound = SoundPreprocessor(user_login, downloaded_file)
    input_sound.convert_stereo_to_mono()
    input_sound.fourier_transform_audio()
    input_sound.minmax_array_numpy()

    # get input image into buffer
    _, input_image_buffer = ImagePreprocessor.generate_audio_image(input_sound.scipy_audio, "input_image")

    # compare images
    image_preprocessor = ImagePreprocessor(input_image_buffer, stored_image_buffer)

    result_dhash = image_preprocessor.compare_dhash()
    result_whash = image_preprocessor.compare_whash()

    # print(f"DHASH Difference: {result_dhash}")
    # print(f"WHASH Difference: {result_whash}")

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
