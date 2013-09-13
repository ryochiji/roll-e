"""
Code to measure distance using IR sensor on a RasPi via the MCP3008
chip.

Code taken from: https://github.com/jerbly/Pi

Also see:
http://jeremyblythe.blogspot.co.uk/2012/09/raspberry-pi-distance-measuring-sensor.html
http://jeremyblythe.blogspot.co.uk/2012/09/raspberry-pi-hardware-spi-analog-inputs.html
""" 
import sys
sys.path.append('../../jerbly-pi/')
import spidev
import time
import os
import mcp3008

DEBUG = 0

spi = spidev.SpiDev()
spi.open(0,0)

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    r = spi.xfer2([1,(8+adcnum)<<4,0])
    adcout = ((r[1]&3) << 8) + r[2]
    return adcout

def get_distance(port=1):
    num_samples = 20
    r = []
    for i in range (0,num_samples):
        r.append(mcp3008.readadc(1))
    a = sum(r)/float(num_samples)
    v = (a/1023.0)*3.3
    d = 16.2537 * v**4 - 129.893 * v**3 + 382.268 * v**2 - 512.611 * v + 306.439
    return int(round(d))

if __name__=="__main__":
    while True:
        cm = get_distance()
        inches = float(cm) / 2.54 
        print "%d cm, %.2f inches" % (cm, inches)
        time.sleep(1)
