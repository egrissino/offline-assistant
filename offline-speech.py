from vosk import Model, KaldiRecognizer
import pyaudio
import kasa
import asyncio
import time
import os
import weather
import speak

# Input device index (card index)
# 0 - HDMI
# 1 - phones
# 2 - USB1 - pnp mic
# 3 - USB2 - jabralink
inputDevIdx = 2

#Audio rate for model and input audio channel
RATE = 44100

# BUffer Size
bufferSize = 22050

def turnOn(dev_name):
    '''
    Turn device on
    '''
    dev_name = dev_name.replace(' ','')
    print(f'Turing on : {dev_name}')
    for dev in devices:
        if dev_name in devices[dev].alias.lower():
            print(dev_name)
            print(devices[dev].alias)
            try:
                asyncio.run(devices[dev].turn_on())
                #time.sleep(1)
            except:
                pass

def turnOff(dev_name):
    '''
    Turn device on
    '''
    attempted = 0
    completed = 0
    dev_name = dev_name.replace(' ','')
    print(f'Turing off : {dev_name}')
    for dev in devices:
        if dev_name in devices[dev].alias.lower():
            #print(dev_name)
            attempted += 1
            print(devices[dev].alias)
            try:
                asyncio.run(devices[dev].turn_off())
                #time.sleep(1)
            except Exception as e:
                print(e)
                completed += 1
                #speak.error()
                pass

    return completed

def processCmd(text):
    '''
    Process voice command
    '''

    command = text.replace('alexa', '')
    print(command)

    if 'turn' in command:
        # check for turn on/off commands
        if 'turn on' in command:
            dev_name = command.replace('turn on ', '')
            dev_name = dev_name.replace('the ', '')
            turnOn(dev_name)
            speak.success()
            return
        elif 'turn off' in command:
            dev_name = command.replace('turn off ', '')
            dev_name = dev_name.replace('the ', '')
            turnOff(dev_name)
            speak.success()
            return

    if ('what is ' in command) or ("what's " in command):
        # Answer querys
        query = command.replace('what is ', '')
        query = query.replace("what's ", '')
        query = query.replace("the ", '')

        if 'weather in ' in query:
            # Get wheather in location if avilable
            area = query.replace('weather in ','')
            weather.readWeather(area)
            speak.success()
            return

    if 'connect' in command:
        # Try blue tooth conenction
        speak.success()
        return

    print(command)
    speak.error()

devices = {}
def updateDeviceList():
    '''
    Update device list from kasa
    '''
    global devices
    devices = asyncio.run(kasa.Discover.discover())

MAX_ERRS = 100
err = 0

if __name__ == "__main__":
    
    updateDeviceList()

    print(os.path.abspath(__file__))
    app_root = os.path.abspath(os.getcwd())
    model_dir = app_root + r"/vosk-model-small-en-us-0.15"
    model = Model(model_dir)
    recognizer = KaldiRecognizer(model, RATE)

    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16,
 channels=1,
 rate=RATE,
 input=True,
 frames_per_buffer=bufferSize ,
 input_device_index=inputDevIdx)
    stream.start_stream()

    text = ""
    while err < MAX_ERRS:
        try:
            err = 0
            data = stream.read(bufferSize, exception_on_overflow=False)
        
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()[14:]
                text += result[:-3]
                #print(len(result))
                #print(text)

                if "alexa" in text:
                    #stream.stop_stream()
                    #print(text)
                    processCmd(text[text.index('alexa'):])
                    text = ""
                    #stream.start_stream()
                else:
                    if len(text) > 41:
                        text = text[-40:]
                    
        except Exception as e:
            if err == 0:
                print(e)
            err += 1
            break
        
