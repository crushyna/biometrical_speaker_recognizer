from src.sound_preprocessor_1 import SoundPreprocessor
from src.image_preprocessor_1 import ImagePreprocessor

# test_login = 'crushyna'
# test_sound = 'src/test_sounds/owsiak_1a.wav'

test_voice_image = 'src/sound_images/sound2.png'


def main(user_login: str, sound_sample: object):
    """
    entry point for module
    :return: int
    """
    input_sound = SoundPreprocessor(user_login, sound_sample)
    input_sound.convert_stereo_to_mono()
    input_sound.fourier_transform_audio()
    input_sound.minmax_array_numpy()
    input_sound.save_audio_image()

    input_image = ImagePreprocessor(f'src/sound_images/{user_login}', test_voice_image)
    result = input_image.compare_dhash()
    print(result)
    return result
