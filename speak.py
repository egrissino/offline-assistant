'''

Speach and sound effects

'''

import platform
import subprocess
import pyaudio
import wave
import pyttsx3

outputDev = "hw:1,0"

class Speaker:
  def __init__ (self, audio=pyaudio.PyAudio(), samples=2048):
    '''
    PyAudio Speaker
    '''
    self.audio = audio
    self.samples = samples
    self.pltfrm = platform.system ()
    self.engine = pyttsx3.init ()

    self.engine.setProperty ('rate', 175)
    self.engine.setProperty ('volume',1.0)

    voices = self.engine.getProperty ('voices')
    self.engine.setProperty ('voice', voices[1].id)

    if 'Windows' in self.pltfrm:
      output = subprocess.call ('powershell.exe Add-Type -AssemblyName System.Speech', shell=True)
      pass

    # Override to pyaudio
    self.pltfrm = 'Windows'
    self.ready = True
    try:
      self.success ()
    except:
      self.ready = False
      
  def speakText(self, text):
    '''
    '''
    # put report into command
    print(text)

    if not self.ready:
      return

    if 'Linux' in self.pltfrm:
      # Call espeak and buffer in subprocess PIPE
      ps = subprocess.Popen(('espeak', '--stdout', '-ven+f1', '-s205', '-p2', '-g2', f'"{text}"'), stdout=subprocess.PIPE)

      # Send PIPE to aplay to speak through device
      output = subprocess.check_output(('aplay', f'-D{outputDev}', '--rate=22050'), stdin=ps.stdout)
      ps.wait()
    elif 'Darwin' in self.pltfrm:
      pass
    elif 'Windows' in self.pltfrm:
      #output = subprocess.call('(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{}\')'.format(text), shell=True)
      self.engine.say (text)
      self.engine.runAndWait ()
    else:
      print ("Unsupported Platform")

  def success(self):
    '''
    Play Success sound to indicate completed command
    '''
    if not self.ready:
      return
    self.playSoundFile ('./wav/success.wav')

  def error(self):
    '''
    Play error sound to indicate failed command
    '''
    if not self.ready:
      return
    self.playSoundFile ('./wav/error-2.wav')

  def playSoundFile (self, filaname):
    '''
    '''
    if not self.ready:
      return
    if 'Linux' in self.pltfrm:
      output = subprocess.check_output(('aplay', f'-D{outputDev}', filaname))
    elif 'Darwin' in self.pltfrm:
      # Mac
      pass
    elif 'Windows' in self.pltfrm:
      # Windows
      f = wave.open(filaname,"rb")
      stream = self.audio.open(format = self.audio.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)
      #read data  
      data = f.readframes(self.samples)  
        
      #play stream  
      while data:  
          stream.write(data)  
          data = f.readframes(self.samples)  
        
      #stop stream  
      stream.stop_stream()  
      stream.close()
    else:
      # Unsupported?
      pass