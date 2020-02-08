from scipy.io import wavfile as wav
from scipy.fft import rfft2, rfftn, rfft
from scipy.signal import correlate
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale, maxabs_scale
from sklearn import metrics

'''
filename = '../UrbanSound Dataset sample/audio/100852-0-0-0.wav'
'''

test_filename_1 = 'src/test_sounds/owsiak_1a.wav'
test_filename_2 = 'src/test_sounds/owsiak_1b.wav'
test_filename_3 = 'src/test_sounds/owsiak_2a.wav'
test_filename_4 = 'src/test_sounds/owsiak_2b.wav'


class SoundPreprocessor:
    """
    sound preprocessor for Scipy audio analysis and processing
    """

    def __init__(self, file_name):
        self.filename = file_name
        self.scipy_sample_rate, self.scipy_audio = wav.read(file_name)

    def return_bit_depth(self):
        # quick look at bit depth
        print('Original sample rate:', self.scipy_sample_rate)

    def return_min_max(self):
        # quick look at min's and maxes:
        print('Original audio file min~max range:', np.min(self.scipy_audio), 'to', np.max(self.scipy_audio))

    def convert_stereo_to_mono(self):
        self.scipy_audio = self.scipy_audio.sum(axis=1) / 2
        return self.scipy_audio

    def plot_audio(self):
        # current audio plot:
        plt.figure(figsize=(12, 4))
        plt.hist2d(self.scipy_audio, bins=256, log=True)
        plt.show()

    def fourier_transform_audio(self):
        # self.scipy_audio = rfft(self.scipy_audio)
        self.scipy_audio = rfft(self.scipy_audio)
        self.scipy_audio = self.scipy_audio[500:22250]
        return self.scipy_audio

    def minmax_array_numpy(self):
        self.scipy_audio = np.real(self.scipy_audio)
        self.scipy_audio = minmax_scale(self.scipy_audio, feature_range=(0, 2))
        return self.scipy_audio

    def maxabs_array_numpy(self):
        self.scipy_audio = maxabs_scale(self.scipy_audio)
        return self.scipy_audio

    @staticmethod
    def error_rate(sound_array_1, sound_array_2):
        # TODO: a lot of work to do here
        '''
        err = np.sum((self.scipy_audio - self.scipy_audio) ** 2)
        err /= float(self.scipy_audio[0] * self.scipy_audio[1])
        '''
        mean_absolute = metrics.mean_absolute_error(sound_array_1, sound_array_2)
        mean_squared = metrics.mean_squared_error(sound_array_1, sound_array_2)
        root_mean_squared = np.sqrt(metrics.mean_squared_error(sound_array_1, sound_array_2))
        correlation = np.mean(correlate(sound_array_1, sound_array_2))
        return mean_absolute, mean_squared, root_mean_squared, correlation
