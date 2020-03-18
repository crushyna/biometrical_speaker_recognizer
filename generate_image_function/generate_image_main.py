from ..src.controllers.azure_sql_controller import SQLController
from ..src.sound_preprocessor_1 import SoundPreprocessor


def generate_binary_voice_image(user_id: int):
    """
    generates binary image from average values of voice arrays and upload it up to database
    returns 1 if it's done correctly
    :param user_id: int
    :return: bool
    """
    sql_database = SQLController()
    # first: check, if user even exists
    _, __ = sql_database.get_user_login_and_voice_image_id(user_id)
    sql_database = SQLController()
    user_login, voice_image_id = sql_database.get_user_login_and_voice_image_id(user_id)
    arrays_list = sql_database.download_user_voice_arrays(user_id)
    image_ndarray = SoundPreprocessor.create_voice_image_mean_array(user_login, arrays_list)
    result = sql_database.upload_voice_image(voice_image_id, image_ndarray)

    return result
