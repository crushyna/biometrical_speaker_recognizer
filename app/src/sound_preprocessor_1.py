import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import rfft
from scipy.io import wavfile as wav
from sklearn.preprocessing import minmax_scale, maxabs_scale
from pydub import AudioSegment, effects


class SoundPreprocessor:
    """
    sound preprocessor for Scipy audio analysis and processing
    """

    def __init__(self, sound_file):
        self.scipy_sample_rate, self.scipy_audio = wav.read(SoundPreprocessor.normalize_audio(sound_file))

    @staticmethod
    def normalize_audio(sound_file):
        wavefile = AudioSegment.from_wav(sound_file)
        normalized_wavefile = effects.normalize(wavefile, headroom=0.2)
        # normalized_wavefile = effects.compress_dynamic_range(normalized_wavefile)
        # normalized_wavefile = effects.compress_dynamic_range(wavefile, threshold=-10.0, ratio=2.0, attack=2.5, release=25.0)
        normalized_wavefile.export(sound_file, format='wav')

        return sound_file

    def return_bit_depth(self):
        # quick look at bit depth
        print('Original sample rate:', self.scipy_sample_rate)
        return self.scipy_sample_rate

    def return_min_max(self):
        # quick look at min's and maxes:
        min_max = (np.min(self.scipy_audio), np.max(self.scipy_audio))
        print(f'Original audio file min~max range: {min_max[0]} to {min_max[1]}')
        return min_max

    def convert_stereo_to_mono(self):
        self.scipy_audio = self.scipy_audio.sum(axis=1) / 2
        return self.scipy_audio

    def fourier_transform_audio(self):
        # TODO: volume normalisation?
        self.scipy_audio = rfft(self.scipy_audio)
        # self.scipy_audio = self.scipy_audio[250:22050]
        self.scipy_audio = self.scipy_audio[100:22050]
        return self.scipy_audio

    def minmax_array_numpy(self):
        self.scipy_audio = np.real(self.scipy_audio)
        self.scipy_audio = minmax_scale(self.scipy_audio, feature_range=(0, 10))
        return self.scipy_audio

    @staticmethod
    def create_voice_image_mean_array(list_of_arrays: list):
        """
        pass any number of ndarrays (as list), and return binary image of their average value
        :param list_of_arrays: list
        :return: image_filepath
        """
        print("\nCreating voice image from mean values of arrays")
        try:
            v_arrays_list_avg = sum(list_of_arrays)
            v_arrays_list_avg = np.divide(v_arrays_list_avg, len(list_of_arrays))
            v_arrays_list_avg = np.real(v_arrays_list_avg)
            v_arrays_list_avg = minmax_scale(v_arrays_list_avg, feature_range=(0, 10))

        except Exception as er:
            return er

        return v_arrays_list_avg
