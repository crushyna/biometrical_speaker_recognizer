from scipy.io import wavfile as wav
from scipy.fft import rfft
from scipy.signal import correlate
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale, maxabs_scale
from sklearn import metrics
from os.path import exists

'''
filename = '../UrbanSound Dataset sample/audio/100852-0-0-0.wav'
'''

# for test purposes only
test_filename_1 = 'src/test_sounds/owsiak_1a.wav'
test_filename_2 = 'src/test_sounds/owsiak_1b.wav'
test_filename_3 = 'src/test_sounds/owsiak_2a.wav'
test_filename_4 = 'src/test_sounds/owsiak_2b.wav'
test_filename_5 = 'src/test_sounds/Inez_1a.wav'
test_filename_6 = 'src/test_sounds/Inez_1b.wav'
test_filename_7 = 'src/test_sounds/Krzysztof_1a.wav'
test_filename_8 = 'src/test_sounds/Krzysztof_1b.wav'
test_filename_9 = 'src/test_sounds/Maciej_1a.wav'
test_filename_10 = 'src/test_sounds/Maciej_1b.wav'
test_filename_11 = 'src/test_sounds/Wojtek_1a.wav'
test_filename_12 = 'src/test_sounds/Wojtek_1b.wav'


class SoundPreprocessor:
    """
    sound preprocessor for Scipy audio analysis and processing
    """

    def __init__(self, object_name, file_name):
        self.name = object_name
        self.filename = file_name
        self.scipy_sample_rate, self.scipy_audio = wav.read(file_name)

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

    def plot_audio(self):
        # current audio plot:
        plt.figure(figsize=(5, 2), frameon=False)
        plt.axis('off')
        plt.plot(self.scipy_audio)

    def save_audio_image(self):
        # save current plot:
        plt.figure(figsize=(5, 2), frameon=False)
        plt.axis('off')
        plt.plot(self.scipy_audio)
        plt.savefig(f'src/sound_images/{self.name}.png', facecolor='white', transparent=False, bbox_inches='tight',
                    pad_inches=0, dpi=300)
        plt.close()

        return exists(f'src/sound_images/{self.name}.png')

    def fourier_transform_audio(self):
        # TODO: volume normalisation?
        # self.scipy_audio = rfft(self.scipy_audio)
        self.scipy_audio = rfft(self.scipy_audio)
        self.scipy_audio = self.scipy_audio[250:22050]
        return self.scipy_audio

    def minmax_array_numpy(self):
        self.scipy_audio = np.real(self.scipy_audio)
        self.scipy_audio = minmax_scale(self.scipy_audio, feature_range=(0, 1))
        return self.scipy_audio

    def maxabs_array_numpy(self):
        self.scipy_audio = maxabs_scale(self.scipy_audio)
        return self.scipy_audio

    @staticmethod
    def error_rate(sound_array_1, sound_array_2):
        # TODO: a lot of work to do here, unless there's image analysis option
        '''
        err = np.sum((self.scipy_audio - self.scipy_audio) ** 2)
        err /= float(self.scipy_audio[0] * self.scipy_audio[1])
        '''
        mean_absolute = metrics.mean_absolute_error(sound_array_1, sound_array_2)
        mean_squared = metrics.mean_squared_error(sound_array_1, sound_array_2)
        root_mean_squared = np.sqrt(metrics.mean_squared_error(sound_array_1, sound_array_2))
        correlation = np.mean(correlate(sound_array_1, sound_array_2))
        return mean_absolute, mean_squared, root_mean_squared, correlation

    @staticmethod
    def create_voice_image_array(*args):
        recordings_list = []
        for each_voice in args:
            SoundPreprocessor.convert_stereo_to_mono(each_voice)
            SoundPreprocessor.fourier_transform_audio(each_voice)
            SoundPreprocessor.minmax_array_numpy(each_voice)
            recordings_list.append(each_voice)

    @staticmethod
    def create_voice_image_mean_array(*args):
        """
        pass any number or ndarrays, and return image of their average value
        :param args: ndarray
        :return: bool
        """
        # TODO: this might need some code separation into smaller piecies

        v_arrays_list = []
        for each_input_array in args:
            v_arrays_list.append(each_input_array)

        v_arrays_list_avg = v_arrays_list[0]
        for each_array in v_arrays_list:
            v_arrays_list_avg = v_arrays_list_avg + each_array

        print(len(v_arrays_list))
        v_arrays_list_avg = np.divide(v_arrays_list_avg, v_arrays_list.__len__())
        v_arrays_list_avg = np.real(v_arrays_list_avg)
        v_arrays_list_avg = minmax_scale(v_arrays_list_avg, feature_range=(0, 1))

        plt.figure(figsize=(5, 2), frameon=False)
        plt.axis('off')
        plt.plot(v_arrays_list_avg)
        plt.savefig(f'src/sound_images/image.png', facecolor='white', transparent=False, bbox_inches='tight',
                    pad_inches=0, dpi=300)
        plt.close()

        return exists(f'src/sound_images/image.png')
