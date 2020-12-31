"""
  Back Light According To Brigtness
  Set the Raspberry Pi's LCD backlight according to the current ambient brightness, as measured by a light sensor.
  robcranfill@gmail.com
"""
from datetime import datetime
from rpi_backlight import Backlight
import sys
import pytz
import time
import math
import board
import busio
import adafruit_veml7700
 
TEST = False
LOG = True
LOG_FILE_NAME = "blatb-data.log"
BRIGHTNESS_FLOOR = 10 


# Set the backlight to the indicated percent (0-100), over the given fade time.
def fadeTo(brightPercent, durationSeconds):
    backlight = Backlight()
    with backlight.fade(duration=durationSeconds):
        backlight.brightness = brightPercent

# return 0-100 based on ... something
# https://hackaday.io/page/6590-ambient-light-sensing
#  which is

# actually, return BRIGHTNESS_FLOOR - 100
def luxToLCDLevel(luxIn):

    if (luxIn < 1254):
      result = 9.9323 * math.log(luxIn) + 27.059
      result = result / 2
    else:
      result = 100
    if result < BRIGHTNESS_FLOOR:
        result = BRIGHTNESS_FLOOR
    print(f"luxToLCDLevel: {luxIn} -> {result}")
    return result


if __name__ == "__main__":

    if TEST:
        print("Test mode - NOT setting")

    i2c = busio.I2C(board.SCL, board.SDA)
    veml7700 = adafruit_veml7700.VEML7700(i2c)

    # print(f"Arguments count: {len(sys.argv)}")
    # for i, arg in enumerate(sys.argv):
    #     print(f"Argument {i:>6}: {arg}")

    
    while True:
        lux = veml7700.lux
        print(f"Ambient light: {veml7700.light:.0f}, Lux: {lux:.0f}")
        if LOG:
          logfile = open(LOG_FILE_NAME, "a")
          now = datetime.now()
          logfile.write(f"{now}\t{veml7700.light:.0f}\t{lux:.0f}\n")
          logfile.close() 
        bl = int(luxToLCDLevel(lux))
        print(f" -> Set backlight to {bl}%")
        if not TEST:
          fadeTo(bl, 0.5)
        time.sleep(5)

