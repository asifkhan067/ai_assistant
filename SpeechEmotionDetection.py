import librosa
import soundfile
import os
import glob
import numpy as np
from tqdm import tqdm
from scipy.io import wavfile
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import pickle
import pandas

emotions = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

observed_emotions = ['calm', 'happy', 'fearful', 'disgust', 'angry']


def extract_feature(file_name, mfcc, chroma, mel):
    with soundfile.SoundFile(file_name) as sound_file:
        x = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        if chroma:
            stft = np.abs(librosa.stft(x))
        result = np.array([])
        if mfcc:
            mfccs = np.mean(librosa.feature.mfcc(
                y=x, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(
                S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(
                x, sr=sample_rate).T, axis=0)
            result = np.hstack((result, mel))
    return result


def envelope(y, rate, threshold):
    mask = []
    y = pandas.Series(y).apply(np.abs)
    y_mean = y.rolling(window=int(rate / 10),
                       min_periods=1, center=True).mean()
    for mean in y_mean:
        if mean > threshold:
            mask.append(True)
        else:
            mask.append(False)
    return mask


def cleaning_files():
    for file in tqdm(glob.glob("speech_test\\Actor_*\\*.wav")):
        file_name = os.path.basename(file)
        signal, rate = librosa.load(file, sr=16000)
        mask = envelope(signal, rate, 0.0005)
        wavfile.write(filename=r'Clean_test\\' + str(file_name),
                      rate=rate, data=signal[mask])


def load_data(test_size=0.2):
    cleaning_files()
    x, y = [], []
    for file in glob.glob("Clean_test\\*.wav"):
        file_name = os.path.basename(file)
        emotion = emotions[file_name.split("-")[2]]
        if emotion not in observed_emotions:
            continue
        feature = extract_feature(file, mfcc=True, chroma=True, mel=True)
        x.append(feature)
        y.append(emotion)
    return train_test_split(np.array(x), y, test_size=test_size, random_state=9)


def main():
    x_train, x_test, y_train, y_test = load_data(test_size=0.25)
    model = MLPClassifier(alpha=0.01, batch_size=256, epsilon=1e-08, hidden_layer_sizes=(300,),
                          learning_rate='adaptive',
                          max_iter=500)
    model.fit(x_train, y_train)
    file_name = "speech_emotions_detection_model.pkl"
    with open(file_name, 'wb') as file:
        pickle.dump(model, file)


# main()
