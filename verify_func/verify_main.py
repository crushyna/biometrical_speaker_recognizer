from ..src.controllers.azure_sql_controller import SQLController
from ..src.image_preprocessor_1 import ImagePreprocessor
from ..src.sound_preprocessor_1 import SoundPreprocessor


def verify_voice(user_login: str, sound_sample: object):
    """
    entry point for module, that is simple voice hash comparison
    :return: int
    """
    verify_main_sql_database = SQLController()

    # get stored image
    user_id, voice_image_id = verify_main_sql_database.get_user_id_and_voice_image_id(user_login)

    voice_image_bytes = verify_main_sql_database.download_voice_image(voice_image_id)
    _, stored_image_buffer = ImagePreprocessor.generate_audio_image(voice_image_bytes, 'stored_image')

    # process input image
    input_sound = SoundPreprocessor(user_login, sound_sample)
    input_sound.convert_stereo_to_mono()
    input_sound.fourier_transform_audio()
    input_sound.minmax_array_numpy()

    _, input_image_buffer = ImagePreprocessor.generate_audio_image(input_sound.scipy_audio, 'input_image')

    # compare images
    image_preprocessor = ImagePreprocessor(input_image_buffer, stored_image_buffer)

    result1 = image_preprocessor.compare_dhash()
    result2 = image_preprocessor.compare_whash()

    print(f'DHASH Difference: {result1}')
    print(f'WHASH Difference: {result2}')

    # if result (some operation) then:
    # upload result = upload_voice_array(user_id, sound_sample)

    return result1, result2
