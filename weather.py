import python_weather

import asyncio
import os
import speak

async def getweather(location):
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
    # fetch a weather forecast from a city
    weather = await client.get(location)
    
    # returns the current day's forecast temperature (int)
    print(weather.current.temperature)

    # get things like preessure, percip, humidity etc
    #weather.current.pressure
    
    # get the weather forecast for a few days
    for forecast in weather.forecasts:
      print(forecast)
      pass

      # hourly forecasts
      for hourly in forecast.hourly:
        print(f' --> {hourly!r}')
        pass

    return weather

def getCurrentWeather (location):
  '''
  Read weather report for a location
  '''
  weather = asyncio.run(getweather(location))
  # Create Textual weather report
  report = f"It's currently a temp of {weather.current.temperature} and {weather.current.description} in {weather.nearest_area.name} {weather.nearest_area.region}"
  return report

def getForecast (location):
  '''
  Read weather report for a location
  '''
  weather = asyncio.run(getweather(location))
  # Create Textual weather report
  report = f"It's currently a temp of {weather.current.temperature} and {weather.current.description} in {weather.nearest_area.name} {weather.nearest_area.region}"
  return report

'''
# put report into command
#command[3].replace('<report>', report)
print(report)
# Call espeak and buffer in subprocess PIPE
ps = subprocess.Popen(('espeak', '--stdout', '-ven+f1', '-s205', '-p2', '-g2', f'"{report}"'), stdout=subprocess.PIPE)

# Send PIPE to aplay to speak through device
output = subprocess.check_output(('aplay', '-Dhw:1,0', '--rate=22050'), stdin=ps.stdout)
ps.wait()
'''

'''
engine = pyttsx3.init()
#espeak -ven+f2 -k5 -s150 -a 100 -g10

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
#print (rate)                        #printing current voice rate
engine.setProperty('rate', 135)     # setting up new voice rate

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
#engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

engine.say(report)
engine.run()
'''

if __name__ == '__main__':
  
  location = 'Chattanooga'

  readWeather(location)
  
