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
sys.path.append('../adafruit/Adafruit_PWM_Servo_Driver/')
sys.path.append('../jerbly-pi/')
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

def irdar_sweep(channel, start, end, incr=5, distances=None):
    """ Sweep IRDAR and record distances
        :param channel:   channel the servo is connected to
        :param start:     starting angle
        :param end:       ending angle
        :param incr:      increment by this many degrees
        :param distances: add data to this dict
    """
    angle = start
    if not distances: distances = {} 
    while True: 
        setAngle(channel, angle, incr, min_delay=MIN_DELAY)
        distances[angle] = distance.get_distance()             
        angle += incr
        if start > end and angle < end: break
        elif start < end and angle > end: break 
  
    return distances

def irdar_full_sweep(channel):
    """ A different sweeping algorithm where each sweep only
        has 10 degree resolution, but by scanning the 10s in
        one pass and the 5s in the next pass, you get 5 degree
        resolution after 2 sweeps, but each sweep goes faster.
    """ 
    distances = {}
    distances = irdar_sweep(channel, -30, 30, 10, distances)
    distances = irdar_sweep(channel, 35, -35, -10, distances)
    return distances


def set_char_at(s, index, c):
    """ Used by the text visualizer """
    l = list(s)
    l[index] = c
    return ''.join(l)


def print_screen(history):
    """ Print 2D visualization onto console """

    # Extract the angles from the distance data. Usually this won't change 
    # from scan to scan, but there are scanning algorithms where that may not 
    # be the case 
    angles = []
    for h in history:
        angles = list(set(angles + h.keys()))   
    angles.sort()

    # Create a 2D grid of characters. Essentially a "screen buffer"
    buff = {}
    for angle in angles:
        buff[angle] = ' '.rjust(120)

    
    blips = ['.', '*', '#', '@']
    blips = blips[-len(history):]      # if we only have 2, take last 2 blips

    # Plot blips onto buffer 
    for h in history:
        blip = blips.pop(0) if len(blips) else '.'
        for angle in angles:
            if angle not in h: continue
            dist = h[angle]
            if dist < 120:
                buff[angle] = set_char_at(buff[angle], dist, blip)

    # Output
    print "\n\n\n"
    for angle in angles:
        obstacle = 'x' if '@' in buff[angle][0:30] else ' '
        print "%s %s %s" % (str(angle).rjust(5), obstacle, buff[angle])
    print '20cm'.rjust(30) + '50cm'.rjust(30) + '1m'.rjust(50)


def irdar_scan(channel, start, end, incr=5, bidirectional=True,
                    num_history=4, func=print_screen):
    """
        Continously scan the IRDAR. By default, a crude text-based 
        visualization is outputted to the console, but you can do
        othings with the output by passing in a callback function 
        as the 'func' parameter.

        :param channel: Channel the servo is connected to
        :param start:   Starting angle of a sweep
        :param end:     Ending angle of a sweep
        :param incr:    Angle to increment by
        :param bidirectional: Scan back and forth if True. Otherwise it will
                              scan in one direction, then immediately go back
                              to the starting position, and scan again.
        :param num_history: Number of past scans' data to save
        :param func:    Callback function. Override to do something other 
                        than print the default output.
                        The function will be passed a single list containing
                        dicts with distance data. The dicts are keyed by angle
                        with distances (in centimeters) as values.
    """
    history = []
    while True:
        distances = irdar_sweep(channel, start, end, incr)
        history.append(distances)
        history = history[-num_history:] 
        if bidirectional:
            temp = end
            end = start
            start = temp
            incr = incr * -1
        else:
            setAngle(channel, start, abs(end - start))
        func(history)

if __name__=="__main__":
    channel = 15 
    pwm.setPWMFreq(60)                        
    setAngle(channel, -30)
    time.sleep(1)

    irdar_scan(channel, -45, 45, incr=3)
