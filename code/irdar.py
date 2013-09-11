#!/usr/bin/python

import sys
sys.path.append('../adafruit/Adafruit_PWM_Servo_Driver/')
sys.path.append('../jerbly-pi/')
from Adafruit_PWM_Servo_Driver import PWM
import distance
import time

pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setAngle(channel, angle, delta=170, min_delay=0.02):
    """
        Sets angle of servo (approximate).
        :param channel: Channel servo is attached to (0-15)
        :param angle: off of center, ( -80 through 80)
    """
    delay = max(delta * 0.003, min_delay=0.05)
    zero_pulse = (servoMin + servoMax) / 2  # half-way == 0 degrees
    pulse_width = zero_pulse - servoMin     
    pulse = zero_pulse + (pulse_width * angle / 80)
    pwm.setPWM(channel, 0, int(pulse))
    time.sleep(delay)

def irdar_sweep(channel, start, end, incr=5):
    angle = start
    distances = {}
    while True: 
        distances[angle] = distance.get_distance()             
        angle += incr
        setAngle(channel, angle, incr, min_delay=0.05)
        if start > end and angle < end: break
        elif start < end and angle > end: break 

    return distances

def set_char_at(s, index, c):
    l = list(s)
    l[index] = c
    return ''.join(l)

def print_screen(history, angles):
    angles.sort()
    buff = {}
    for angle in angles:
        buff[angle] = ' '.rjust(120)
    blips = ['.', '*', '#', '@']
    blips = blips[-len(history):]      # if we only have 2, take last 2 blips
    for h in history:
        blip = blips.pop(0)
        for angle in angles:
            if angle not in h: continue
            dist = h[angle]
            if dist < 120:
                buff[angle] = set_char_at(buff[angle], dist, blip)
    for angle in angles:
        obstacle = 'x' if '@' in buff[angle][0:30] else ' '
        print "%s %s %s" % (str(angle).rjust(5), obstacle, buff[angle])

def sweep_and_print(channel, start, end, incr=5):
    history = []
    while True:
        distances = irdar_sweep(channel, start, end, incr)
        history.append(distances)
        history = history[-4:] #keep last 4
        temp = end
        end = start
        start = temp
        incr = incr * -1
        print_screen(history, distances.keys())

if __name__=="__main__":
    channel = 15 
    pwm.setPWMFreq(60)                        
    setAngle(channel, -45)
    time.sleep(1)

    sweep_and_print(channel, -45, 45)
    """
    distances = irdar_sweep(channel, -45, 45)

    angles = distances.keys()
    angles.sort()
    for angle in angles:
        cm = distances[angle]
        if cm > 120:
            blip = ''   #no blip
        else:
            blip = '#'.rjust(cm)
        print "%s: %s" % (str(angle).rjust(5), blip)
    """
