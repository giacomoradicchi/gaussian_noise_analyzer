"""
%%%%%%%%%*%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%!
% FILE ........... noise_writer.ino                                          %
% LANGUAGE ....... Python                                                    %
% DESCRIPTION .... reads a noise signal from serial port and writes it on    %
                   a .txt file. It then analyzes data using                  %
                   noise_analyzer.py                                         %
% PLATFORM ....... Arduino UNO R4 Wi-Fi                                      %
% LINK-FILEs ..... none                                                      %
% DATE ........... Apr/17/2026                                               %
% LAST-MFD ....... May/19/2026                                               %
% CREATED by ..... Group A1                                                 %
%%%%%%%%%*%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%!
"""

import serial
import time

from noise_analyzer import analyze_data

# parameters
input_duration = 1 # secs
serial_port = '/dev/tty.usbmodem9888E00985442' # to see the serial input, write on terminal 'ls /dev/tty.*'
ser = serial.Serial(serial_port, 2000000)
#output_file = 'data.txt'
output_file = 'test_data/test_data.txt'

time.sleep(1)

print("start reading...")
t0 = time.time()
with open(output_file, 'w', newline='') as f:
    while time.time() - t0 < input_duration:
        line = ser.readline().decode('utf-8', errors='ignore')
        if line:
            f.write(line)


print("finished reading!")

analyze_data(output_file, input_duration)