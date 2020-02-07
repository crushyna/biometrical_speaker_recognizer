import librosa
from scipy.io import wavfile as wav
from scipy.fftpack import fft2
import numpy as np
import matplotlib.pyplot as plt
import soundfile


'''
filename = '../UrbanSound Dataset sample/audio/100852-0-0-0.wav'
'''


class SoundPreprocessor:
    """
    sound preprocessor for both Librosa and Scipy audio analysis and processing
    """
    def __init__(self, file_name):
        self.filename = file_name
        self.librosa_audio, self.librosa_sample_rate = librosa.load(file_name)
        self.scipy_sample_rate, self.scipy_audio = wav.read(file_name)

    def return_bit_depth(self):
        # quick look at bit depth
        print('Original sample rate:', self.scipy_sample_rate)
        print('Librosa sample rate:', self.librosa_sample_rate)

    def return_min_max(self):
        # quick look at min's and maxes:
        print('Original audio file min~max range:', np.min(self.scipy_audio), 'to', np.max(self.scipy_audio))
        print('Librosa audio file min~max range:', np.min(self.librosa_audio), 'to', np.max(self.librosa_audio))

    def plot_audio_stereo(self):
        # current audio in stereo:
        plt.figure(figsize=(12, 4))
        plt.plot(self.scipy_audio)
        plt.show()

    def plot_audio_mono(self):
        # Librosa audio with channels merged
        plt.figure(figsize=(12, 4))
        plt.plot(self.librosa_audio)
        plt.show()

