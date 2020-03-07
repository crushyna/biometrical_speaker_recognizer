import unittest
from src.sound_preprocessor_1 import SoundPreprocessor
from numpy import ndarray


class SoundPreprocessorTest(unittest.TestCase):
    """
    simple tests for sound preprocessor
    """

    test_instance = 'test_sound_1'
    test_voice_sample = 'test_sounds/clint_eastwood_1.wav'
    test_sound_1 = SoundPreprocessor(test_instance, test_voice_sample)

    def test_return_bit_depth(self):
        self.assertIsInstance(self.test_sound_1.return_bit_depth(), int)

    def test_return_min_max(self):
        self.assertIsInstance(self.test_sound_1.return_min_max(), tuple)

    def test_convert_stereo_to_mono(self):
        self.assertIsInstance(self.test_sound_1.convert_stereo_to_mono(), ndarray)

    def test_save_audio_image(self):
        # TODO: fails every time, fix it somehow. Maybe split plot and save?
        self.assertTrue(self.test_sound_1.save_audio_image())

    def test_fourier_transform_audio(self):
        self.assertEqual(self.test_sound_1.scipy_audio.shape.__len__(), 1)


if __name__ == '__main__':
    unittest.main()
