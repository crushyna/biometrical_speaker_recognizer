import unittest
import zipfile
from numpy.core.multiarray import ndarray
from io import BytesIO
from src.sound_preprocessor_1 import SoundPreprocessor
from src.image_preprocessor_1 import ImagePreprocessor


class TestSoundPreprocessor(unittest.TestCase):
    with zipfile.ZipFile('test_voices.zip', 'r') as zip_ref:
        zip_ref.extractall('./audio_files')

    voicefile_1 = "./audio_files/glos1.wav"
    voicefile_2 = "./audio_files/glos2.wav"

    def test_voice_1(self):
        test_sound_1 = SoundPreprocessor(TestSoundPreprocessor.voicefile_1)
        self.assertIsInstance(test_sound_1, object)

    def test_voice_2(self):
        test_sound_2 = SoundPreprocessor(TestSoundPreprocessor.voicefile_2)
        self.assertIsInstance(test_sound_2, object)

    def test_return_bit_depth(self):
        test_sound_1 = SoundPreprocessor(TestSoundPreprocessor.voicefile_1)
        result = test_sound_1.return_bit_depth()
        self.assertIsInstance(result, int)

    def test_fourier_transform_audio(self):
        test_sound_2 = SoundPreprocessor(TestSoundPreprocessor.voicefile_2)
        result = test_sound_2.fourier_transform_audio()
        self.assertIsInstance(result, ndarray)
        self.assertIsInstance(result.shape, tuple)
        self.assertEqual(len(result.shape), 1)

    def test_minmax_array_numpy(self):
        test_sound_1 = SoundPreprocessor(TestSoundPreprocessor.voicefile_1)
        result = test_sound_1.minmax_array_numpy()
        self.assertIsInstance(result, ndarray)
        self.assertIsInstance(result.shape, tuple)
        self.assertEqual(len(result.shape), 1)
        self.assertAlmostEqual(result.min(), 0.0)
        self.assertAlmostEqual(result.max(), 10.0)

    def test_create_voice_image_mean_array(self):
        test_sound_1 = TestSoundPreprocessor.create_test_sound(TestSoundPreprocessor.voicefile_1)
        test_sound_2 = TestSoundPreprocessor.create_test_sound(TestSoundPreprocessor.voicefile_2)
        result = SoundPreprocessor.create_voice_image_mean_array([test_sound_1.scipy_audio, test_sound_2.scipy_audio])
        self.assertIsInstance(result, ndarray)
        self.assertIsInstance(result.shape, tuple)
        self.assertEqual(len(result.shape), 1)
        self.assertAlmostEqual(result.min(), 0.0)
        self.assertAlmostEqual(result.max(), 10.0)

    @staticmethod
    def create_test_sound(imagefile):
        test_sound = SoundPreprocessor(imagefile)
        test_sound.fourier_transform_audio()
        test_sound.minmax_array_numpy()

        return test_sound


class TestImagePreprocessor(unittest.TestCase):

    def test_create_audio_image(self):
        test_sound_1 = TestSoundPreprocessor.create_test_sound(TestSoundPreprocessor.voicefile_1)
        test_sound_2 = TestSoundPreprocessor.create_test_sound(TestSoundPreprocessor.voicefile_2)

        _, result_1 = ImagePreprocessor.generate_audio_image(test_sound_1.scipy_audio)
        _, result_2 = ImagePreprocessor.generate_audio_image(test_sound_2.scipy_audio)
        self.assertIsInstance(result_1, BytesIO)
        self.assertIsInstance(result_2, BytesIO)

    def test_compare_dhash_whash(self):
        test_sound_1 = TestSoundPreprocessor.create_test_sound(TestSoundPreprocessor.voicefile_1)
        test_sound_2 = TestSoundPreprocessor.create_test_sound(TestSoundPreprocessor.voicefile_2)
        _, result_1 = ImagePreprocessor.generate_audio_image(test_sound_1.scipy_audio)
        _, result_2 = ImagePreprocessor.generate_audio_image(test_sound_2.scipy_audio)

        image_preprocessor_instance = ImagePreprocessor(result_1, result_2)
        self.assertIsInstance(image_preprocessor_instance, object)

        hash1 = image_preprocessor_instance.compare_dhash()
        hash2 = image_preprocessor_instance.compare_whash()

        self.assertIsInstance(hash1, int)
        self.assertIsInstance(hash2, int)


if __name__ == '__main__':
    unittest.main()
