# blatb
Backlight according to (ambient) brightness

Yet another (sub)projet for my Raspberry Pi weather display.

This sets the display's backlight according to the ambient light level as 
read by an attached [Adafruit VEML7700 light sensor](https://learn.adafruit.com/adafruit-veml7700).


I wasn't sure what range of values the sensor returns, so I included code to dump the raw values to a file.
This isn't necessary and I guess I may remove that in the near future. The included shell script
finds the min and max of those values.


## Prerequisites
* Hardware
  * RPi & Raspian
  * An attached Adafruit VEML7700 light sensor (see above link)
  * Must enable I2C (using raspi-config)
  * Must restart after updating udev rules

* Software libraries
  * adafruit_veml7700
	  * `pip3 install adafruit-circuitpython-veml7700`
  (this will also install various other Adafruit "Circuit Python" libraries.)
  * rpi-backlight
	  * `pip3 install rpi-backlight`
