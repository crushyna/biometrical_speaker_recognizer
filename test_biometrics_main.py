import unittest
from biometrics_main import main

test_login = 'crushyna'
test_sound = 'src/test_sounds/owsiak_1a.wav'


class BiometricsMainTest(unittest.TestCase):
    """
    simple test for module entry point
    """
    def test_result(self):
        self.assertIsInstance(main(test_login, test_sound), int)


if __name__ == '__main__':
    unittest.main()
