"""
%%%%%%%%%*%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%!
% FILE ........... noise_writer.ino                                          %
% LANGUAGE ....... Python                                                    %
% DESCRIPTION .... reads a noise signal from serial port and writes it on    %
                   a .txt file. It then analyzes data using                  %
                   noise_analyzer.py                                         %
% PLATFORM ....... Arduino UNO R4 Wi-Fi                                      %
% LINK-FILEs ..... none                                                      %
% DATE ........... Apr/17/2024                                               %
% LAST-MFD ....... Apr/17/2024                                               %
% CREATED by ..... Group A1                                                 %
%%%%%%%%%*%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%%%%%%%%%*%%!
"""

import serial
import time

from noise_analyzer import analyze_data

# parameters
input_duration = 10 # secs
serial_port = '/dev/tty.usbmodemB081849E6E302' # to see the serial input, write on terminal 'ls /dev/tty.*'
ser = serial.Serial(serial_port, 2000000)
output_file = 'data.txt'

time.sleep(1)

t0 = time.time()
with open(output_file, 'w', newline='') as f:
    while time.time() - t0 < input_duration:
        linea = ser.readline().decode('utf-8')
        f.write(linea)
        #print(linea)

analyze_data(output_file)