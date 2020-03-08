from src.sound_preprocessor_1 import SoundPreprocessor
from src.image_preprocessor_1 import ImagePreprocessor
from src.controllers.azure_sql_controller import SQLController


def main(user_login: str, sound_sample: object):
    """
    entry point for module, that is simple voice hash comparison
    :return: int
    """
    sql_database = SQLController()

    user_id, voice_image_id = sql_database.get_user_id_and_voice_image_id(user_login)
    voice_image_bytes = sql_database.download_voice_image(voice_image_id)
    _, img_buffer_2 = SoundPreprocessor.generate_voice_image_from_bytes(voice_image_bytes)

    input_sound = SoundPreprocessor(user_login, sound_sample)
    input_sound.convert_stereo_to_mono()
    input_sound.fourier_transform_audio()
    input_sound.minmax_array_numpy()

    # TODO: save image to memory buffer, if OK then upload to Voice Array List
    _, img_buffer_1 = input_sound.save_audio_image()

    image_preprocessor = ImagePreprocessor(img_buffer_1, img_buffer_2)

    result1 = image_preprocessor.compare_dhash()
    result2 = image_preprocessor.compare_whash()

    print(result1)
    print(result2)

    return result1, result2


def upload_voice_array(user_id: int, sound_sample_location: str):
    """
    create an ndarray out of .wav file sample and upload it to database
    :param user_id: int
    :param sound_sample_location: str
    :return: bool
    """
    sql_database = SQLController()
    input_sound = SoundPreprocessor(user_id, sound_sample_location)
    input_sound.convert_stereo_to_mono()
    input_sound.fourier_transform_audio()
    input_sound.minmax_array_numpy()
    result = sql_database.upload_voice_array(user_id, input_sound.scipy_audio)

    return result


def generate_voice_image(user_id: int):
    """
    generates image from average values of voice arrays and upload it up to database as binary Voice Image
    returns 1 if it's done correctly
    :param user_id: int
    :return: bool
    """
    sql_database = SQLController()
    user_login, voice_image_id = sql_database.get_user_login_and_voice_image_id(user_id)
    arrays_list = sql_database.download_user_voice_arrays(user_id)
    result, img_buffer = SoundPreprocessor.create_voice_image_mean_array(user_login, arrays_list)
    result = sql_database.upload_voice_image(voice_image_id, img_buffer.getvalue())

    img_buffer.close()

    return result


def __old__create_voice_image(user_name: str, *args: str):
    """
    joins voices (.wav files) from *args into one .wav file
    :param user_name: str
    :param args: str
    :return: .wav file
    """
    dir_voice_images = 'src/voice_images/'
    import wave
    voice_list = []
    for each_voice_path in args:
        voice_list.append(each_voice_path)

    with wave.open(f'{dir_voice_images}{user_name}.wav', 'wb') as wav_out:
        for wav_path in voice_list:
            with wave.open(wav_path, 'rb') as wav_in:
                if not wav_out.getnframes():
                    wav_out.setparams(wav_in.getparams())
                wav_out.writeframes(wav_in.readframes(wav_in.getnframes()))
