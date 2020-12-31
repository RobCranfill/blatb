# blatb
Backlight according to (ambient) brightness

Yet another (sub)projet for my Raspberry Pi weather display.

This sets the display's backlight according to the ambient light level as 
read by an attached [Adafruit VEML7700 light sensor](https://learn.adafruit.com/adafruit-veml7700).


I wasn't sure what range of values the sensor returns, so I included code to dump the raw values to a file.
This isn't necessary and I guess I may remove that in the near future. The included shell script
finds the min and max of those values.

