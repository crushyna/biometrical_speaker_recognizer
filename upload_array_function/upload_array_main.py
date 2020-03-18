from ..src.controllers.azure_sql_controller import SQLController
from ..src.sound_preprocessor_1 import SoundPreprocessor


def upload_voice_array(user_id: int, sound_sample_location: str):
    """
    create an ndarray out of .wav file sample and upload it to database
    :param user_id: int
    :param sound_sample_location: str
    :return: bool
    """
    sql_database = SQLController()
    # first: check, if user even exists
    _, __ = sql_database.get_user_login_and_voice_image_id(user_id)
    input_sound = SoundPreprocessor(user_id, sound_sample_location)
    input_sound.convert_stereo_to_mono()
    input_sound.fourier_transform_audio()
    input_sound.minmax_array_numpy()
    result = sql_database.upload_voice_array(user_id, input_sound.scipy_audio)

    return result
