import pandas as pd
import os
import librosa
import librosa.display

from src.helpers.wav_file_helper import WavFileHelper
wav_file_helper = WavFileHelper()

metadata = pd.read_csv('../UrbanSound Dataset sample/metadata/UrbanSound8K.csv')
metadata.head()


# collection data
audio_data = []
for index, row in metadata.iterrows():
    file_name = os.path.join(os.path.abspath('/Volumes/Untitled/ML_Data/Urban Sound/UrbanSound8K/audio/'),
                             'fold' + str(row["fold"]) + '/', str(row["slice_file_name"]))
    data = wav_file_helper.read_file_properties(file_name)
    audio_data.append(data)

# Convert into a Panda dataframe
audio_df = pd.DataFrame(audio_data, columns=['num_channels', 'sample_rate', 'bit_depth'])

