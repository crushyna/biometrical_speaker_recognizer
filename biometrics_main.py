from src.sound_preprocessor_1 import SoundPreprocessor
from src.image_preprocessor_1 import ImagePreprocessor
from src.controllers.azure_sql_controller import SQLController

# test_login = 'crushyna'
# test_sound = 'src/test_sounds/owsiak_1a.wav'

test_voice_image = 'src/sound_images/inez_image.png'


def main(user_login: str, sound_sample: object):
    """
    entry point for module
    :return: int
    """
    sql_database = SQLController()

    user_id, voice_image_id = sql_database.check_if_user_exist(user_login)
    voice_image_array = sql_database.check_if_voice_image_exists(voice_image_id)

    print(type(voice_image_array))

    input_sound = SoundPreprocessor(user_login, sound_sample)
    input_sound.convert_stereo_to_mono()
    input_sound.fourier_transform_audio()
    input_sound.minmax_array_numpy()
    input_sound.save_audio_image()

    input_image = ImagePreprocessor(f'src/sound_images/{user_login}', test_voice_image)
    result = input_image.compare_dhash()
    print(result)
    return result


def upload_voice_array(user_id: int, sound_sample_location: str):
    # TODO: uploads as 71 len string. Try with nvarchar(MAX) and varbinary(MAX)
    sql_database = SQLController()
    input_sound = SoundPreprocessor(user_id, sound_sample_location)
    input_sound.convert_stereo_to_mono()
    input_sound.fourier_transform_audio()
    input_sound.minmax_array_numpy()
    sql_database.upload_voice_array(user_id, input_sound.scipy_audio)


def create_voice_image(user_name: str, *args: str):
    """
    joins voices (.wav files) from *args into one .wav file
    :param user_name: str
    :param args: str
    :return: .wav file
    """

    # TODO: strange things happen when you create image from joined .wav files, need to investigate

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
