"""
  BackLight According To Brightness
  Set the Raspberry Pi's LCD backlight according to the current ambient brightness, 
  as measured by an attached VEML 7700 light sensor.
  The VEML7700 is attached via the I2C bus.

  robcranfill@gmail.com
"""
import adafruit_veml7700
import board
import busio
from rpi_backlight import Backlight

import argparse
from datetime import datetime
import math
import sys
import time
 

LOG_FILE_NAME = "blatb-data.log"
BRIGHTNESS_FLOOR = 10 

# exit values
EXIT_VALUE_SENSOR  = 1
EXIT_VALUE_LOGGING = 2
EXIT_VALUE_OTHER   = 3


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
  # print(f"  luxToLCDLevel: {luxIn:0.2f} -> {result:0.2f}")
  return result


# ------------------ main
#
if __name__ == "__main__":

  parser = argparse.ArgumentParser(
              prog="blatb",
              description="Set RPi backlight according to VEML7700 light sensor.",
              epilog="")
  
  parser.add_argument("-d", "--data", action="store_true")
  parser.add_argument("-t", "--test", action="store_true")

  args = parser.parse_args()
  dump_data = args.data
  test_mode = args.test

  try:
    
    try:
      i2c = busio.I2C(board.SCL, board.SDA)
      veml7700 = adafruit_veml7700.VEML7700(i2c)
    except:
      print("Error connecting to VEML7700 sensor; is there one?")
      sys.exit(EXIT_VALUE_SENSOR)

    try:

      # prevent integration_time_value error. (is this the best way?)
      #     File "/home/pi/.local/lib/python3.7/site-packages/adafruit_veml7700.py", line 194, in integration_time_value
      #       return self.integration_time_values[integration_time]
      #   KeyError: 6
      veml7700.light_integration_time = veml7700.ALS_100MS
      
      # This measures the light, also in "lux" units.
      light = veml7700.light
      lux   = veml7700.lux
      # print(f"Ambient light: {light:0.2f}, Lux: {lux:0.2f}")

      level = int(luxToLCDLevel(lux))
      now = datetime.now().strftime('%x %X')

      if dump_data:
        logfile = open(LOG_FILE_NAME, "a")
        logfile.write(f"{now}\t{light:.0f}\t{lux:.0f}\t{level}\n")
        logfile.close() 

      if test_mode:
        print("Test mode - NOT setting backlight level!")
      else:
        print(f"{now} Ambient light: {light:0.2f}, Lux: {lux:0.2f} -> Set backlight to {level:2.0f}%")
        # print(f"  Set backlight to {level:2.0f}%")
        fadeTo(level, 0.5)
  
    except Exception as e:
      print(f"Error writing data! {e}")
      sys.exit(EXIT_VALUE_LOGGING)

  except Exception as e:
    print(f"Exception {e}")
    sys.exit(EXIT_VALUE_OTHER)

  finally:
    pass

