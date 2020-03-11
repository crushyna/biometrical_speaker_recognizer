from scipy.io import wavfile as wav
from scipy.fft import rfft
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale, maxabs_scale

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

    def fourier_transform_audio(self):
        # TODO: volume normalisation?
        self.scipy_audio = rfft(self.scipy_audio)
        self.scipy_audio = self.scipy_audio[250:22050]
        return self.scipy_audio

    def minmax_array_numpy(self):
        self.scipy_audio = np.real(self.scipy_audio)
        self.scipy_audio = minmax_scale(self.scipy_audio, feature_range=(0, 10))
        return self.scipy_audio

    def maxabs_array_numpy(self):
        # not used!
        self.scipy_audio = maxabs_scale(self.scipy_audio)
        return self.scipy_audio

    @staticmethod
    def create_voice_image_mean_array(user_login: str, list_of_arrays: list):
        """
        pass any number of ndarrays (as list), and return binary image of their average value
        :param user_login: str
        :param list_of_arrays: list
        :return: bool, image_filepath
        """
        print("\nCreating voice image from mean values of arrays")
        '''
        v_arrays_list_avg = list_of_arrays[0]
        for each_array in list_of_arrays:
            v_arrays_list_avg = v_arrays_list_avg + each_array
        '''
        v_arrays_list_avg = sum(list_of_arrays)

        v_arrays_list_avg = np.divide(v_arrays_list_avg, len(list_of_arrays))
        v_arrays_list_avg = np.real(v_arrays_list_avg)
        v_arrays_list_avg = minmax_scale(v_arrays_list_avg, feature_range=(0, 1))

        return v_arrays_list_avg

    def __old__save_audio_image(self):
        # save current plot:
        from io import BytesIO
        img_buffer_1 = BytesIO()
        plt.figure(figsize=(5, 2), frameon=False)
        # plt.axis('off')
        plt.plot(self.scipy_audio)
        plt.savefig(img_buffer_1, format='png', facecolor='white', transparent=False, bbox_inches='tight',
                    pad_inches=0, dpi=300)

        print(f"img_buffer_1: {img_buffer_1}")
        print(f"img_buffer_1.getvalue(): {img_buffer_1.getvalue()}")
        plt.close()

        return isinstance(img_buffer_1.getvalue(), str), img_buffer_1

    @staticmethod
    def __old__generate_voice_image_from_bytes(input_data: bytes):
        """
        generate voice image from bytes input data
        :param input_data: bytes
        :return: IO.Bytes
        """
        print("\nCreating voice image from bytes")
        from io import BytesIO
        img_buffer_voice_image = BytesIO()

        plt.figure(figsize=(5, 2), frameon=False)
        plt.axis('off')
        plt.plot(input_data)

        plt.savefig(img_buffer_voice_image, format='png', facecolor='white', transparent=False, bbox_inches='tight',
                    pad_inches=0, dpi=300)
        plt.close()

        print(f"img_buffer: {img_buffer_voice_image}")
        print(f"img_buffer.getvalue(): {img_buffer_voice_image.getvalue()}")

        return isinstance(img_buffer_voice_image.getvalue(), str), img_buffer_voice_image

    @staticmethod
    def __old__create_voice_image_array(*args):
        recordings_list = []
        for each_voice in args:
            SoundPreprocessor.convert_stereo_to_mono(each_voice)
            SoundPreprocessor.fourier_transform_audio(each_voice)
            SoundPreprocessor.minmax_array_numpy(each_voice)
            recordings_list.append(each_voice)
