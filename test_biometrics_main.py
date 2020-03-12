import unittest

from biometrics_main import verify_voice, upload_voice_array

test_login = 'crushyna'
test_sound = 'src/test_sounds/owsiak_1a.wav'
test_id = 6


class BiometricsMainTest(unittest.TestCase):
    """
    simple test for module entry point
    """

    def test_verify_voice(self):
        self.assertIsInstance(verify_voice(test_login, test_sound), tuple)

    def test_upload_voice_array(self):
        self.assertIsInstance(upload_voice_array(test_id, test_sound), int)

    # maybe later?
    '''
    def test_generate_binary_voice_image(self):
        with self.assertRaises(pyodbc.IntegrityError) as context:
            generate_binary_voice_image(6)

        self.assertTrue('Proper response' in context.exception)
    '''


if __name__ == '__main__':
    unittest.main()
