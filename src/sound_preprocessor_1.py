from scipy.io import wavfile as wav
from scipy.fftpack import fft, rfft
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale, maxabs_scale
from sklearn import metrics


'''
filename = '../UrbanSound Dataset sample/audio/100852-0-0-0.wav'
'''

test_filename = 'src/test_sounds/clint_eastwood_1.wav'


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
        plt.plot(self.scipy_audio)
        plt.show()

    def fourier_transform_audio(self):
        self.scipy_audio = rfft(self.scipy_audio)
        self.scipy_audio = self.scipy_audio[:len(self.scipy_audio)//2]
        return self.scipy_audio

    def minmax_array_numpy(self):
        self.scipy_audio = minmax_scale(self.scipy_audio)
        return self.scipy_audio

    def maxabs_array_numpy(self):
        self.scipy_audio = maxabs_scale(self.scipy_audio)
        return self.scipy_audio

    def mean_squared_error(self):
        err = np.sum((self.scipy_audio - self.scipy_audio) ** 2)
        err /= float(self.scipy_audio[0] * self.scipy_audio[1])
        return err