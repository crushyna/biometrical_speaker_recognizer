import unittest
from src.image_preprocessor_1 import ImagePreprocessor
from src.sound_preprocessor_1 import SoundPreprocessor
from numpy import asarray


class ImagePreprocessorTest(unittest.TestCase):
    test_image_1 = 'src/sound_images/crushyna.png'
    test_image_2 = 'src/sound_images/paulina.png'

    # TODO: it analyses test_images as STRINGS instead of objects, need to fix it

    test_imgpreprocessor_class = ImagePreprocessor(test_image_1, test_image_2)

    def test_compare_dhash(self):
        self.assertIsInstance(self.test_imgpreprocessor_class.compare_dhash(), int)

    def test_compare_whash(self):
        self.assertIsInstance(self.test_imgpreprocessor_class.compare_whash(), int)

    def test_generate_audio_image(self):
        test_login = 'test_login_imgpreprocessor'
        sound_sample = 'src/test_sounds/clint_eastwood_1.wav'

        input_sound = SoundPreprocessor(test_login, sound_sample)
        input_sound.convert_stereo_to_mono()
        input_sound.fourier_transform_audio()
        sound_array = input_sound.minmax_array_numpy()

        self.assertIsInstance(self.ImagePreprocessor.generate_audio_image(sound_array, 'test_buffer'), bool, str)


if __name__ == '__main__':
    unittest.main()
