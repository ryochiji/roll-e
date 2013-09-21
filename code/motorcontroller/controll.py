import serial
import time


class Controller:

    def __init__(self, serialport):
        self.s = serialport
        self.channel = chr(0x09)
        self.speed0 = 0
        self.speed1 = 0

    def _send_cmd(self, command):
        self.s.write(chr(0xAA)+self.channel+command)

    def m0_forward(self, speed):
        self._send_cmd(chr(0x09)+chr(int(speed)))

    def m1_forward(self, speed):
        self._send_cmd(chr(0x0D)+chr(int(speed)))

    def m0_stop(self):
        self.m0_forward(0)

    def m1_stop(self):
        self.m1_forward(0)

    def stop(self):
        self.m0_stop()
        self.m1_stop()

    def m0_reverse(self, speed):
        self._send_cmd(chr(0x0A)+chr(int(speed)))

    def m1_reverse(self, speed):
        self._send_cmd(chr(0x0E)+chr(int(speed)))

    def do(self, command, speed=0):
        speed = int(speed)
        if command == 'forward':
            self.m0_forward(speed)
            self.m1_forward(speed)
        elif command == 'stop':
            self.m0_stop()
            self.m1_stop()
        elif command == 'reverse':
            self.m0_reverse(speed)
            self.m1_reverse(speed)
        elif command == 'left':
            self.m0_forward(speed)
            self.m1_reverse(speed)
            time.sleep(0.5)
            self.stop()
        elif command == 'right':
            self.m0_reverse(speed)
            self.m1_forward(speed)
            time.sleep(0.5)
            self.stop()

ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)
c = Controller(ser)
while True:
    line = raw_input('command>')
    line = line.strip()
    parts = line.split(' ')
    if len(parts)>1:
        c.do(parts[0],parts[1])
    else:
        c.do(parts[0])
