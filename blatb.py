"""
  BackLight According To Brightness
  Set the Raspberry Pi's LCD backlight according to the current ambient brightness, 
  as measured by an attached VEML 7700 light sensor.
  The VEML7700 is attached via the I2C bus.

  robcranfill@gmail.com
"""
import adafruit_veml7700
from rpi_backlight import Backlight
from datetime import datetime
import sys
import time
import math
import board
import busio
 
TEST = False
LOG = True
LOG_FILE_NAME = "blatb-data.log"
BRIGHTNESS_FLOOR = 10 

# exit values
EXIT_VALUE_SENSOR = 1
EXIT_VALUE_LOGGING = 2
EXIT_VALUE_OTHER = 3


# Set the backlight to the indicated percent (0-100), over the given fade time.
def fadeTo(brightPercent, durationSeconds):
    backlight = Backlight()
    with backlight.fade(duration=durationSeconds):
        backlight.brightness = brightPercent


# Return 0-100 based on the algorithm mentioned here:
#   https://hackaday.io/page/6590-ambient-light-sensing
#
def luxToLCDLevel(luxIn):

  if (luxIn <= 0):
    return BRIGHTNESS_FLOOR

  if (luxIn < 1254):
    result = 9.9323 * math.log(luxIn) + 27.059
    result = result / 2 # I found their result too big!
  else:
    result = 100
  if result < BRIGHTNESS_FLOOR:
    result = BRIGHTNESS_FLOOR
  print(f"  luxToLCDLevel: {luxIn:0.2f} -> {result:0.2f}")
  return result


# ------------------ main
#
if __name__ == "__main__":

  # print(f"Arguments count: {len(sys.argv)}")
  # for i, arg in enumerate(sys.argv):
  #     print(f"Argument {i:>6}: {arg}")

  if TEST:
    print("Test mode - NOT setting backlight level")

  try:
    
    try:
      i2c = busio.I2C(board.SCL, board.SDA)
      veml7700 = adafruit_veml7700.VEML7700(i2c)
    except:
      print("Error connecting to VEML7700 sensor; is there one?")
      sys.exit(EXIT_VALUE_SENSOR)

  # prevent this error? (is this the best way?)
  #     File "/home/pi/.local/lib/python3.7/site-packages/adafruit_veml7700.py", line 194, in integration_time_value
  #       return self.integration_time_values[integration_time]
  #   KeyError: 6
    veml7700.light_integration_time = veml7700.ALS_100MS
    
    # This measures the light, in "lux" units.
    lux = veml7700.lux
    print(f"Ambient light: {veml7700.light:0.2f}, Lux: {lux:0.2f}")

    level = int(luxToLCDLevel(lux))
    print(f" -> Set backlight to {level:2.0f}%")

    try:
      logfile = open(LOG_FILE_NAME, "a")
      if TEST:
        logfile.write("Test mode - NOT setting backlight level!\n")
      else:
        if LOG:
          now = datetime.now()
          logfile.write(f"{now}\t{veml7700.light:.0f}\t{lux:.0f}\t{level}\n")
        fadeTo(level, 0.5)
      logfile.close()
    except:
      print("Error logging output!")
      sys.exit(EXIT_VALUE_LOGGING)

  except Exception as e:
    print(f"{e}")
    sys.exit(EXIT_VALUE_OTHER)

  finally:
    pass

