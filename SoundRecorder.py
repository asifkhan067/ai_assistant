import pickle
import librosa
import numpy
import pyaudio
import wave
import SpeechEmotionDetection
from scipy.io import wavfile
from SpeechEmotionDetection import extract_feature

with open('speech_emotion_detection_model.pkl', 'rb') as file:
    model = pickle.load(file)
model


def record():
    chunk = 1024
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 44100
    recording_time = 10
    file_name = "output.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=audio_format, channels=channels,
                    rate=rate, input=True, frames_per_buffer=chunk)
    # print("* recording")
    frames = []

    for i in range(0, int(rate / chunk * recording_time)):
        data = stream.read(chunk)
        frames.append(data)
        # print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()
    write_file = wave.open(file_name, 'wb')
    write_file.setnchannels(channels)
    write_file.setsampwidth(p.get_sample_size(audio_format))
    write_file.setframerate(rate)
    write_file.writeframes(b''.join(frames))
    write_file.close()


def guess_emotion():
    record()
    file = 'output.wav'
    signal, rate = librosa.load(file, sr=16000)
    mask = SpeechEmotionDetection.envelope(signal, rate, 0.0005)
    new_file = "clean_"+file
    wavfile.write(filename=new_file, rate=rate, data=signal[mask])
    ans = []
    new_feature = extract_feature(new_file, mfcc=True, chroma=True, mel=True)
    ans.append(new_feature)
    ans = numpy.array(ans)
    prediction = model.predict(ans)
    return prediction
