#!/usr/bin/python
"""
IRDAR - Infrared Detection and Ranging

Designed for use with the following hardware:
 * Raspberry Pi
 * Adafruit 16 channel servo driver (i2c)
 * Sharp IR distance sensor GP2Y0A02YK
 * MCP3008

For more info: http://ryosprojects.wordpress.com/2013/09/13/irdar-infrared-detection-and-ranging-with-the-raspberry-pi/
"""

import sys
sys.path.append('../../adafruit/Adafruit_PWM_Servo_Driver/')
from Adafruit_PWM_Servo_Driver import PWM
import distance
import time

pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

# Set this value to a lower value for faster scans. Faster scans may
# come at the expense of accuracy.
MIN_DELAY = 0.15

def setAngle(channel, angle, delta=170, min_delay=0.02):
    """
        Sets angle of servo (approximate).
        :param channel: Channel servo is attached to (0-15)
        :param angle: off of center, ( -80 through 80)
    """
    delay = max(delta * 0.003, min_delay)
    zero_pulse = (servoMin + servoMax) / 2  # half-way == 0 degrees
    pulse_width = zero_pulse - servoMin     
    pulse = zero_pulse + (pulse_width * angle / 80)
    pwm.setPWM(channel, 0, int(pulse))
    time.sleep(delay)

if __name__=="__main__":
    if len(sys.argv)==1:
        print "Usage: python setangle.py <channel> <angle>"
        sys.exit(1)

    channel = int(sys.argv[-2]) 
    pwm.setPWMFreq(60)                        
    setAngle(channel, int(sys.argv[-1]))
    time.sleep(1)
