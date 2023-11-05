'''

Speach and sound effects

'''

import subprocess

outputDev = "hw:1,0"

def speakText(text):
  '''
  '''
  # put report into command
  print(text)

  # Call espeak and buffer in subprocess PIPE
  ps = subprocess.Popen(('espeak', '--stdout', '-ven+f1', '-s205', '-p2', '-g2', f'"{text}"'), stdout=subprocess.PIPE)

  # Send PIPE to aplay to speak through device
  output = subprocess.check_output(('aplay', f'-D{outputDev}', '--rate=22050'), stdin=ps.stdout)
  ps.wait()


def success():
  '''
  Play Success sound to indicate completed command
  '''
  output = subprocess.check_output(('aplay', f'-D{outputDev}', '/home/pi/offline-speech/wav/success.wav'))


def error():
  '''
  Play error sound to indicate failed command
  '''
  output = subprocess.check_output(('aplay', f'-D{outputDev}', '/home/pi/offline-speech/wav/error-2.wav'))
