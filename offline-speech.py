from vosk import Model, KaldiRecognizer
import pyaudio

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
inputDevIdx = 0

#Audio rate for model and input audio channel
RATE = 44100

# BUffer Size
bufferSize = 22050

import kasa
class Devices:
    def __init__ (self, devs={}):
        '''
        Devices Lsting and control from kasa
        '''
        self.devices = devs
        self.loop = asyncio.get_event_loop ()
        self.updateDeviceList ()

        print (self.devices)

    def turnOn (self, dev_name):
        '''
        Turn device on
        '''
        dev_name = dev_name.replace (' ','')
        print (f'Turing on : {dev_name}')
        for dev in self.devices:
            if dev_name in self.devices[dev].alias.lower():
                try:
                    self.loop.run_until_complete (self.devices[dev].turn_on())
                    self.loop.run_until_complete (self.devices[dev].update())
                    return True
                except Exception as e:
                    print (e)
        return False

    def turnOff (self, dev_name):
        '''
        Turn device on
        '''

        dev_name = dev_name.replace (' ','')
        print (f'Turing off : {dev_name}')
        for dev in self.devices:
            if dev_name in self.devices[dev].alias.lower():
                try:
                    self.loop.run_until_complete (self.devices[dev].turn_off())
                    self.loop.run_until_complete (self.devices[dev].update())
                    return True
                except Exception as e:
                    print (e)
        return False
    
    def updateDeviceList (self):
        '''
        Update device list from kasa
        '''
        self.devices = self.loop.run_until_complete (kasa.Discover.discover())

class Assistant:
    def __init__(self, speaker, devices=Devices(), local='Chattanooga, Tennessee', name="assistant"):
        '''
        Offline Assistant
        '''
        self.devices = devices
        self.speaker = speaker
        self.defaultArea = local
        self.name = name

        self.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def processCmd(self, text):
        '''
        Process voice command
        '''
        command = text.replace(self.name, '')
        print(command)

        if 'turn' in command:
            # check for turn on/off commands
            if 'turn on' in command:
                dev_name = command.replace('turn on ', '')
                dev_name = dev_name.replace('the ', '')
                if (self.devices.turnOn(dev_name)):
                    self.speaker.success()
                else:
                    self.speaker.error()
                return
            
            elif 'turn off' in command:
                dev_name = command.replace('turn off ', '')
                dev_name = dev_name.replace('the ', '')
                if ( self.devices.turnOff(dev_name)):
                    self.speaker.success()
                else:
                    self.speaker.error()
                return

        if ('what' in command):
            # Answer querys
            query = command.replace('what is ', '')
            query = query.replace("what's ", '')
            query = query.replace("the ", '')

            if 'weather' in query:
                # Get wheather in location if avilable
                area = query.replace ('weather','')
                if 'in' in area:
                    area = area.replace ('in','')
                else:
                    area = self.defaultArea
                report = weather.getCurrentWeather (area)
                self.speaker.speakText (report)
            
            if 'time' in query:
                # Get time now
                now = time.localtime ()
                if now.tm_min == 0:
                    minutes = " o-clock"
                elif now.tm_min < 10:
                    minutes = " o {}".format(now.tm_min)
                else:
                    minutes = str(now.tm_min)

                hours = ((now.tm_hour+12) % 12)
                if hours == 0:
                    hours = 12

                self.speaker.speakText ("The time is {} {}".format(hours, minutes) )

            if 'date' in query:
                # get the date
                today = time.localtime ()
                self.speaker.speakText ("The date is {} {} {}".format(today.tm_mon, today.tm_mday, today.tm_year))

            if 'day' in query:
                # get the date
                today = time.localtime ()
                self.speaker.speakText ("Today is {}".format(self.weekdays[today.tm_wday]))

            if 'moon' in query:
                # get moon data
                report = weather.readWeather (self.defaultArea)
                self.speak ("")

        if 'connect' in command:
            # Try blue tooth conenction
            self.speaker.success()
            return

MAX_ERRS = 100
err = 0

if __name__ == "__main__":
    print(os.path.abspath(__file__))
    # Open Voice recognizer
    app_root = os.path.abspath(os.getcwd())
    # model_dir = app_root + r"/vosk-model-small-en-us-0.15"
    model_dir = app_root + r"/vosk-model-en-us-0.22-lgraph"
    model = Model(model_dir)
    recognizer = KaldiRecognizer(model, RATE)

    # Open Audio Control
    audio = pyaudio.PyAudio()
    devs = Devices ()
    speaker = speak.Speaker (audio)
    assistant = Assistant (speaker, name="home")

    # Open Mic Stream
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=bufferSize ,
                        input_device_index=inputDevIdx)
    stream.start_stream()

    # Main loop
    text = ""
    while err < MAX_ERRS:
        try:
            err = 0
            data = stream.read(bufferSize, exception_on_overflow=False)
        
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()[14:]
                text += result[:-3]
                #print(len(result))
                print(text)

                if assistant.name in text:
                    #stream.stop_stream()
                    #print(text)
                    assistant.processCmd(text[text.index(assistant.name):])
                    text = ""
                    #stream.start_stream()
                else:
                    text += " "
                    if len(text) > 41:
                        text = text[-40:]
                    
        except Exception as e:
            if err == 0:
                print(e)
            err += 1
            break
        
