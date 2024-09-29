'''

Pyaudio listener interface for offline assistant

'''

import os
import sys
import threading
from vosk import Model, KaldiRecognizer
import pyaudio
import asyncio
from pydub import AudioSegment, effects

# Input device index (card index)
# 1 - USB1 - pnp mic
# 2 - USB2 - jabralink
# 5 - default
inputDevIdx = 1

#Audio rate for model and input audio channel
default_RATE = 44100

# BUffer Size
default_bufferSize = 2048

class Listener:
    def __init__(self, audio=pyaudio.PyAudio(), deviceIdx=inputDevIdx, rate=default_RATE, buffersz=default_bufferSize):
        '''
        Listener class for microphone and text to speech buffering
        '''
        self.err    = 0
        self.devIdx = deviceIdx
        self.rate   = rate
        self.buffsz = buffersz
        self.text   = ""
        self.audio = audio

        # Kaldi speech recognizer
        self.model      = None
        self.recognizer = None

        # Audio buffering
        self.audioframes = []

    def loadModel(self, model_dir):
        '''
        '''
        # Check for model file or exit
        if not (os.path.exists(model_dir)):
            print("Please download vosk-model-small-en-us-0.15 and unzip folder to this directory")
            exit()

        self.model = Model(model_dir)
        self.recognizer = KaldiRecognizer(self.model, self.rate)


    def checkforText(self):
        '''
        '''
        if len(self.audioframes) <= 1:
            return self.text
        
        audio = AudioSegment (self.audioframes)
        norm_audio = effects.normalize (audio)
        
        if self.recognizer.AcceptWaveform(norm_audio):
            result = self.recognizer.Result()[14:]
            self.text += result[:-3]
            #print(result[:-3])
            #print(self.text)
        else:
            pass

        # prune buffer
        if len(self.text) > 101:
            self.text = self.text[-100:]

        return self.text


    def readData(self):
        '''
        Read data from stream in buffersize
        '''
        try:
            data = self.stream.read(int(self.buffsz), exception_on_overflow=False)
            self.audioframes.append(data)

            # always use the most recent frames
            if len(self.audioframes) > 30:
                self.audioframes = self.audioframes[:-20]

        except Exception as e:
            if self.err == 0:
                print(e)
            self.err += 1

    def startStream(self):
        try:
            # try to launch pyaudio and open device for listening
            self.stream = self.audio.open(format=pyaudio.paInt16,
                 rate=self.rate,
                 channels=1,
                 input=True,
                 frames_per_buffer=self.buffsz,
                 input_device_index=self.devIdx)

            self.stream.start_stream ()
        except Exception as e:
            print(e)
            print("failed to start mic stream! check device settings and run list_audio_devices.py")

    def getText(self):
        return self.text

models = (r'vosk-model-small-en-us-0.15',
          r'vosk-model-en-us-0.22',
          r'vosk-model-en-us-0.42-gigaspeech')

if __name__ == "__main__":

    for arg in sys.argv[1:]:
        if arg[0] == "-":
            if (arg[1] is 'm'):
                try:
                    model_index = arg[2]
                except IndexError:
                    model_index = 0

    if model_index < len(models):
        model_name = models[model_index]

    # Get root dirs setup
    print(os.path.abspath(__file__))
    app_root = os.path.abspath(os.getcwd())

    model_dir = app_root + model_name

    listener = Listener()
    listener.loadModel(model_dir)
    listener.startStream()


    while True:
        result = listener.checkforText()
        if result != "":
            print(result)
